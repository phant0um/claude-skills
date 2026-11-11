---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: hill-climb
description: "Use when: agente existente falha casos de avaliação e precisa de ciclo aval → diagnóstico → correção. Executar o ciclo completo de avaliação → diagnóstico → correção de um agente existente, iterando até que todos os casos passem ou o limite de rounds seja atingido."
version: 1.2
author: Nexus Agent System
tags: [eval, improve, regression, harness, spec-based]
updated: 2026-11-10
consolidated-by: R3 (absorveu probe, hill como modos)
reads:
  - 04-SYSTEM/automation/agents/
  - 04-SYSTEM/automation/procedures/core/
writes:
  - 06-GENERATED/tasks/lessons.md
  - evals/cases_<slug>.py
  - evals/results_<slug>_<round>.json
  - 04-SYSTEM/automation/agents/agents/<slug>/<slug>.md
  - 04-SYSTEM/automation/procedures/core/<slug>.md
  - 06-GENERATED/probe/<slug>-probe-*.md
triggers:
  positive:
    - "agente existente falha casos de avaliação"
    - "ciclo avaliação → diagnóstico → correção"
    - "melhorar agente iterando até passar nos casos"
  negative:
    - "agente novo sem suíte de eval"
    - "caso único trivial"
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7+W8: corpo completo lido pelo shield (opus, somente leitura); W3a/W7b/W7c: writes e caminhos reais de agente e procedimento; W8/W8b: perfis economy/bounded/deep de model-routing e reads de procedures/core; checks frontmatter/lint/evals verdes; 270 linhas, 12 secoes"
---
# Skill: Hill Climb

## Propósito
Executar o ciclo completo de avaliação → diagnóstico → correção de um agente existente, iterando até que todos os casos passem ou o limite de rounds seja atingido.

---

## Quando NÃO usar

- **Agente sem casos de avaliação** — hill-climb precisa de baseline mensurável para escalar.
- **Falha de arquitetura, não de configuração** — subir ladeira não corrige desenho errado; redesenhar.
- **Sem orçamento para múltiplas iterações** — hill-climb é incremental; uma tentativa não prova nada.
- **Skill imatura (<3 usos)** — sem histórico, ajuste é aposta; usar `hill-climb` só com dados.

Disambiguation: `hill-climb` melhora agente existente que falha casos de avaliação; `improve-agent-lifecycle-loop` é o ciclo de melhoria amplo; `evolve` extrai padrões reutilizáveis — hill-climb é o degrau de tuning.


## Condições de Ativação
Ative esta skill quando:
- O usuário solicitar `@harden [nome-do-agente]` ou `run reasoning/hill-climb/SKILL.md on [agente]`
- Um agente registrar taxa de falha >20% em evals consecutivos
- Pós-deploy de nova feature (regressão preemptiva)

NÃO ative para: agentes sem eval suite definida; queries simples sem histórico de falhas.

---

## Modos de Execução

| Modo | Runtime | Quando usar |
|------|---------|-------------|
| **Container** | Agentes `.py` em Docker, cURL contra API local | Harness com containers, agentes Python |
| **Spec-based** | Agentes `.md` lidos pelo modelo (padrão vault-michel) | scheduler legado, sem container |

No modo spec-based (vault-michel), agentes são arquivos `.md` em `04-SYSTEM/automation/agents/` (procedimentos como guard ficam em `04-SYSTEM/automation/procedures/core/`).
Não há container, não há `.py`, não há `docker restart`. A avaliação analisa se as instruções
do agente produziriam o comportamento esperado.

---

## Modelo por Etapa

| Etapa | Perfil (`model-routing.json`) | Justificativa |
|-------|--------|---------------|
| Leitura de agent spec + derivação de probes | economy | Leitura estruturada, baixo custo |
| Execução de probes (container: cURL / spec-based: análise) | economy | Chamadas repetitivas |
| Julgamento PASS/FAIL de cada probe | bounded | Sem task_class `judging`; escolha por risco (`risk_max: medium`), não por task_class |
| Diagnóstico de falha + seleção de lever | deep | Análise causal (`diagnosis` é task_class de `deep`; `bounded` cobre só bounded-edit/extraction) |
| Edição cirúrgica do agent spec | bounded | Requer coerência de texto |
| Re-run suite completo final (anti-regressão) | economy | Verificação mecânica |

---

## Protocolo de Execução

### PASSO 0 — Preparar o eval (uma vez, antes do round 1)

Fonte: automating-eval-design-and-hillclimbing-with-claude.

- **Origem dos casos, nesta ordem:** falhas reais (ledger de erros, `operations.md`,
  transcripts), depois casos escritos à mão, depois casos derivados do spec.
  Cada caso traz uma linha `why_hard`. Caso escolhido só porque o modelo atual
  falha nele mede o vale desse modelo, não o que importa.
- **Grader mais barato que serve:** output restrito (label, schema, path, regex)
  usa check programático. Output aberto usa judge com rubric de claims checáveis
  sim/não, nunca escala 1–5. Rubric só checa o que o input declara. O judge roda
  em modelo diferente do modelo configurado no agente testado.
- **Fixtures disfarçadas:** diretórios e arquivos que o modelo lê levam nomes
  neutros, sem "eval", "test", "canary", "fixture" nem dica da resposta
  esperada no path, para o modelo não reconhecer que está sendo avaliado. O
  gabarito fica fora do diretório lido. Exemplo:
  `04-SYSTEM/automation/evals/fixtures/skill-adversarial-gate/build_prompts.py`.
- **Judge de outra família:** quando o grader é LLM, usar família ou tier
  diferente do modelo otimizado, porque modelo favorece a própria saída
  (viés de autopreferência). Fonte: playbook de evals do Poteto.
- **Aprovação humana da suite:** suite nova ou alterada mostra ao humano os inputs
  e 3–5 casos já corrigidos, com a pergunta "você daria nota diferente?". Nota
  divergente corrige o caso ou a rubric antes do round 1. Aprovado, o arquivo de
  casos recebe `# approved: <data> <quem>`. Suite sem essa marca não inicia
  rounds, porque o climb otimizaria contra um grader que ninguém validou. Na
  rotina sem humano: gerar a suite, reportar para aprovação e parar.
- **Plumbing:** timeout, erro de ferramenta, resposta cortada ou arquivo ausente
  é falha de harness, não do agente. Excluir do score, registrar e corrigir o
  harness antes de medir ruído.
- **Split train/test ao acaso**, cerca de 2/3 e 1/3, fixado antes do round 1.
  O diagnóstico e os patches leem só o train. O test nunca é lido pelo climb.
  Suite com menos de 6 casos não tem test útil: declarar `holdout: none`
  no relatório e tratar qualquer ganho como não confirmado.
- **Gate de ruído:** rodar o baseline ao menos 2x e rodar o grader 2x no mesmo
  output. Flips entre rodadas idênticas medem o ruído. Se o ruído for maior ou igual
  ao menor ganho que importa, parar e pedir mais repeats ou casos. Não iniciar rounds.
  Reportar o baseline como k/n com IC Wilson 95% (binary-eval-statistics).
- **Headroom:** baseline ≥ 95% no train não tem espaço para qualidade.
  Trocar o objetivo para custo com qualidade igual (modelo e effort mais baratos,
  prompt mais curto) ou parar.

### Round de Avaliação (máx. 5 rounds, para mais cedo se tudo passar)

**PASSO 1 — Derivar Probes** *(economy)*
- Verificar se existe `evals/cases_<slug>.py`:
  - SIM → carregar suite existente como base, complementar se necessário
  - NÃO → derivar probes a partir do arquivo do agente (caminhos em Artefatos de Saída; identidade + restrições + fora do escopo)
- Target: 8–12 probes cobrindo: golden-path, edge cases, tool-selection, adversariais (prompt injection, input malformado, desvio de propósito)
- Adversarial aqui é categoria de input hostil que o agente vai encontrar em uso, com `why_hard` escrito. Não é caso escolhido porque o modelo atual erra (PASSO 0).
- Salve em `evals/cases_<slug>.py` no formato `{input, rubric, expected_behavior, why_hard}`
- Probe novo ou alterado reabre a aprovação humana do PASSO 0 antes do próximo round.
- Referência: [probe](probe.md) para geração de suite adversarial completa

**PASSO 2 — Executar Probes** *(economy; comparação vs rubric e PASS/FAIL: bounded)*

**Modo container:** Para cada probe, dispare via `cURL` contra o container local. Leia a
resposta + tool calls dos logs do container.

**Modo spec-based (vault-michel):** Agentes são arquivos `.md` lidos pelo modelo.
Avalie cada probe analisando se as instruções do agente (identidade, restrições,
comportamento de entrada, fora do escopo) produziriam o comportamento esperado:
1. Ler o agent spec completo
2. Simular: "dado este input, o que as instruções produziriam?"
3. Comparar resposta simulada vs rubric do probe
4. Se ambíguo → FAIL (safe default para agentes críticos) ou `OVERSPEC_RUBRIC`

Simular não é executar. Quem julga não pode ser o mesmo contexto que escreveu o patch,
e o veredito do mesmo probe precisa se repetir em 2 leituras (gate de ruído do PASSO 0).

Registre: `probe_id | status(PASS/FAIL) | type | reason`


**PASSO 3 — Julgar Falhas** *(deep)*
- Se `/score-drift` foi rodado antes: usar o relatório como pré-classificação
- Se falha é ambígua: rodar `/trace <slug> <comportamento>` antes de diagnosticar
- Para cada FAIL, classifique segundo a taxonomia:
  - `MISSING_RULE` → regra ausente nas instruções
  - `WRONG_TOOL` → ferramenta errada disparada
  - `HALLUCINATION` → resposta factualmente incorreta
  - `OVERSPEC_RUBRIC` → rubric de avaliação muito restrita
  - `CONTEXT_LOSS` → agente perdeu contexto de turns anteriores
  - `ADVERSARIAL_BYPASS` → falhou em input hostil

**PASSO 4 — Corrigir** *(bounded)*

**Modo container:** Edite `agents/<slug>.py`, hot-reload (`docker restart <slug>`).

**Modo spec-based:** Edite o arquivo do agente (caminhos em Artefatos de Saída) — patch aditivo nas seções existentes.

Levers por tipo de falha:
  - `MISSING_RULE` → adicione step em `## Comportamento de Entrada` ou restrição com o motivo em `## Restrições`
  - `WRONG_TOOL` → ajuste seleção de ferramenta em `## Ferramentas`
  - `HALLUCINATION` → adicione restrição explícita + exemplo genérico (nunca o caso do eval)
  - `OVERSPEC_RUBRIC` → relaxe o critério no eval case
  - `CONTEXT_LOSS` → aumente contexto histórico
  - `ADVERSARIAL_BYPASS` → adicione restrição nomeando o padrão de ataque e o dano que evita

**Nunca cole conteúdo de falha no agente.** Input, output esperado ou trecho de
transcript de um probe não entram no spec. O patch corrige a causa raiz (regra
ausente, seção que induz o erro) e não reformula uma linha. Patch que só serve para
os casos do eval é overfit, mesmo que passe.

**Remoção também é patch.** Regra que causa over-trigger, contradiz outra ou não
reproduz mais falha no modelo atual sai — um patch por vez, re-probe antes e depois,
registro no changelog do agente.

Re-execute os probes de **train** que falharam e depois o **test** inteiro *(economy)*

**Validation gate do ciclo (snapshot → evidência → rollback):**
- **Antes de aplicar a correção:** tirar snapshot do estado anterior (`git commit` ou cópia do arquivo do agente — ver Restrições).
- **Após aplicar:** a correção só é **adotada** com evidência de melhoria: re-run dos probes + métrica comparada (baseline → candidato). "Rodou" não é evidência.
- **Decisão train × test:** train e test sobem → manter. Train sobe e test fica flat → overfit provável, reverter. Regressão em qualquer um dos dois → reverter.
- **Sem melhoria ou regressão:** rollback ao snapshot + registro no lessons log — o score nunca fica abaixo do baseline (ratchet).

**PASSO 5 — Anti-regressão** *(economy)*
- Se todos os probes do round passaram, execute a suite completa
- Se algum probe previamente verde quebrou: reverta a última edição e registre como `REGRESSION_RISK`
- No modo spec-based: patches aditivos não devem quebrar passes existentes — verificar

**Round de reflexão (sem edição):** se o score travar por 2 rounds, ou se nenhum
patch possível ganharia mais que o ruído, não gastar round editando. Ler cada falha
de train restante e classificar a causa: agente (taxonomia do PASSO 3), task ambígua,
grader errado, harness ou variância. Só falhas do agente seguem para os próximos rounds.
Task ou grader quebrado viram `OVERSPEC_RUBRIC` e vão para correção do eval, registrada.

---

## Artefatos de Saída
- `evals/cases_<slug>.py` — suite persistente
- `evals/results_<slug>_<round>.json` — histórico de runs
- arquivo do agente endurecido: `04-SYSTEM/automation/agents/agents/<slug>/<slug>.md` (agentes) ou `04-SYSTEM/automation/procedures/core/<slug>.md` (procedimentos como guard)
- `06-GENERATED/tasks/lessons.md` — append de métricas do hill-climb

---

## Completion

- [ ] Todos os 5 pré-requisitos do loop presentes: fitness function, executor, keep-or-revert, lessons, budget
- [ ] Suite com marca `# approved:` e grader validado por humano antes do round 1
- [ ] Máximo 5 rounds executados (para cedo se todos probes passarem)
- [ ] Cada FAIL classificado segundo taxonomia (MISSING_RULE, WRONG_TOOL, HALLUCINATION, etc.)
- [ ] Correção aplicada (aditiva) + re-run dos probes que falharam
- [ ] Anti-regressão: suite completa rodada, zero probes previamente verdes quebrados
- [ ] `evals/results_<slug>_<round>.json` atualizado
- [ ] Lessons log appendado
- [ ] Relatório final: test × baseline como k/n com IC Wilson 95% e ruído medido. Ganho dentro do ruído ou ICs sobrepostos → recomendar não adotar

## Failure modes

- **Infinite loop**: 5 rounds esgotados sem convergir → gerar relatório de falhas pendentes, aguardar humano
- **Probe removal**: remover probe existente para subir score → fraude no ratchet, proibido
- **False PASS**: probe marcado PASS com alucinação factual → mesmo se rubric satisfeito, alucinação = FAIL
- **Overfit ao eval**: patch sobe o train e deixa o test flat, ou cola o caso no spec → reverter; o test existe para isso
- **Grader não validado**: climb sobe score contra rubric que ninguém conferiu → sem marca `# approved:`, não iniciar rounds
- **Round sobre ruído**: patch aceito por 1 flip quando o ruído medido é ≥ 1 flip → sem gate de ruído, o ratchet trava em sorte
- **Regression blindness**: só re-roda probes que falharam, ignora suite completa → sempre rodar suite inteira no final
- **Destructive patch**: remover regra sem re-probe antes e depois ou sem registro no changelog → remoção só como patch isolado e medido

---

## Restrições
- NUNCA edite o agente sem antes registrar o estado anterior (git commit ou backup)
- NUNCA marque um probe como PASS se a resposta contiver alucinação factual
- NUNCA remova um probe existente para fazer o rate subir — apenas melhore o agente
- Máximo de 5 rounds. Ao atingir o limite, gere relatório de falhas pendentes e aguarde intervenção humana

## Relacionado

- [probe](probe.md) — geração de suites adversariais
- [adversarial-probe](adversarial-probe.md) — ponteiro do MODO B3 (link direto: o conteúdo está em probe.md §MODO B3)
- [score-drift](../drift-review/score-drift.md) — medir drift antes do hill-climb
- 04-SYSTEM/automation/skills/reasoning/hill-climb/probe.md §MODO B3 — casos adversariais de drift para agentes (absorveu adversarial-probe, adr-nx-014)


## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO GERAR TESTES** — [probe](probe.md)
- **MODO LOOP AUTÔNOMO (rotina)** — hill-mode
