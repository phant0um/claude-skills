---
name: ingest-verify-modelo-por-etapa
kind: reference
type: skill
status: active
parent: "[ingest-verify](../SKILL.md)"
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Etapas C6 e C7 existem em ingest-verify/SKILL.md:107,117. Aberto: a tabela manda Haiku ler source page (conteudo derivado de clipping); finder.md:45-48 aplica a HR1 a esse tipo de conteudo. Nao decidido aqui; o SKILL usa Haiku em C11 (:169)."
---

## Modelo por etapa — ingest-verify

| Etapa | Modelo | Justificativa |
|-------|--------|---------------|
| Frontmatter parse (bash) | — | Zero tokens |
| Wikilink resolution (bash) | — | Zero tokens |
| Manifest check (bash/python) | — | Zero tokens |
| Tese central check | Haiku | Julgamento simples — 1 pergunta Y/N |
| Relatório final | Haiku | Estruturação de findings |
| C6 Concept absorption (bash) | — | Zero tokens |
| C7 Personal reflection (bash) | — | Zero tokens |
