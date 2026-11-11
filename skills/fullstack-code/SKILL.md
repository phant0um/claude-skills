---
kind: skill-proc
resolver-status: exposed
type: skill
name: fullstack-code
input:
  required_fields: [task]
output:
  format: json|md
triggers:
  positive:
    - "revisar migration"
    - "revisar query"
    - "review que atravessa a stack"
  negative:
    - "implementar feature"
    - "teste exploratório"
    - "auditoria de segurança"
allowed_effects:
  - write 06-GENERATED/
  - read 04-SYSTEM/
forbidden_effects:
  - modify agent files
  - modify manifest
  - external-publish
version: 1.0.0
source_agent: forge-fullstack
status: active
created: 2026-08-20
description: "Use when: revisar mudança que atravessa a stack, e especialmente migration ou query de banco — veredito SAFE/RISKY/DANGEROUS. Rubrica 5E vem de code-optimize; implementar feature vai para as skills de camada."
updated: 2026-10-25
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "2026-10-25: conferido contra disco com revisao shield (opus, somente leitura). Corrigidos: Maestro citado como ativo (aposentado 2026-09-25); simplify-code dado como sem substituto vivo (existe no plugin michel); rota da secao Quando NAO usar mandava revisao para test-probing (scanner de seguranca) em vez de code-optimize/code-review; Cleanup aplicava fixes no codigo revisado sem o frontmatter declarar escrita, agora so propoe o diff; allowed_effects sem 03-RESOURCES (o corpo nunca escreve la); referencia a '5 fases' que o merge de 2026-08-31 removeu; Test generation apontava complexity-ratchet (modo de codebase-design, nao gerador) e agora aponta tdd; texto 'restaurado, nao reescrito' trocado por 'adaptado'. Conferido ok: proveniencia forge.md @ 6304e261b, perfil deep no model-catalog, wikilinks, codenames, M1-M4/Q1-Q8 e SAFE/RISKY/DANGEROUS nas references, sdd.md. NAO conferido: conteudo tecnico de migrations (lock Postgres, alembic), evals/."
---

# fullstack-code — review que atravessa a stack

> **Proveniência:** procedimento transplantado de `04-SYSTEM/automation/agents/fullstack-agent-system/forge.md` @ `6304e261b` (fatia S1 do plano-refino-automation, 2026-08-23). Adaptado depois do transplante (modelo atualizado pelo ADR-NX-012, rotas e efeitos). `source_agent` do frontmatter preservado.

# Forge — Senior Code Quality Engineer (material transplantado)

> **O que esta skill é.** Revisão de qualidade de mudança que atravessa a
> stack, com o **review de banco** (migration e query) como material próprio.
> Não implementa feature: o corpo transplantado do Forge diz literalmente
> *"Never implements features — only improves existing code"*, e isso continua
> valendo. Para construir, use as skills de camada — `backend-implementation`,
> `frontend-implementation`, `infra-implementation`, `data-ai-implementation` —
> ou a cadeia de dev.
>
> A rubrica 5E foi **fundida em** [code-optimize](../code-optimize/SKILL.md) (2026-08-31), que já era a versão
> mais desenvolvida — Fowler smells, dois eixos paralelos, Deep Modules. Esta
> skill deixou de manter uma segunda cópia e aponta para lá.
>
> **Codenames.** Stratum = `04-SYSTEM/automation/skills/dev/backend-implementation/SKILL` · Facet =
> `04-SYSTEM/automation/skills/dev/frontend-implementation/SKILL` · Bastion = `04-SYSTEM/automation/skills/dev/infra-implementation/SKILL` ·
> Neuron = `04-SYSTEM/automation/skills/dev/data-ai-implementation/SKILL` · Sentinel =
> `04-SYSTEM/automation/skills/security/fullstack-security-audit/SKILL`. Decompor trabalho de dev é
> dev.

## Purpose

Specializes in code quality optimization. Reviews any deliverable from Stratum, Facet, or Neuron against the **5E rubric** (binary gates, BinEval — no 0–100 score), emits a **SHIP | REFACTOR** verdict, identifies actionable findings per dimension, and optionally delivers a refactored version. Never implements features — only improves existing code.

> Perfil `deep` (claude-opus-5-5 · medium, model-catalog): quality review é análise técnica profunda. Opus/critical reservado para threat modeling (Sentinel) e orquestração complexa (o agente Maestro foi aposentado em 2026-09-25, ADR-004-retired-agents).

---

## Rubrica 5E — mora em `code-optimize`

Gates 5E, blocking vs non-blocking, override por `REVIEWS.md` e veredito SHIP | REFACTOR são de [code-optimize](../code-optimize/SKILL.md). **Carregue-a para revisar código de aplicação.** Esta skill cobre só o review de banco (abaixo).

## DB Migration Review

Gatilho: arquivo de migration no diff (padrões: `migrations/*.sql`, `alembic/versions/*.py`, `prisma/migrations/*.sql`, `db/migrate/*.rb`, `*.up.sql` + `*.down.sql`), OU quando user explicitamente pede "review migration".

Gatilho bateu → leia [migration-review](references/migration-review.md) e rode M1–M4 com veredito próprio SAFE | RISKY | DANGEROUS, em paralelo à rubrica 5E de code-optimize. Sem gatilho → skip silencioso.

---

## DB Query Review

Gatilho: diff contém SQL de query (não migration), OU Prisma `schema.prisma` com `query`/`select`/`where`, OU quando user pede "review queries".

Gatilho bateu → leia [query-review](references/query-review.md) e rode Q1–Q8 com veredito próprio SAFE | RISKY | DANGEROUS. Query Review é on-demand.

---

## Output Format

Para código de aplicação, o formato de saída (tabela por dimensão, findings com
linha, versão refatorada) é o de [code-optimize](../code-optimize/SKILL.md) §PASSO 5. Migration e Query Review têm
formato próprio, nas references dos ponteiros acima.

## Cleanup Phase — simplify-code integration

Se verdict REFACTOR ou houver blocking finding:

1. Carregar `simplify-code` (versão viva em `04-SYSTEM/automation/skills/dev/simplify-code/SKILL.md`, com `disable-model-invocation: true`: só o usuário a invoca; sem ela, aplicar os 3 eixos manualmente. Cópia antiga em `08-ARCHIVE/system/agents/skills-dup-2026-07/simplify-code/SKILL.md`). Reviewers: Reuse → economicidade, Quality → fluência + efetividade, Efficiency → eficiência (N+1, hot paths, TOCTOU).
2. Escopo = diff avaliado, não o codebase. Agregue os findings com os do veredito 5E.
3. **Proponha** os fixes por risk tier SAFE → CAREFUL → RISKY, como diff no relatório. Esta skill não escreve no código revisado (ver `allowed_effects`); quem aplica é a skill de camada (backend-, frontend-, data-ai- ou infra-implementation), com confirmação do usuário para RISKY.
4. Entregue o veredito final e o diff proposto; a skill de camada re-roda linter e testes dos arquivos tocados.

**Não rodar:** SHIP com 0 findings; mudança trivial (typo, rename único; custo de 3 subagentes > ganho); user pediu "só diagnóstico".

---

## Fora do Escopo

- Security vulnerabilities (→ Sentinel)
- Feature implementation (→ `backend-implementation` / `frontend-implementation` / **SDD**)
- Infrastructure config (→ Bastion)
- ML pipeline quality (→ Neuron + Forge for non-ML code)
- Test generation (→ `04-SYSTEM/automation/skills/dev/tdd/SKILL.md`)
- DB query optimization (→ Query Review phases Q1-Q8 acima)
- Orquestração de implementação multi-task (→ **SDD** — `04-SYSTEM/automation/skills/orchestration/subagent-team/sdd.md`)

## Critério de Qualidade

- Critério de sucesso: cada Migration e Query Review emite veredito SAFE | RISKY | DANGEROUS, com tabela e volume de linhas nomeados.
- Cada finding referencia arquivo e linha; recomendação marcada [pre] / [fix] / [post]
- Review de código de aplicação usa a rubrica de [code-optimize](../code-optimize/SKILL.md), sem cópia local
- Veredito DANGEROUS bloqueia até existir plano alternativo

## Exemplos

**Input:** "Review this Express route handler — 80 lines, no error handling, SQL concat"
**Output:** Veredito: REFACTOR — Eficácia FAIL (blocking: 3 uncaught exceptions, SQL injection linha 22), Economicidade FAIL (non-blocking: duplicate auth logic), Efetividade FAIL (blocking: SRP violation — handler does DB + business logic + formatting). 2 blocking → REFACTOR. Refactored version delivered.

**Input:** "executar `fullstack-code` — review migration — alembic/versions/0042_add_user_status.py"
**Output:** Veredito: SHIP (5 dimensões PASS, SQL limpo). Migration Review: MIGRATION DANGEROUS — M1: `ALTER TABLE users ADD COLUMN status VARCHAR(20) NOT NULL` sem DEFAULT em tabela com 2M rows (table lock + data loss se falhar). M2: `downgrade()` só faz `drop_column('status')` — irreversível sem backup. M3: sem `SET lock_timeout`. Recomendações: [pre] `pg_dump users > backup.sql`, [pre] `SELECT count(*) FROM users` para verificar, [fix] adicionar `server_default='pending'` + backfill em batches de 10k. Migration Verdict: DANGEROUS — bloquear até plano alternativo.

## Quando NÃO usar

- Revisão 5E de código de aplicação → `code-optimize`; diff de PR → `code-review`; validar tarefa concluída → `adversarial-gate`.
- Auditoria de vulnerabilidades → `fullstack-security-audit` (classe de risco própria).

## Condições de falha

- Invalid input → stop, don't invent
- Missing resources → warning, don't create

## Completion

- [ ] Itens de `## Critério de Qualidade` atendidos.
- [ ] Veredito SAFE | RISKY | DANGEROUS emitido para cada Migration e Query Review.

## Failure modes

- **Migration sem rollback testado**: aprovar sem plano de volta → DANGEROUS bloqueia até haver plano.
- **Query julgada sem `EXPLAIN`**: "parece lento" como finding → rode o `EXPLAIN` antes de julgar.
- **Trade-off documentado penalizado**: tratar desnormalização deliberada como defeito → respeite a decisão registrada.
- **Veredito sem tabela e volume**: migration julgada sem nomear tabela e nº de linhas → nomeie os dois.
- **Rubrica 5E copiada**: duplicar a rubrica aqui → carregue `code-optimize`.
