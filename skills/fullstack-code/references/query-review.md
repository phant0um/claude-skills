---
name: fullstack-code-query-review
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/dev/fullstack-code/SKILL
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Afirmacoes tecnicas de SQL (RLS, auth.role(), CTE materializada em PostgreSQL <=12) lidas, nao verificadas contra documentacao."
---

# DB Query Review — referência de fullstack-code

## Contents

Q1–Q8 (Performance, Connection, Security & RLS, Schema, Concurrency, Data Access, Monitoring, Advanced) · Query Verdict · Query Output Format · Quando NÃO rodar.

### 8 Categorias (priorizadas por impacto)

### FASE Q1 — Query Performance [CRITICAL] *(deep)*

Check:
- **Missing indexes** — `WHERE`, `JOIN`, `ORDER BY` em colunas sem índice → full table scan
- **N+1 queries** — loop que executa query por iteração em vez de batch (`SELECT ... WHERE id = ?` dentro de for)
- **Partial indexes** — índice que cobre subset da query mas não a condição principal
- **SELECT \*** — ler todas as colunas quando precisa de 2-3 (waste de I/O + memory)
- **OR conditions** — `WHERE a = 1 OR b = 2` impede uso de índice composto → UNION ALL ou índices separados
- **LIKE com prefixo wildcard** — `LIKE '%term%'` não usa índice (full scan); `LIKE 'term%'` usa

### FASE Q2 — Connection Management [CRITICAL] *(deep)*

Check:
- **Connection leaks** — conexão aberta e nunca fechada (missing `connection.close()`, `finally` sem cleanup)
- **Pool sizing** — pool de conexões subdimensionado para concorrência esperada
- **Long-running transactions** — transação que segura conexão por >30s sem necessidade
- **Connection per request** — pattern que abre conexão nova para cada request em vez de pool

### FASE Q3 — Security & RLS [CRITICAL] *(deep)*

Check:
- **RLS policies** — tabela com dados de usuário sem Row-Level Security → qualquer query acessa todos os rows
- **SECURITY DEFINER** — função com `SECURITY DEFINER` bypassa RLS — verificar se necessário e se grants são mínimos
- **BOLA/IDOR** — query que acessa objeto por ID sem verificar ownership (`SELECT * FROM orders WHERE id = ?` sem `AND user_id = ?`)
- **SQL injection** — query construída por concatenação de string em vez de parameterized query
- **auth.role() deprecation** — uso de `auth.role()` (deprecated) em vez de `auth.uid()`

### FASE Q4 — Schema Design [HIGH] *(deep)*

Check:
- **Normalization level** — 3NF violado sem justificativa (denormalização para performance é OK se documentada)
- **Foreign key without index** — FK sem índice na coluna referenciada → join lento
- **Enum vs lookup table** — enum para valores que mudam frequentemente (migration cara) vs lookup table
- **UUID vs SERIAL** — UUID como PK sem índice → insert mais lento que SERIAL

### FASE Q5 — Concurrency & Locking [MEDIUM-HIGH] *(deep)*

Check:
- **Lock ordering** — queries que lockam múltiplas tabelas em ordem inconsistente → deadlock
- **SELECT FOR UPDATE** — lock pessimista onde optimistic concurrency suffice (version column + WHERE)
- **Long transactions** — transação que segura lock por >5s bloqueando outras operações
- **Advisory locks** — uso de advisory locks sem timeout → lock infinito

### FASE Q6 — Data Access Patterns [MEDIUM] *(deep)*

Check:
- **Pagination** — `OFFSET N LIMIT M` em tabela grande (skip cada vez mais rows) → cursor-based pagination
- **Aggregation in app** — `SELECT *` + count/sum no código em vez de `SELECT COUNT(*)` no DB
- **Repeated queries** — mesma query executada múltiplas vezes na mesma request → cache
- **Eager loading** — `SELECT *` + join quando só precisa de 1 tabela → lazy load

### FASE Q7 — Monitoring & Diagnostics [LOW-MEDIUM] *(deep)*

Check:
- **Missing EXPLAIN** — query crítica sem verificação de query plan (não sabe se usa índice)
- **No slow query log** — threshold de slow query não configurado (pg_stat_statements)
- **Blind spots** — tabelas críticas sem índice de monitoramento
- **No query timeout** — query sem `SET statement_timeout` → pode rodar indefinidamente

### FASE Q8 — Advanced Features [LOW] *(deep)*

Check:
- **CTE vs subquery** — CTE materializada quando subquery inline seria mais eficiente (PostgreSQL ≤12)
- **Window functions** — window function usada onde aggregate simples suffice
- **JSONB vs columns** — JSONB para dados que são queried frequentemente (sem índice GIN) → columns
- **Materialized views** — materialized view sem refresh strategy → dados stale

### Query Verdict

| Verdict | Condição | Ação |
|---------|----------|------|
| **QUERIES SAFE** | 0 findings Q1-Q3, Q4-Q8 minor | Pode ir para produção |
| **QUERIES RISKY** | 1-3 findings, nenhum CRITICAL em Q1-Q3 | Otimizar antes de produção, pode deploy com monitoramento |
| **QUERIES DANGEROUS** | Qualquer CRITICAL em Q1-Q3 (N+1, SQL injection, BOLA) | **BLOQUEAR** — corrigir antes |

**Critical findings** (bloqueiam):
- SQL injection
- BOLA/IDOR sem ownership check
- N+1 em hot path (lista, dashboard, API pública)
- RLS ausente em tabela com dados multi-tenant

### Query Output Format

```markdown
## Query Review: <filename>

| Phase | Category | Findings | Critical |
|-------|----------|----------|----------|
| Q1 | Query Performance | N | Y/N |
| Q2 | Connection Mgmt | N | Y/N |
| Q3 | Security & RLS | N | Y/N |
| Q4 | Schema Design | N | Y/N |
| Q5 | Concurrency | N | Y/N |
| Q6 | Data Access | N | Y/N |
| Q7 | Monitoring | N | Y/N |
| Q8 | Advanced | N | Y/N |

### Critical Findings
- [Q1] Line X: `<issue>` → Fix: `<optimized query>`

### Recommendations
- [index] `CREATE INDEX CONCURRENTLY idx_<name> ON <table>(<col>)`
- [RLS] `ALTER TABLE <t> ENABLE ROW LEVEL SECURITY`
- [query] Replace N+1 with: `<batch query>`

## Query Verdict: SAFE | RISKY | DANGEROUS
```

### Quando NÃO rodar Query Review
- Diff não contém SQL/ORM queries → skip
- Query é migration DDL (Migration Review cobre) → skip Q-phases, M-phases rodam
- DB é SQLite local sem concorrência → skip Q2 (connection mgmt) e Q5 (concurrency)

