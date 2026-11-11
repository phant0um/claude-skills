---
status: active
kind: reference
name: spec-verify
version: 1.0
type: skill
author: Nexus Agent System
created: 2026-05-28
tags: [verification, spec-driven, quality-gate, acceptance-criteria, pre-implementation]
updated: 2026-08-09
description: "Spec do MODO VERIFICAR de [spec-lifecycle](SKILL.md). Não é skill invocável. @spec-verify [task-description] — Força especificação explícita antes de implementação. Claude escreve spec → verifica próprio output contra spec → reporta desvios. Reduz retrabalho ao detectar divergência earl"
parent: "[spec-lifecycle](SKILL.md)"
mode: "VERIFICAR"
consolidated-by: R3
consumes: ["task-description"]
tools: []
references:
  - 04-SYSTEM/automation/skills/meta/spec-lifecycle/SKILL.md
verifier: ["Require spec escrita antes do código e relatório de desvios contra acceptance criteria."]
human_gate: true
reads: []
reviewed-scope: "checagem mecanica + semantica: 4/4 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 14 secoes, 143 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Trigger](#trigger)
- [Protocol](#protocol)
- [Casos de Uso no Vault](#casos-de-uso-no-vault)
- [Reforços obrigatórios de spec (P0)](#reforços-obrigatórios-de-spec-p0)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Quando NÃO usar](#quando-não-usar)
- [Fontes](#fontes)

> **Não é skill invocável.** MODO VERIFICAR de [spec-lifecycle](SKILL.md) — carregado por ela, não resolvido pelo router.




# Skill: Spec Verify

## Propósito

Força especificação explícita antes de implementação. Claude escreve spec → verifica próprio output contra spec → reporta desvios. Reduz retrabalho ao detectar divergência early (1 linha de spec vs reverter 40 arquivos).

> *"Plan is cheap to fix. Code across 40 files is not."* — @0xCodez

## Trigger

Usar antes de qualquer task com 3+ arquivos ou lógica não-trivial:
- Implementações de features novas
- Refactors com mudança de interface
- Ingest de fontes complexas (FIAP PDFs, papers)
- Criação de agentes ou skills

## Protocol

### Step 1 — Escrever Spec (antes de qualquer código/edição)

```
Spec para: [nome da task]
Data: YYYY-MM-DD

## O que vai mudar
- [arquivo/componente]: [mudança esperada]

## Acceptance criteria
- [ ] [critério verificável 1]
- [ ] [critério verificável 2]

## Não vai mudar (out of scope)
- [item explicitamente fora do escopo]

## Definition of Done
[Uma frase descrevendo o estado final verificável]
```

### Step 2 — Implementar

Executar com spec visível. Não expandir escopo sem atualizar spec.

### Step 3 — Verificar contra spec

Após implementação:
- Checar cada acceptance criteria: `✓` / `✗` / `parcial`
- Listar desvios com razão
- Se desvio crítico: reverter ou atualizar spec + re-aprovar

### Step 4 — Reportar

```
Spec-verify resultado:
✓ [critério 1]
✓ [critério 2]
✗ [critério 3] — motivo: [razão]; ação: [fix / aceito / descartado]
```

## Casos de Uso no Vault

| Task | Spec mínima |
|------|-------------|
| Ingest FIAP PDF | Tese central, conceitos-chave, frontmatter completo, links para entities |
| Criar agente | Identity, triggers, capabilities, guardrails, output format |
| Refactor de skill | O que muda, o que não muda, exemplos de input→output |
| Reorganização vault | Quais paths mudam, quais wikilinks precisam update, backup antes |

## Reforços obrigatórios de spec (P0)

- **ASSUMPTION label:** toda premissa ou ambiguidade vira linha `ASSUMPTION: <n> — <premissa>` na spec. Classificar como `load-bearing` (se falsa, muda arquitetura — validar antes de implementar) ou `deferred` (postergável — registrar dono e prazo). Spec sem ASSUMPTION label é spec incompleta; não avançar ao Step 2.
- **Reference-value table:** para cada acceptance criteria com valores, anexar tabela de referência (valores aceitos vs rejeitados, um caso por linha). Conformance é verificada valor a valor contra a tabela — nunca contra impressão geral do output.
- **Gate de auditabilidade:** regra de negócio que só vive no código é regra que ninguém audita. Toda regra nova exige entrada na spec (ou ADR) antes do merge — sem spec, sem merge.

## Completion

- [ ] Spec escrita antes de qualquer código ( acceptance criteria + out of scope + Definition of Done)
- [ ] Implementação executada com spec visível (sem escopo expandido sem update)
- [ ] Step 3 verificação: cada acceptance criteria checado (✓/✗/parcial)
- [ ] Desvios críticos: revertidos ou spec atualizada + re-aprovada
- [ ] Spec-verify report entregue com status por critério

## Failure modes

- **Spec after code**: escrever spec depois de implementar → spec vira racionalização, não plano
- **Scope creep silencioso**: expandir escopo sem atualizar spec → desvio não rastreado
- **Vague acceptance criteria**: "funciona" sem condição verificável → não distingue done de not-done

---

## Quando NÃO usar

- **Task <3 arquivos ou lógica trivial** — spec é overhead; implementar direto com testes.
- **Fix de bug já diagnosticado com causa confirmada** — escrever teste de regressão e corrigir; spec não adiciona.
- **Tarefa exploratória/protótipo** — protótipo não quer acceptance criteria; `dev/prototype`.
- **Invocações automáticas** (cron/background) — spec-verify é modo interativo; sem operador para validar a spec, não aplica.

Disambiguation: `spec-verify` é o MODO VERIFICAR de `meta/spec-lifecycle` — carregado por ela, não invocável pelo router; `dev/tdd` verifica comportamento via teste, `reason-judge` pontua qualidade por rubrica — nenhum substitui verificação contra spec.

## Fontes

- claude-code-10-techniques-master — técnica 6 (spec-driven development)
