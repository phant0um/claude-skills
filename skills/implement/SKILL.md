---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: implement
description: "Use when: implementar trabalho descrito em PRD ou issues prontos para código — /tdd em seams pré-acordados, typecheck e /review ao final."
skill: implement
version: 1.0
author: Nexus Agent System
source: mattpocock/skills (implement)
trigger: ['/implement', '@implement']
effort: low
tags: [implementation, prd, issues, tdd, review, commit]
updated: 2026-10-13
reads: []
writes:
  - 06-GENERATED/tasks/lessons.md
triggers:
  positive:
    - "/implement"
    - "@implement"
    - "PRD ou issues prontos para implementação"
  negative:
    - "protótipo throwaway"
    - "spike sem spec"
    - "hotfix <10 linhas com causa confirmada"
consumes: ["prd", "issues"]
tools: []
references:
  - 04-SYSTEM/automation/skills/dev/tdd/SKILL.md
  - 04-SYSTEM/automation/skills/meta/spec-lifecycle/SKILL.md
  - 04-SYSTEM/automation/skills/meta/spec-lifecycle/spec-verify
verifier: ["Require typecheck pass, suite completo green e /review ao final."]
human_gate: true
reviewed-scope: "checagem mecanica + semantica: 9/9 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 9 secoes, 147 linhas; drift R13/R14: 2 achados resolvidos (decisoes D1-D4 A / SKILL_REF)"
reviewed-by: R15 (claude-sonnet; decisoes D1-D4 A)
reviewed: 2026-10-04
---


# Skill: Implement

## Propósito

Implementar trabalho descrito em PRD ou issues. Ultra-lean: usa /tdd onde possível, roda typecheck regularmente, suite completo no final, /review, commit.

---

## Condições de Ativação

Ative quando:
- PRD ou issues existem e precisam ser implementados
- `/implement` chamado explicitamente
- Após `to-tickets` ou `to-spec` gerarem artifacts

NÃO ative para: protótipos (→ /prototype); spikes sem spec; hotfixes <10 linhas.

---

## Protocolo

### 1. Ler PRD/issues
- Identificar scope, acceptance criteria, seams de teste
- Ler GLOSSARY.md (se existir) para vocabulário de domínio
- Respeitar ADRs na área tocada

### 2. Implementar com TDD
- Usar `/tdd` em seams pre-acordados com user
- Vertical slices: 1 teste → 1 impl → repeat
- Rodar typecheck regularmente (a cada 2-3 tasks)
- Rodar single test file regularmente

### 3. Full test suite
- Rodar suite completo 1× no final
- Zero regressões permitidas
- Se regressão: fix antes de prosseguir

### 4. Review
- Rodar `/review` ou `@verify` no trabalho
- Addressar findings antes de commit

### 5. Commit
- Commit no branch atual, um commit atômico por fatia verde (teste + typecheck passando). Cada commit é save point: `git revert <sha>` sozinho desfaz a fatia sem quebrar o resto.
- Fatia incompleta que precisa entrar antes de terminar fica atrás de flag desligada por default; registre no commit quando remover a flag.
- Mensagem diz o porquê da fatia, não a lista de arquivos.
- Mensagem descritiva com referência ao PRD/issue

Porquê: commit grande mistura fatias e transforma rollback em cirurgia manual.

### 6. Model swap no handoff (multi-modelo)
Se rodar em harness que troca modelo por fase (Devin CLI, Kilo Code, sub-agentes): use **modelo forte na geração** (implementar slice) e **modelo rápido/barato no handoff** (resumir estado, escrever handoff doc — tarefa mecânica). Padrão de campo: GLM/Opus p/ implementar → SWE-fast/Haiku p/ handoff. Ver model-router p/ tiers.

---

## Completion

- [ ] PRD/issues lidos e scope confirmado
- [ ] TDD aplicado nos seams pre-acordados
- [ ] Typecheck passa
- [ ] Full test suite passa (zero regressões)
- [ ] /review executado, findings addressados
- [ ] Commits atômicos por fatia verde, cada um revertível sozinho

## Failure modes

- **TDD skip**: implementar sem testes em seams acordados → sempre usar /tdd nos seams
- **Suite skip**: não rodar full suite no final → regressões invisíveis
- **Review skip**: commitar sem /review → quality gate bypassed
- **Scope creep**: implementar além do PRD/issue → sem spec update = drift

---

## Self-Improvement

Após cada execução:
1. Se regressão encontrada no suite final → registrar padrão em `06-GENERATED/tasks/lessons.md`
2. Se scope creep detectado → flag para @harden com contexto
3. Lições append: `- YYYY-MM-DD: [implement] N tasks, M testes, regressões=X`

> Ver: [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop

---

## Restrições

- NUNCA implementar sem ler PRD/issues primeiro
- NUNCA pular full test suite no final
- NUNCA commitar sem /review
- NUNCA expandir scope sem atualizar spec/PRD

---

## Quando NÃO usar

- **Protótipos throwaway** — usar `dev/prototype`; implement não persiste.
- **Spike sem spec** — experimento para validar abordagem é `dev/prototype`, não implementação.
- **Hotfix <10 linhas com causa confirmada** — implement é overhead; corrigir direto com teste de regressão.
- **PRD/issues ausentes** — implement sem spec é chute; voltar para `meta/spec-lifecycle`.

Disambiguation: `dev/implement` executa trabalho especificado; `dev/tdd` é o modo test-first usado por implement nos seams; `spec-verify` fecha o loop verificando o resultado contra a spec — implement não é verificação.

## Relacionado

- [tdd](../tdd/SKILL.md) — TDD para seams pre-acordados
- [spec-lifecycle](../spec-lifecycle/SKILL.md) — spec completa antes de implement
- [spec-verify](../spec-lifecycle/spec-verify.md) — verify contra spec
- [code-optimize](../code-optimize/SKILL.md) — review pós-implementação
- [codebase-design](../codebase-design/SKILL.md) — vocabulário de módulo/seam ao desenhar código novo
- [domain-modeling](../domain-modeling/SKILL.md) — GLOSSARY.md (o "Ler GLOSSARY.md" do step 1)
