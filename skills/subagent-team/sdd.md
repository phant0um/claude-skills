---
type: reference
status: active
kind: reference
name: sdd
description: "Spec do MODO REVIEW POR TASK (sdd) de [subagent-team](SKILL.md). Não é skill invocável. Subagent-Driven Development: fresh subagent per task + task review (spec + quality) + broad final review. Meio termo entre subagent-team (paralelo sem review) e autonomous-loop (heavy com context resets)."
version: 1.0.0
author: Nexus Agent System (adapted from obra/superpowers)
tags: [subagent, development, review, parallel, delegation, workflow]
updated: 2026-08-09
parent: 04-SYSTEM/automation/skills/orchestration/subagent-team/SKILL.md
mode: "REVIEW POR TASK (sdd)"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 13 secoes, 267 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Diferença vs skills relacionadas](#diferença-vs-skills-relacionadas)
- [Protocolo de Execução](#protocolo-de-execução)
- [Model Selection](#model-selection)
- [Continuous Execution](#continuous-execution)
- [Progress Ledger](#progress-ledger)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Restrições](#restrições)
- [Related](#related)

> **Não é skill invocável.** MODO REVIEW POR TASK (sdd) de [subagent-team](SKILL.md) — carregado por ela, não resolvido pelo router.



# Skill: SDD — Subagent-Driven Development

## Propósito

Executar planos de implementação com tasks independentes usando subagentes frescos por task, review estruturado por task (spec + qualidade), e review final broad. Mantém contexto do orquestrador limpo para coordenação.

**Princípio:** Fresh subagent per task + task review + broad final review = alta qualidade, iteração rápida, sem context pollution.

---

## Condições de Ativação

Ative esta skill quando:
- Você tem um plano de implementação com tasks independentes
- Tasks são majoritariamente independentes (podem ser paralelizáveis)
- Quer ficar na sessão atual (sem context switch)
- Feature development em projetos reais (pdf2md, plataforma juridica, brasfoot, social-rss)

NÃO ative para:
- Tasks com dependências complexas sequenciais (use `spec-lifecycle`)
- Projetos longos >30 min com múltiplas features (use `autonomous-loop`)
- Hotfixes isolados (execute direto)
- Tarefas <15 min

---

## Diferença vs skills relacionadas

| Skill | Quando | Context | Review |
|-------|--------|---------|--------|
| `sdd` | Feature development, tasks independentes | Mesma sessão, subagent fresco por task | Review por task + final broad |
| `autonomous-loop` | Projetos longos, múltiplas features | Context resets entre sprints | Sprint contract + Evaluator |
| `subagent-team` | Múltiplas perspectivas simultâneas | Paralelo, sem review por task | Sem review estruturado |
| `spec-lifecycle` | Spec → tasks → implement | Sequencial, spec-driven | Spec verify antes de implement |

---

## Protocolo de Execução

### PASSO 0 — Pre-Flight Plan Review

Antes de dispatchar Task 1, scanear o plano uma vez buscando conflitos:
- Tasks que se contradizem ou violam Global Constraints
- Qualquer coisa que o plano mandates que a rubrica de review trata como defect

Apresentar todos findings como **uma pergunta batched** — cada finding ao lado do texto do plano que o mandates, perguntando qual governa — antes de começar execução. Se scan limpo, prosseguir sem comentário.

### PASSO 1 — Ler plano, criar todos

1. Ler plano completo
2. Notar contexto e Global Constraints
3. Criar `todo` list com todas as tasks
4. Identificar dependências entre tasks (se houver)

### PASSO 2 — Por task: dispatch implementer

Usar `delegate_task` para cada task:

```
delegate_task(
    goal="[prompt do implementer com spec completa da task + contexto do projeto]",
    context="[contexto necessário: file paths, convenções, stack, test cmd]",
    toolsets=["terminal", "file"]
)
```

**Construir o prompt do implementer:**
- Spec completa da task (não assumir que subagent sabe o que você sabe)
- File paths exatos que devem ser tocados
- Convenções do projeto (naming, style, test framework)
- Comando de teste do projeto
- "Implemente, teste, commit. Self-review antes de reportar DONE."

**Status handling:**

| Status | Ação |
|--------|------|
| **DONE** | Gerar review package, dispatch task reviewer |
| **DONE_WITH_CONCERNS** | Ler concerns. Correção/scope → resolver antes de review. Observação → nota e prosseguir |
| **NEEDS_CONTEXT** | Fornecer contexto faltante, re-dispatch |
| **BLOCKED** | (1) contexto → dar mais contexto, mesmo modelo; (2) reasoning → modelo mais capaz; (3) task grande → quebrar menor; (4) plano errado → escalar para humano |

> **Nunca** ignore escalation ou force mesmo modelo a retry sem mudanças.

### PASSO 3 — Por task: dispatch task reviewer

Após implementer reportar DONE, dispatch reviewer:

```
delegate_task(
    goal="[prompt do reviewer: review diff da task contra spec + qualidade]",
    context="[spec da task + diff output]",
    toolsets=["terminal", "file"]
)
```

**Reviewer verifica 2 dimensões:**
1. **Spec compliance** — implementação matcha spec da task?
2. **Code quality** — naming, structure, DRY, error handling, test coverage

**Reviewer output:**
```json
{
  "spec_review": "PASS|FAIL",
  "quality_findings": [
    {"severity": "Critical|Important|Minor", "file": "path", "line": N, "issue": "...", "fix": "..."}
  ],
  "verdict": "APPROVE|FIX_REQUIRED|REJECT"
}
```

**Se reviewer reporta issues:**
- Critical/Important → dispatch fix subagent com findings → re-review
- Minor → nota e prossegue
- ⚠️ Cannot verify from diff → resolver orquestrador antes de marcar complete

### PASSO 4 — Marcar task complete

Após reviewer APPROVE:
1. Marcar task como complete no `todo`
2. Append ao progress ledger: `Task N: DONE (reviewer: APPROVE, N findings minor)`
3. Próxima task

### PASSO 5 — Após todas as tasks: broad final review

Dispatch final code reviewer com diff de todas as tasks:

```
delegate_task(
    goal="[review completo do branch diff: security, lógica, integração entre tasks, edge cases]",
    context="[diff completo do branch + spec original]",
    toolsets=["terminal", "file", "search"]
)
```

**Final reviewer verifica:**
- Integração entre tasks (uma task quebra outra?)
- Edge cases cross-task (input de task A afeta task B?)
- Security scan (complementar ao `requesting-code-review`)
- Overall code quality (não só por-task, mas holística)

### PASSO 6 — Finish

Usar `finishing-a-development-branch` (se disponível) ou:
1. Re-run test suite completo
2. Lint/type check
3. Commit final com `[sdd-verified]` prefix
4. Reportar summary: N tasks, N reviews, N fixes, verdict final

---

## Model Selection

| Task Type | Model Tier |
|-----------|-----------|
| Mechanical (1-2 files, spec completa) | Fast/cheap model |
| Integration (multi-file, debugging) | Standard model |
| Architecture & design | Most capable model |
| Final broad review | Most capable available (não session default) |
| Review tasks | Scale to diff size, complexity, risk |

> **Turn count > token price.** Modelos baratos tomam 2-3x mais turns em multi-step work — custam mais overall. Use mid-tier como floor para reviewers e implementers de prose descriptions.

> **Sempre especificar modelo explicitamente no delegate_task.** Modelo omitido herda session model (geralmente o mais caro).

---

## Continuous Execution

- **Não pausar para check-in entre tasks.** Executar todas sem parar.
- Únicas razões para parar: BLOCKED que você não resolve, ambiguidade que impede progresso, ou todas completas.
- `"Should I continue?"` prompts e progress summaries waste time — execute.
- Entre tool calls, narrar no máximo 1 linha curta — o ledger e tool results carregam o registro.

---

## Progress Ledger

Manter ledger inline (não arquivo separado para sessão única):

```markdown
## SDD Progress — $(date -I)

| Task | Implementer | Reviewer | Fixes | Status |
|------|-------------|----------|-------|--------|
| 1 | DONE | APPROVE | 0 | ✅ |
| 2 | DONE | FIX_REQUIRED→APPROVE | 2 | ✅ |
| 3 | BLOCKED→DONE | APPROVE | 1 | ✅ |
| 4 | DONE | REJECT→re-implement | — | 🔄 |
```

---

## Completion

- [ ] Pre-flight plan review executado (conflitos resolvidos antes de começar)
- [ ] Todas as tasks dispatchadas com spec completa (não assumir contexto do subagent)
- [ ] Cada task passou por reviewer (spec compliance + quality)
- [ ] Critical/Important findings do reviewer foram corrigidos e re-reviewd
- [ ] ⚠️ Cannot verify items resolvidos pelo orquestrador
- [ ] Broad final review executado no diff completo do branch
- [ ] Test suite completo + lint/type check passing
- [ ] Commit final com `[sdd-verified]` prefix

## Failure modes

- **Context inheritance**: subagent herda contexto da sessão em vez de receber spec isolada → prompt do implementer está incompleto
- **Skip review**: marcar task DONE sem reviewer → não tem garantia de qualidade
- **Same model retry**: BLOCKED → re-dispatch com mesmo modelo sem mudanças → algo precisa mudar
- **HEAD~1 review package**: usar `HEAD~1` no diff → silently drops commits de multi-commit task. Usar `BASE..HEAD`
- **No final review**: pular broad review → integration bugs entre tasks não detectados
- **Pause between tasks**: "should I continue?" → waste de tempo, execute continuamente

---

## Restrições

- NUNCA dispatch subagent sem spec completa — subagent não sabe o que você sabe
- NUNCA pule o reviewer de uma task — review é o ponto
- NUNCA use `HEAD~1` para diff — usa `BASE..HEAD` para capturar todos commits
- NUNCA marque task DONE sem reviewer APPROVE
- NUNCA force retry sem mudanças quando implementer reporta BLOCKED

---

## Related

- `autonomous-loop` — versão heavy para projetos longos
- `subagent-team` — versão sem review estruturado
- `spec-lifecycle` — spec-driven sequencial
- `requesting-code-review` — pre-commit gate (complementar ao final review)
- `simplify-code` — cleanup pass (pode rodar após SDD complete); **arquivada** em `08-ARCHIVE/system/agents/skills-dup-2026-07/simplify-code/SKILL.md`, sem substituto vivo