---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: spec-lifecycle
skill: spec-lifecycle
version: 1.0
author: Nexus Agent System
tags: [spec, planning, tasks, implementation, spec-driven]
updated: 2026-11-10
description: "Use when: executar o ciclo completo de Spec-Driven Development: constitution → specify → clarify → plan → tasks → implement, garantindo que código emerja de especificações executáveis e não de vibe-coding. Diferente de [decisions](../decisions/SKILL.md) (registro pontual de decisão) — spec-lifecycle é o pipeline de spec→code."
consolidated-by: R3 (absorveu spec-verify, prd-grade, spec, verify como modos)
reads: []
writes: []
triggers:
  positive:
    - "ciclo completo de spec-driven development"
    - "constitution → specify → clarify → plan → tasks"
    - "/spec-lifecycle"
  negative:
    - "código sem spec"
    - "spec já implementada"
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7: corpo completo lido pelo shield (opus, somente leitura); W7a: pins de modelo removidos, escalada via model-routing; checks frontmatter/lint/evals verdes; 192 linhas, 11 secoes"
---
# Skill: Spec Lifecycle

## Propósito
Executar o ciclo completo de Spec-Driven Development: constitution → specify → clarify → plan → tasks → implement, garantindo que código emerja de especificações executáveis e não de vibe-coding.

---

## Quando NÃO usar

- **Task <3 arquivos ou lógica trivial** — spec é overhead; implementar direto.
- **Fix de bug já diagnosticado** — teste de regressão + fix; spec não adiciona.
- **Protótipo/exploração** — protótipo não quer spec; `prototype`.
- **Modo absorvido já ativo** — spec-lifecycle carrega modos (VERIFICAR etc.); não empilhar com invocação direta do modo.

Disambiguation: `spec-lifecycle` governa o ciclo completo (spec → implement → verify); `spec-verify` é o MODO VERIFICAR (carregado por ela); `tdd` executa implementação test-first — lifecycle orquestra, modos executam. Spec pronta que vai para OUTRO modelo executar em ondas: `plan-handoff` escreve o plano e o contrato EXEC.


## Condições de Ativação
Ative esta skill quando:
- O usuário solicitar `@spec [feature]` ou `especificar [feature]`
- Uma nova feature for solicitada sem spec formal existente
- Um PR for aberto sem spec correspondente em `.specify/specs/`

NÃO ative para: hotfixes urgentes (<10 linhas); mudanças de configuração pura; refatorações sem mudança de comportamento observável.

---

## Perfil de modelo

Perfil `deep` — Specify e Plan sao decisao de produto e arquitetura; erro ali propaga por todas
as fases seguintes do ciclo
(model-routing §Padrao custo-efetivo; model-catalog §Perfis).
Esta skill nao mantem pins locais por etapa.

## Protocolo de Execução

1. FASE 0: criar a constitution se não existir; depois dela, todas as fases a respeitam.
2. FASE 1 e 1.5: specify (spec.md com acceptance criteria) e identificar test seams.
3. FASE 2: clarify, resolvendo ambiguidades com o usuário antes da spec.
4. FASE 3 e 4: plan e tasks, com tarefas mapeadas 1:1 para os acceptance criteria.
5. FASE 5: implementar seguindo tasks.md, sem escopo novo sem atualizar a spec.
6. FASE 6: verify-report.md checando cada acceptance criteria.

### FASE 0 — Constitution
- Se `.specify/memory/constitution.md` não existir, crie agora <!-- drift:ok: caminho de outro projeto -->
- Inclua: princípios de qualidade de código, padrões de teste, consistência de UX, requisitos de performance
- Uma vez criada, a constitution é lei — todas as fases seguintes devem respeitá-la

### FASE 1 — Specify
- Peça ao usuário: "Descreva O QUÊ e POR QUÊ — não a stack técnica"
- **Sintetizar conversa existente** (de to-spec): NÃO entrevistar se contexto já existe — sintetizar o que já foi discutido
- Gere `.specify/specs/<id>-<feature>/spec.md` com: user stories, critérios de aceitação, restrições
- Deixe em branco: stack, arquitetura, implementação

### FASE 1.5 — Identify Test Seams

> **Leading word: seam.** Ponto onde você testa. O fewer seams, melhor — ideal é 1.

- Sketch dos seams onde a feature será testada
- Preferir seams existentes a novos
- Usar o seam mais alto possível (highest seam = testa mais behavior com menos setup)
- Se novos seams são necessários, propô-los no ponto mais alto
- Confirmar com user que seams match expectations

### FASE 2 — Clarify
- Execute perguntas estruturadas sequenciais baseadas nos gaps da spec
- Registre respostas na seção `## Clarifications` do spec.md
- PARE quando: todas as user stories tiverem critérios de aceitação verificáveis

### FASE 3 — Plan
- Agora incorpore stack técnica e arquitetura
- Gere: `plan.md`, `data-model.md`, `api-spec.json` (se aplicável)
- Inclua: research.md para bibliotecas/frameworks recentes (pesquise versões via web search MCP)
- **AUDITORIA**: re-leia o plano procurando: over-engineering, dependências desnecessárias, violações da constitution

**Tabela de fatos verificados.** Antes de propor solução, o plan lista os fatos
de que ela depende, numerados (F1, F2…). Cada fato traz evidência: `path:linha`
lido nesta sessão ou PoC rodado. Fato sem evidência vira `[hyp]` e bloqueia a
decisão que depende dele. Fonte: Octop.

### FASE 4 — Tasks
- Quebre o plano em tasks atômicas com:
  - Dependências explícitas (A → B → C)
  - Marcadores de paralelismo `[P]` onde aplicável
  - File paths exatos de destino
  - Tasks de teste ANTES das tasks de implementação (TDD)
  - Checkpoints de validação a cada user story
- Salve em `tasks.md`

### FASE 5 — Implement
- Valide pré-requisitos: constitution ✓, spec ✓, plan ✓, tasks ✓
- Execute tasks em ordem respeitando dependências, no loop de [implement](../implement/SKILL.md) (TDD, typecheck, review)
- Ao final de cada user story: self-evaluate antes de avançar
- Se uma task falhar 3x consecutivas: escale para o perfil de raciocínio mais forte da policy model-routing nessa task específica

### FASE 6 — Verify
- Compare implementação contra spec.md e acceptance criteria
- Para cada critério: PASS / FAIL / PARTIAL
- Se qualquer FAIL: retorne ao FASE 5 com feedback específico
- Gere `verify-report.md`

> **Vocabulário de drift (P0):** findings da FASE 6 (Verify) usam a taxonomia specification-drift D1–D16 (rastreabilidade D1–D7, code-compliance D8–D10, test-compliance D11–D13, integração D14–D16) — ver [drift-review](../drift-review/SKILL.md). Na FASE 1–2, rotular toda premissa/ambiguidade como `ASSUMPTION: <n>` — `load-bearing` (validar antes do Implement) ou `deferred` (registrar dono). Spec sem ASSUMPTION label falha o Verify; D5 (assumption drift) é o finding clássico de spec envelhecida.

---

## Artefatos de Saída
```
.specify/
  memory/constitution.md
  specs/<id>-<feature>/
    spec.md
    plan.md
    tasks.md
    data-model.md     (se aplicável)
    api-spec.json     (se aplicável)
    research.md       (se libs novas)
    verify-report.md  (pós-impl.)
```

---

**Critério de sucesso:** cada acceptance criteria checado em verify-report.md e tasks.md mapeando 1:1 para eles.

## Completion

- [ ] Fase Clarify: ambiguidades resolvidas com usuário antes de spec
- [ ] Fase Specify: spec.md com acceptance criteria + data-model + api-spec (se aplicável)
- [ ] Fase Plan: tasks.md com tarefas que mapeiam 1:1 para acceptance criteria
- [ ] Fase Implement: código segue tasks.md (sem escopo expandido sem update)
- [ ] Fase Verify: verify-report.md com cada acceptance criteria checado
- [ ] Estrutura .specify/ criada com memory/constitution.md

## Failure modes

- **Skip Clarify**: pular direto para Specify → ambiguidade vira bug na implementação
- **Code before tasks**: escrever código antes de tasks.md aprovado → sem plano, escopo creep
- **Constitution drift**: modificar constitution.md durante feature → abrir issue separada

---

## Restrições
- NUNCA pule a fase Clarify — ambiguidade na spec vira bug na implementação
- NUNCA escreva código antes de ter tasks.md aprovado
- NUNCA modifique constitution.md durante uma feature — abra issue separada

---

## Related

- **SDD** ([sdd](../subagent-team/sdd.md)) — executa as tasks geradas por spec-lifecycle com subagentes frescos por task + review estruturado. Spec-lifecycle produz o plano; SDD executa.
- **autonomous-loop** ([autonomous-loop](../autonomous-loop/SKILL.md)) — versão heavy para projetos longos (>30 min, múltiplas features). Use SDD para features isoladas; autonomous-loop para builds completos.
- **plan** (skill do scheduler legado) — authoring do plano markdown. Spec-lifecycle é mais completo (constitution → specify → clarify → plan → tasks → implement).
- **complexity-ratchet** ([complexity-ratchet](../codebase-design/complexity-ratchet.md)) — ratchet de testes após implementação.


## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO VERIFICAR** — [spec-verify](spec-verify.md)
- **MODO GRADEAR** — [prd-grade](prd-grade.md)
- **MODO GATE DE PLANEJAMENTO (rotina)** — spec
- **MODO GATE PÓS-IMPLEMENTAÇÃO (rotina)** — verify

