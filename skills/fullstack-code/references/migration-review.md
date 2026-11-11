---
name: fullstack-code-migration-review
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/dev/fullstack-code/SKILL
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Afirmacoes tecnicas de SQL (locks, CONCURRENTLY, DDL transacional) lidas, nao verificadas contra documentacao de PostgreSQL/MySQL."
---

# DB Migration Review — referência de fullstack-code

### FASE M1 — Schema Safety *(deep)*

Check:
- **Table locking** — `ALTER TABLE` em tabela com milhões de rows sem `ALGORITHM=INPLACE, LOCK=NONE` (MySQL) ou sem `SET lock_timeout` (PostgreSQL)
- **Data loss** — `DROP COLUMN`, `DROP TABLE`, `ALTER COLUMN ... TYPE` que pode truncar dados, `NOT NULL` sem `DEFAULT` em tabela populada
- **Index creation** — `CREATE INDEX` sem `CONCURRENTLY` (PostgreSQL) bloqueia writes; sem `ALGORITHM=INPLACE` (MySQL) bloqueia tabela
- **Constraint addition** — `ADD CONSTRAINT FOREIGN KEY` sem verificação de dados existentes (pode falhar mid-migration deixando schema inconsistente)
- **Sequence/serial changes** — alterar `SERIAL`/`AUTOINCREMENT` sem recalcular max(id) pode causar PK collision

### FASE M2 — Rollback Safety *(deep)*

Check:
- **Rollback script existe** — para cada `*.up.sql` há `*.down.sql`? Para Alembic, `downgrade()` não é vazio?
- **Rollback é reversível** — `DROP TABLE` no up não pode ser revertido sem backup de dados. `TRUNCATE` é irreversível.
- **Idempotência** — rodar migration duas vezes falha graciosamente ou quebra o schema?
- **Transactional safety** — migration está dentro de `BEGIN/COMMIT`? (PostgreSQL DDL é transacional; MySQL não é — precisa de estratégia diferente)
- **Partial failure recovery** — se migration quebra no meio, schema fica em estado válido? (ex: criar tabela antes de criar FK que referencia ela)

### FASE M3 — Performance Impact *(deep)*

Check:
- **Full table scan** — migration roda `UPDATE` sem `WHERE` em tabela grande (lock + downtime)
- **Backfill strategy** — adicionar `NOT NULL` column sem default em tabela populada exige backfill; está no plano?
- **Index bloat** — criar 3+ índices simultaneamente sem `CREATE INDEX CONCURRENTLY` paralisa writes por muito mais tempo que criar sequencial
- **Connection timeout** — migration longa sem `SET statement_timeout` pode ser morta pelo LB mid-way deixando schema inconsistente (MySQL non-transactional DDL)
- **Disk space** — `ALTER TABLE` que reescreve tabela (MySQL) precisa de espaço temporário igual ao tamanho da tabela — verificar se há espaço livre

### FASE M4 — Data Integrity *(deep)*

Check:
- **FK violations** — adicionar FK sem verificar se dados existentes satisfazem a constraint (`SET foreign_key_checks=0` e depois descobrir dados órfãos)
- **Unique constraint** — adicionar `UNIQUE` em coluna com duplicatas existentes → falha na migration
- **Enum changes** — alterar enum removendo valor em uso quebra queries existentes que referenciam o valor removido
- **Default values** — `DEFAULT` novo faz sentido para todos os rows existentes? (ex: `DEFAULT false` em coluna `is_active` desativa todos os usuários)
- **Cascading** — `ON DELETE CASCADE` novo pode apagar dados não intencionais em produção

### Migration Verdict

Além do veredito 5E, a migration recebe verdict próprio:

| Verdict | Condição | Ação |
|---------|----------|------|
| **MIGRATION SAFE** | 0 findings em M1-M4 | Pode aplicar em produção |
| **MIGRATION RISKY** | 1-3 findings, nenhum CRITICAL | Aplicar com janela de manutenção, rollback pronto |
| **MIGRATION DANGEROUS** | Qualquer CRITICAL em M1/M2 | **BLOQUEAR** — requer plano de migração alternativo |

**Critical findings** (bloqueiam produção automaticamente):
- Data loss sem backup explícito
- Table lock em tabela de produção sem janela de manutenção
- Rollback inexistente ou irreversível
- FK/Unique constraint sem verificação prévia de dados

### Migration Output Format

```markdown
## Migration Review: <filename>

| Phase | Findings | Critical |
|-------|----------|----------|
| M1 — Schema Safety | N | Y/N |
| M2 — Rollback Safety | N | Y/N |
| M3 — Performance | N | Y/N |
| M4 — Data Integrity | N | Y/N |

### Critical Findings
- [M1] Line X: `<issue>` → Risk: `<consequence>` → Fix: `<safe alternative>`

### Recommendations
- [pre-migration] Backup command
- [pre-migration] Data verification query
- [during] Lock/timeout strategy
- [post-migration] Verification query
- [rollback] Down procedure

## Migration Verdict: SAFE | RISKY | DANGEROUS
```

### Quando NÃO rodar Migration Review
- Diff não contém arquivos de migration → skip silencioso
- Migration é nova tabela em DB vazio → sem dados para perder, skip M2/M4
- Migration é `CREATE DATABASE` ouDDL administrativo → fora do escopo

