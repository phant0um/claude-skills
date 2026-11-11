---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: plan-handoff
skill: plan-handoff
version: 1
trigger: /plan-handoff [tarefa] [orquestrador=<modelo>] [executor=<modelo>]
effort: medium
description: "Use when: escrever plano detalhado em ondas para OUTRO modelo executar — orquestrador e executor nomeados, tabela de conflitos (se X, faça Y; senão pare), contrato EXEC spec por onda e formato exato do relatório que o orquestrador valida sem confiar no executor. Desafiar o plano antes é grill-me; paralelizar domínios na sessão é subagent-team; loop longo autônomo é autonomous-loop; spec de feature de código multi-sessão é spec-lifecycle."
tags:
  - planning
  - handoff
  - orchestrator
  - executor
  - exec-spec
  - delegation
created: 2026-10-03
updated: 2026-10-11
consumes:
  - prompt-contracts
  - loop-engineering
  - model-routing
reads:
  - 04-SYSTEM/system/governance/schemas/exec-spec.schema.json
  - 04-SYSTEM/system/governance/schemas/exec-report.schema.json
  - 04-SYSTEM/automation/agents/nexus-system/model-router.md
writes:
  - 07-QUEUE/plans/
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
references:
  - "prompt-contracts"
  - "loop-engineering"
  - "[adversarial-gate](../adversarial-gate/SKILL.md)"
verifier:
  - python3 04-SYSTEM/scripts/check-exec-spec.py <W*.exec-spec.json> exit 0 em toda onda; todo done_when falha no estado ANTES da execução.
human_gate: false
triggers:
  positive:
    - /plan-handoff
    - crie o plano em etapas para outro modelo executar
    - plano detalhado com orquestrador e executor
    - escreva como o executor deve fazer o relatório para eu validar
  negative:
    - tarefa que eu mesmo executo nesta sessão em <30 min
    - desafiar ou questionar um plano (grill-me)
    - executar um plano já escrito
reviewed-scope: "checagem mecanica apos 4 edicoes (saida 07-QUEUE, gate de manifest, prova de conservacao, specs gravados): 10/10 wikilinks resolvem; skill-lint GREEN; kind=skill-proc, 16 secoes, 281 linhas. Sem varredura R12 nem eval novo"
reviewed-by: claude-sonnet-5-5 (sessao 2026-10-11, revisao mecanica)
reviewed: 2026-10-11
---

# Skill: plan-handoff

## Propósito

Produzir um plano que outro modelo executa sem contexto desta sessão e que o
orquestrador valida sem confiar no relatório. O plano tem três camadas: ondas
em Markdown para leitura, um EXEC spec JSON por onda para a máquina e um
contrato de relatório que o executor preenche.

Relatório de executor é alegação, não evidência. Por isso o plano já entrega os
comandos que o orquestrador roda por conta própria.

## Quando NÃO usar

- **Você mesmo executa, em menos de 30 min** — escrever plano custa mais que fazer.
- **Ainda não está decidido o quê fazer** — `grill-me` (ou `office-hours`) primeiro.
  Plano sobre premissa falsa só delega o erro.
- **Feature de código multi-sessão com spec formal** — `spec-lifecycle`; esta skill
  pode gerar o plano de execução depois que a spec existir.
- **Domínios paralelos despachados agora, na sessão** — `subagent-team`.
- **Loop autônomo com context resets** — `autonomous-loop`; ele consome um plano,
  não o escreve.

Disambiguation: `plan-handoff` escreve e contrata; `subagent-team` e
`autonomous-loop` executam; `adversarial-gate` valida cada onda concluída.

## Entradas

| Campo | Obrigatório | Default se ausente |
|---|---|---|
| tarefa | sim | — |
| orquestrador | não | perfil `orchestrator` no model-router (hoje sonnet·medium); quem escreve o plano usa o perfil `planner` (hoje opus·medium) |
| executor | não | executor mais barato que cumpre o critério. Mecânico: haiku·low ou sonnet·low. Julgamento: não delegar. |
| escopo de escrita | não | inferido da tarefa e declarado no plano como suposição |

Modelo e effort vêm de
model-router. Não fixe par
modelo·effort aqui. Default assumido é declarado no topo do plano.

## Procedimento

### 1. Ancorar no estado real

Leia os arquivos-alvo antes de planejar. Registre no plano o que o executor
vai encontrar: path, contagem, hash curto ou linha âncora
(`git hash-object <path> | cut -c1-12`). O inventário do plano diverge do
filesystem com frequência. O executor precisa detectar essa divergência, não
herdá-la.

Se a tarefa muda efeito, autoridade ou custo material e há ambiguidade, pare.
Rode `grill-me` antes de continuar.

Se alguma onda cria, move ou apaga arquivo em `04-SYSTEM/`, o manifest baseline
(`harness-audit.py`, `BASELINE_REL`) congela a lista de paths e quebra. Rebaseline é
"manifest rewrite" e exige aprovação humana. Declare no plano um gate humano para
isso, com saída padrão: reverter a onda. Prefira desenho que não crie arquivo novo
quando o ganho não pagar o gate.

### 2. Cortar em ondas

Cada onda tem um executor, um objetivo verificável e um escopo de escrita
fechado. Regras de corte:

- **Uma onda, um owner.** Se duas partes tocam o mesmo arquivo, elas entram na
  mesma onda ou viram ondas sequenciais com `depends_on`.
- **Tamanho pelo executor.** Executor fraco recebe passos literais, um efeito
  por passo, sem "decida a melhor forma". Se um passo exige julgamento, ele fica
  com o orquestrador.
- **Ordem pelo risco.** A onda mais barata e reversível vai primeiro. Ela valida
  o formato do plano antes da onda cara.
- **Teto por onda.** `max_turns` ≤18 (limite do schema). Se a onda não cabe, faça
  `split`.

### 3. Escrever a tabela de conflitos

Para cada onda, liste o que pode dar errado e a resposta exata. Cubra no mínimo:

| Conflito | Resposta padrão |
|---|---|
| arquivo-alvo difere da âncora (hash/linha) | não editar; `conflicts_hit`; `stop_and_report` |
| teste falha ANTES da mudança | registrar como estado pré-existente; não corrigir fora do escopo |
| passo exige arquivo fora de `files_allow` | parar; `next_planner_action: expand_allowlist` |
| instrução admite 2 leituras | escolher a mais conservadora, registrar em `assumptions` |
| `done_when` não passa depois de 2 tentativas | `stop_and_revert`; status `failed` |
| ferramenta ou comando ausente | parar; `blocker` com o erro exato |
| orçamento esgotado | `on_budget_exit` da onda; status `budget_exit` |

Proibições valem para toda onda e entram no plano literalmente. O executor
nunca resolve conflito por um destes caminhos:

- ampliar o escopo;
- enfraquecer ou apagar teste;
- editar o critério de done;
- copiar um fix pronto de fora do escopo.

A tabela vira o campo `conflicts` do EXEC spec. `else` diz o que fazer quando o
`then` não resolve.

### 4. Escrever `done_when` que já falha

Todo `done_when` é um comando, um grep, um regex ou a existência de um arquivo.
Nenhum critério é "ficou bom". Antes de entregar o plano, rode cada `done_when`
no estado atual: ele **tem que falhar**. Critério que já passa antes da execução
é verde de graça e não prova nada. Se não houver como falhar antes, o critério
está errado. Falhar porque a pasta de trabalho do plano ainda não existe não conta:
o critério precisa falhar porque o trabalho falta.

**Onda de refactor (mover ou cortar texto):** o `done_when` inclui uma prova de
conservação. Um script compara o conjunto de linhas não vazias antes e depois:
toda linha antiga sobrevive na árvore alvo, salvo uma allowlist de duplicatas
declarada por faixa de linha, e o número de linhas novas é o esperado. Linha
perdida ou nova fora do esperado reprova a onda.

### 5. Escrever o contrato de relatório

O executor grava `W<n>.exec-report.json` ao lado do spec, conforme
`exec-report.schema.json`. O plano copia este bloco para o executor:

```text
RELATÓRIO — obrigatório, um JSON por onda, em <dir>/W<n>.exec-report.json
- status: success | partial | failed | blocked | budget_exit. Use partial
  quando algum done_when falhou. Nunca use success sem todos os done_when passando.
- tests[]: um item por done_when. evidence = comando exato + exit code +
  a linha decisiva da saída. Sem evidence, passed=false.
- files_touched: todo arquivo escrito, inclusive os revertidos.
- deviations[]: todo passo feito diferente do plano (step, what, why).
- assumptions[]: toda escolha entre duas leituras possíveis.
- conflicts_hit[]: todo conflito da tabela que ocorreu e a ação tomada.
- blocker: erro exato (uma linha) ou null.
- next_planner_action: accept só se status=success e deviations vazio.
Não escreva prosa fora do JSON. Não resuma o que deu certo: a evidência mostra.
```

Formato estrito quebra com frequência em modelo pequeno com effort baixo. O
validador pega a quebra. Relatório inválido gera uma re-emissão só do JSON e
não repete a onda.

### 6. Escrever a validação do orquestrador

Para cada onda, o plano lista o que o orquestrador roda **sem ler o relatório
primeiro**:

1. `python3 04-SYSTEM/scripts/check-exec-spec.py <dir>/W<n>.exec-report.json`: o schema.
2. Re-rodar cada `done_when` e comparar com `tests[]`. Divergência é falha, mesmo com status success.
3. `git status --porcelain` e `git diff --stat`: todo path tocado precisa estar em
   `files_allow`. Path fora da lista é violação. Path ausente de `files_touched` é relatório falso.
4. Ler `deviations` e `assumptions`. Toda suposição que muda efeito sobe para decisão.
5. Onda de risco médio ou alto: rodar `adversarial-gate` antes de aceitar.

Decisão por `next_planner_action` real, recalculada pelo orquestrador:

| Achado | Ação |
|---|---|
| tudo confere, sem deviations | `accept`; próxima onda |
| confere, com deviations ou assumptions | `run_review` |
| done_when falhou por lacuna do plano | `replan_gap`; corrigir o plano, não o executor |
| onda grande demais (budget_exit) | `split_task` |
| precisa de path novo | `expand_allowlist`, só com aprovação se mudar escopo material |

## Completion

O plano só está pronto para entrega quando todos os itens abaixo passam.


- [ ] Os specs estão gravados em disco por quem tem permissão de escrita (se o
      planejador é read-only, o orquestrador os extrai do plano e grava).
- [ ] `check-exec-spec.py` dá exit 0 em todo `W*.exec-spec.json`.
- [ ] Todo `done_when` falhou no estado atual. Registre a saída no plano, §Linha de base.
- [ ] Todo arquivo de `files_allow` existe ou tem um passo `create`.
- [ ] Nenhum passo pede julgamento a executor marcado como mecânico.
- [ ] O plano não depende de contexto desta sessão. Um leitor frio consegue executar.

## Saída

Arquivos em `07-QUEUE/plans/` (`06-GENERATED/plans/` está congelado desde 2026-08-24, ver ROUTER):

```text
07-QUEUE/plans/YYYY-MM-DD--plan--<escopo>--<slug>.md
07-QUEUE/plans/YYYY-MM-DD--plan--<escopo>--<slug>/W1.exec-spec.json
07-QUEUE/plans/YYYY-MM-DD--plan--<escopo>--<slug>/W1.exec-report.json   ← escrito pelo executor
```

Esqueleto do `.md`:

```markdown
---
title: "Plano — <título>"
type: plan
scope: <escopo>
status: proposed
orchestrator: <modelo@effort>
executor: <modelo@effort>
writer: orchestrator
created: YYYY-MM-DD
---

# Plano — <título>

> Para quem executa: documento auto-contido. Siga literalmente. Em dúvida,
> consulte a tabela de conflitos. Se ela não cobrir o caso, pare e reporte.

## 0. Objetivo e suposições declaradas
## 1. Linha de base (estado medido + saída dos done_when falhando)
## 2. Ondas
### W1 — <objetivo> (executor: <modelo>; depende de: —)
Passos literais · files_allow/deny · done_when · orçamento · spec: W1.exec-spec.json
Conflitos: tabela da onda
## 3. O que o executor NÃO faz
## 4. Contrato de relatório (bloco do §5)
## 5. Validação do orquestrador (comandos por onda)
## 6. Orçamento total e parada
```

## Stop conditions

- Tarefa ambígua com custo alto: pare e rode `grill-me`.
- `done_when` que não consegue falhar antes da execução: reescreva ou remova a onda.
- Onda que exige julgamento e o executor é mecânico: mova a onda para o orquestrador.

## Failure modes

- **Plano que herda inventário velho.** Contém paths que não existem mais. Previna com o §1 e com as âncoras.
- **done_when vacuamente verde.** Previna com o §4.
- **Relatório aceito pela palavra.** O orquestrador lê o status e não re-roda nada. Previna com o §6, passos 2 e 3.
- **Executor que "conserta" conflito.** Ele amplia escopo ou afrouxa teste. Previna com a lista de proibições do §3.
- **Plano preso à sessão.** Cita "como discutimos" ou um arquivo só lido na conversa. Previna com o checklist de §Completion.

## Related

- Contrato e budgets: loop-engineering §Contrato EXEC
- TaskPacket: prompt-contracts
- Gate por onda: [adversarial-gate](../adversarial-gate/SKILL.md)
- Gate do validador: `04-SYSTEM/scripts/test-check-exec-spec.py` (fixtures valid-* passam, negative-* falham)
- Porta de dev: dev §Qual cadeia por porte
- Exemplo aplicado (formato atual, em `07-QUEUE/plans/`):
  2026-10-11--plan--skills--context-engineering-claude5
- Exemplos manuais que originaram a skill (o 1º vive na pasta congelada `06-GENERATED/plans/`):
  2026-09-20--plan--harness--fechamento-lacunas-glm53flash ·
  resumo-generation-plan
