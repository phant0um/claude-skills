---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: retro
description: "Use when: /retro — retrospectiva de sessão que propõe melhoria no AMBIENTE do agente (navegação, gate automático, tool economy, no-op em steering file, acesso a informação), não no comportamento dele. Diferente do modo retrospectiva de [evolve](../evolve/SKILL.md) (que extrai padrão da sessão para virar skill) e de hill-climb (que roda eval fixture); retro conserta o terreno em que o agente pisa."
triggers:
  positive:
    - "/retro"
    - "retrospectiva de sessão"
    - "por que essa sessão foi cara"
    - "regra do CLAUDE.md devia ser gate ou hook"
  negative:
    - "extrair skill nova da sessão (evolve)"
    - "endurecer agente contra fixture (hill-climb)"
updated: 2026-10-25
effort: medium
trigger: "/retro"
reads:
  - CLAUDE.md
  - 04-SYSTEM/ROUTER.md
  - 06-GENERATED/observability/
writes:
  - 06-GENERATED/reports/hill-proposals/
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisao 2026-10-25: evolve modo retrospectiva = codex-retrospective (fronteira declarada); CODING_STANDARDS so em repo externo; destino hill-proposals/retro-<data>/REPORT.md (layout do loop Hill); limiar 2 ou mais; trigger CLAUDE.md inchado removido (roteia para writing-for-agents). NAO conferido: source de Zach Lloyd/Poteto nao sustenta a tese; retro ausente do MOC de skills e do run-skill-evals; trigger-eval nao re-rodado."
---

> Adaptado de `mattpocock/skills` → `in-progress/retro` (2026-08-30).

Você está propondo melhorias no **ambiente** do agente para melhorar runs futuras.
O alvo é o terreno — arquivo de steering, gate, ferramenta, ponteiro — nunca uma
correção pontual do output desta sessão.

## Steps

1. Invocar [writing-for-agents](../writing-for-agents/SKILL.md) — todo
   candidato que vira texto obedece àquelas regras.
2. Ler as fontes primárias da sessão indicada. Sem indicação, use a corrente.
3. Levantar candidatos nas categorias abaixo.
4. Apresentar em ordem de severidade, com a evidência da sessão que sustenta cada
   um. Não aplicar: proposta em `06-GENERATED/reports/hill-proposals/retro-<data>/REPORT.md`.

**Critério de done:** toda categoria percorrida e ou tem candidato com evidência,
ou está explicitamente marcada sem achado. Categoria não visitada não conta.

## Categorias

- **Navegação** — quão fácil foi achar o arquivo certo? Há dependência escondida
  entre arquivos? Um **navigation pointer** resolveria? *Use quando* a sessão
  demorou para achar uma informação.
- **Gate automático** — existe check que teria pego o erro cometido? Lint, tipo,
  teste, linter de filesystem, `harness-audit.py`? *Use quando* o agente errou algo
  que uma checagem mecânica pegaria. Leia antes o comando de check do próprio
  repo (no vault, `04-SYSTEM/scripts/run-gates.py`; em repo externo, scripts `lint`/`check` ou job de CI): check que existe mas está desligado ou
  quebrado em silêncio é o achado, não reinvenção. Repo sem **guardrail** nenhum
  (sem pre-commit e sem CI rodando lint/typecheck/teste) é achado por si só.
- **Regra de revisão** — o revisor (shield, `code-review`) devia ganhar regra nova?
  Alguma regra existente devia sair ou ser esclarecida? Classifique a violação
  primeiro: **mecânica** (padrão sintático fixo, API banida, forma de import, regra
  de local de arquivo) vira check determinístico — regra no linter do repo, hook
  de pre-commit ou job de CI, o que for mais barato. Construir o check é o default.
  o arquivo de padrões (no vault, `shield.md` e `code-review`; em repo externo, `CODING_STANDARDS.md` se existir) fica só para **julgamento** (consistência entre arquivos,
  "segue o estilo ao redor"). *Use quando* o revisor deixou passar.
- **Steering global** — há instrução no `CLAUDE.md` que devia virar regra de
  revisão ou gate? *Use quando* o arquivo está grande.
- **Tool economy** — houve tool call cara que dava para simplificar? Algum CLI/MCP
  é particularmente ineficiente em token? *Use quando* uma chamada saiu cara.
- **No-ops** — instrução em steering file que não muda o comportamento. Teste é
  relativo ao modelo, não ao leitor: resolve rodando, não debatendo. *Use quando*
  os arquivos de steering estão grandes e pesados.
- **Acesso a informação** — dá para aumentar o acesso do agente? Log de servidor
  em tee, leitura somente-leitura de serviço externo. *Use quando* uma informação
  crucial não estava disponível.
- **Correção repetida vira gate** — nas transcrições/logs da sessão, levante as
  intervenções humanas (correção, pedido de refazer) e agrupe por tema. Correção
  que aparece **2 ou mais vezes** vira restrição determinística (hook, regra de
  lint, schema check, teste), não regra em prosa: agente segue restrição do
  ambiente com mais fidelidade que regra branda (Zach Lloyd, "factory
  engineering"; palestra do Poteto `[hyp]`: tese não confirmada na source do vault). Cada candidato sai com contagem de
  ocorrências e tipo de gate proposto; gate novo só conta com negativo plantado
  (contrato 4). *Use quando* o humano repetiu a mesma correção na sessão.
- **Script recorrente** — tarefa repetida, ou correção que o agente errou 2 ou mais vezes →
  recomendar script/CLI próprio (+ skill que o chama). Todo script novo exige gate
  com negativo plantado e teste que falha quando o layout/API muda, senão apodrece
  em silêncio e o agente confia no output. *Use quando* a mesma tarefa mecânica
  voltou ou o mesmo erro se repetiu.

## Reference

### Implementação vs revisão

Todo trabalho passa por dois estágios. O agente de **implementação** carrega a
maior **pressão de contexto**: explora, escreve e depura. O de **revisão** carrega
a menor — recebe um diff, não explora, em geral não escreve nem depura.

Consequência: o padrão de código é responsabilidade do revisor, não do
implementador. Regra empurrada para o implementador gasta contexto onde ele tem
menos sobrando.

### Onde cada coisa mora no vault

- `CLAUDE.md` / `AGENTS.md` — entram no contexto de todo agente do repo. Use com
  parcimônia extrema, quase só para **navigation pointer** a outros arquivos.
- `04-SYSTEM/ROUTER.md` — o router: onde fica o quê. Candidato de navegação vai
  aqui antes de ir para o `CLAUDE.md`.
- Policies em `04-SYSTEM/automation/agents/nexus-system/policies/` — lidas
  sob demanda, não sempre. Regras do revisor vivem em `agents/agents/shield/shield.md` e em `skills/dev/code-review/`.
- Skills — para doc (a description entra no contexto) ou comando invocado pelo
  humano. Siga writing-for-agents.
- Gates em `04-SYSTEM/scripts/` — gate novo só conta quando detecta negativo
  plantado (contrato 4 do `CLAUDE.md`).

## Quando NÃO usar

retro conserta o **terreno** — steering, gate, tool, ponteiro. Fora disso, a
irmã certa:

- Extrair um **padrão da sessão para virar skill nova** →
  [evolve](../evolve/SKILL.md) (modo padrão, Fase 1). O modo retrospectiva de `evolve` ([codex-retrospective](../evolve/codex-retrospective.md)) revisa N dias de erros repetidos e fricção e se sobrepõe a retro nessas categorias: sessão única e ambiente é retro; janela de dias e routing é codex-retrospective. retro propõe
  melhoria de ambiente, não cria capability.
- **Endurecer um agente contra fixture de eval** →
  [hill-climb](../hill-climb/SKILL.md). retro não roda eval nem
  mede regressão comportamental.
- **Corrigir o output pontual desta sessão** → faça a correção direto no
  artefato. retro só levanta melhoria de ambiente para runs futuras.

## Completion

- [ ] Toda categoria percorrida: com candidato e evidência, ou marcada sem achado.
- [ ] Candidatos em ordem de severidade, cada um com a evidência da sessão.
- [ ] Proposta gravada em `06-GENERATED/reports/hill-proposals/retro-<data>/REPORT.md`, nada aplicado.

## Failure modes

- **Aplicar a melhoria**: editar steering, gate ou tool durante o retro → só proponha; aplicação é outra tarefa.
- **Categoria não visitada**: pular categoria sem marcar → não conta como percorrida.
- **Candidato sem evidência**: melhoria sem trecho da sessão que a sustente → descarte ou busque a evidência.
- **Capability no lugar de terreno**: propor skill nova → vai para `evolve`; retro conserta ambiente.
