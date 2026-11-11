---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: autonomous-loop
description: "Use when: executar tarefa de desenvolvimento longa (>30 min, múltiplas features) como loop AUTÔNOMO Planner→Generator→Evaluator com context resets. Diferente de [adversarial-gate](../adversarial-gate/SKILL.md) (que é uma porta de validação por tarefa) — autonomous-loop é a ARQUITETURA do loop; adversarial-gate pode rodar dentro dele. Use autonomous-loop quando o problema é execução autônoma contínua, não validação pontual de done."
version: 1.2
author: Nexus Agent System
tags: [long-running, multi-session, context-reset, planner, evaluator, cleanup, simplify-code]
updated: 2026-10-11
reads: []
writes: []
triggers:
  positive:
    - "/autonomous-loop"
    - "tarefa de desenvolvimento >30 min múltiplas features autônoma"
    - "arquitetura Planner Generator Evaluator com context resets"
  negative:
    - "tarefa <30 min ou 1 domínio"
    - "trabalho sem iterações de feedback"
    - "sessão interativa curta"

reviewed-scope: "checagem mecanica + semantica: 5/5 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 9 secoes, 170 linhas; drift R13/R14: 1 achados resolvidos (decisoes D1-D4 A / SKILL_REF)"
reviewed-by: R15 (claude-sonnet; decisoes D1-D4 A)
reviewed: 2026-10-04
---
# Skill: Ralph Loop

## Propósito
Executar tarefas de desenvolvimento de longa duração (>30 min, múltiplas features) de forma autônoma, usando arquitetura Planner → Generator → Evaluator com context resets para evitar context anxiety e self-evaluation bias.

---

## Quando NÃO usar

- **Tarefa <30 min ou 1 domínio** — loop de longa duração não paga; executar direto.
- **Trabalho sem iterações de feedback** (script único, ingest mecânica) — autonomous-loop é para refinamento contínuo.
- **Sessão interativa curta** — o loop assume autonomia prolongada; em sessão guiada, fazer passo a passo.
- **Sem critério de done definido** — loop sem parada declarada vira laço infinito; definir antes.

Disambiguation: `autonomous-loop` é a tarefa de desenvolvimento longa (>30 min) com iterações; `subagent-team` paraleliza domínios independentes; `adversarial-gate` valida tarefas durante a execução — autonomous-loop executa, não valida. `plan-handoff` escreve o plano e o contrato EXEC que o loop consome; não escreve plano aqui dentro.


## Condições de Ativação
Ative esta skill quando:
- A tarefa envolver construção de aplicação completa a partir de 1–4 frases de prompt
- O build estimado for >30 min ou >5 features
- A tarefa envolver múltiplas sessions de coding (long-running)

NÃO ative para: features isoladas já especificadas (use `spec-lifecycle`); hotfixes; tarefas <15 min.

---

## Perfil de modelo

Perfil `standard` — Planner/Generator/Evaluator sao execucao bounded com verifier a cada sprint
(model-routing §Padrao custo-efetivo; model-catalog §Perfis).
Esta skill nao mantem pins locais por etapa.

> Escalada de capacidade so depois de 3+ sprints consecutivos falharem o
> Evaluator — falha repetida e a evidencia nova que a Hard Rule 2 exige
> (1 hop, nunca antes do gate rodar).
## Protocolo de Execução

### AGENTE 1 — Planner
**Input**: prompt de 1–4 frases do usuário
**Output**: `progress.md` com spec completa

Instruções:
- Seja **ambicioso no escopo** — a spec deve superar o que um agente solo produziria
- Foque em: deliverables e contexto de produto (NÃO detalhes técnicos de implementação)
- Inclua: features principais, user stories, critérios de aceitação
- Identifique oportunidades para integrar features de AI/agente no produto
- Carregue e aplique `dev/frontend-implementation` se o produto tiver UI

### AGENTE 2 — Generator
**Loop por sprint** (ou sessão contínua com compaction se modelo suportar):

**PRÉ-SPRINT — Sprint Contract**:
- Generator propõe: o que será construído + como será verificado
- Evaluator revisa a proposta (confirma alinhamento com spec)
- Iterate até acordo antes de escrever código

**BUILD**:
- Trabalhe feature por feature seguindo a spec
- Use git para versionamento a cada sprint
- Ao final de cada feature: self-evaluate antes de chamar o QA

**CONTEXT RESET** *(fallback — apenas modelos sem compaction nativa)*:
- Escreva `handoff.md`: estado atual, features completas, próximos passos, bugs conhecidos
- Reset do contexto + carregamento de `handoff.md` no início da nova sessão
- **Skip se usando Opus 4.6+ ou Sonnet 4.6+** — compaction automática substitui este passo

### AGENTE 3 — Evaluator/QA
**Critérios de avaliação** (cada um com threshold mínimo):
1. **Funcionalidade** (threshold: 8/10) — features do sprint contract funcionam?
2. **Design/UX** (threshold: 7/10) — interface é utilizável e coerente?
3. **Qualidade de Código** (threshold: 7/10) — código limpo, sem dead code?
4. **Profundidade de Produto** (threshold: 7/10) — vai além do mínimo viável?

**Instruções críticas para o Evaluator**:
- Use Playwright MCP para INTERAGIR com o app — não avalie por screenshots estáticos
- Seja **cético por padrão** — Claude tende a aprovar trabalho medíocre
- Teste edge cases, não apenas happy paths
- Se identificar um bug: seja específico sobre localização (arquivo, linha, condição)
- PROIBIDO: identificar um problema e depois concluir "não é crítico" sem justificativa forte

Se qualquer critério abaixo do threshold → SPRINT FAIL → Generator recebe feedback e refaz.

### AGENTE 2.5 — Cleanup Sweep *(simplify-code)*

Após Evaluator aprovar o sprint (score ≥ threshold), antes do próximo Sprint Contract:

1. Carregar `simplify-code` — **skill arquivada** em `08-ARCHIVE/system/agents/skills-dup-2026-07/simplify-code/SKILL.md`, sem substituto vivo. Sem ela, aplicar os 3 eixos abaixo manualmente sobre `git diff sprint_<N-1>..sprint_<N>`
2. 3 reviewers paralelos acham issues estruturais que o Evaluator não cobre:
   - **Code Reuse** — duplicação que acumula entre sprints
   - **Code Quality** — débito técnico que passing tests não detectam
   - **Efficiency** — N+1 e hot-path bloat que escapa do QA funcional
3. Aplicar apenas SAFE fixes (auto-aplicáveis sem risco de quebrar comportamento)
4. CAREFUL e RISKY findings → adicionar ao `qa-reports/qa_<N>.md` como debt para o próximo sprint
5. Re-run test suite para confirmar que SAFE fixes não quebraram nada

**Quando pular o Cleanup Sweep:**
- Sprint gerou <50 linhas de diff → custo de 3 subagentes > ganho
- Evaluator encontrou bugs (SPRINT FAIL) → cleanup é desperdício, refazer primeiro
- Último sprint do projeto → cleanup vai para handoff/final review, não entre sprints

**Custo-benefício:** 3 subagentes por sprint é caro. Para projetos curtos (<3 sprints), rodar apenas no sprint final. Para projetos longos (5+ sprints), rodar a cada 2-3 sprints para controlar acúmulo de débito.

---

## Artefatos de Saída
- `progress.md` — spec expandida pelo Planner
- `handoff.md` — estado de sessão para context reset
- `sprint-contracts/sprint_<N>.md` — contratos negociados
- `qa-reports/qa_<N>.md` — relatórios do Evaluator
- Codebase completo com git history

---

## Completion

- [ ] Planner gerou `progress.md` com spec completa (features, user stories, critérios de aceitação)
- [ ] Cada sprint teve Sprint Contract negociado (Generator + Evaluator alinhados antes do build)
- [ ] Evaluator usou Playwright MCP (interação real, não screenshots estáticos)
- [ ] Cleanup Sweep (simplify-code) executado entre sprints aprovados (ou skip justificado)
- [ ] Todos os critérios de avaliação ≥ threshold (Funcionalidade 8/10, Design 7/10, Código 7/10, Produto 7/10)
- [ ] Codebase com git history a cada sprint
- [ ] Se 10+ rounds de QA sem convergir: pausou e relatou ao usuário

## Failure modes

> **Failure policy é obrigatória em todo loop.** Sem ela, Claude improvisa quando algo dá errado — é onde loops criam problemas. Ver how-to-create-loops-claude-code · getting-started-with-loops-anthropic

- **Premature approval**: Evaluator aprova sprint com feature central não funcionando → proibido, feature central = FAIL automático
- **Sprint contract drift**: Generator ignora o contract e constrói outra coisa → contract é lei para o sprint
- **Static evaluation**: Evaluator avalia por screenshots sem interagir com o app → usar Playwright MCP, testar edge cases
- **Opus no Planner**: usar Opus para expansão de prompt → desperdício, Planner é Haiku (template work)
- **simplify-code em sprint pequeno**: rodar 3 subagentes para <50 linhas de diff → desperdício, skip
- **Relatório como done**: Turno que termina só com texto é relatório, não é done. Se a checklist tiver item aberto e nenhum bloqueio declarado, mande uma continuação que nomeia os itens abertos. Máximo de 3 continuações por tarefa; depois disso, pare e registre (ADR-NX-012: Opus 5.5 tende a encerrar o turno com relatório).

---

## Restrições
- NUNCA o Evaluator aprova um sprint onde "a feature central não funciona"
- NUNCA o Generator ignora o sprint contract — ele é lei para aquele sprint
- NUNCA o Generator altera testes, critérios do Evaluator ou métrica para passar — o contrato do sprint declara o que é intocável; alterar isso = fraude, reprova o sprint
- NUNCA use Opus para o Planner (desperdício — é trabalho de template)
- Se o build atingir 10+ rounds de QA sem convergir: pause, relate ao usuário, solicite spec simplificação
