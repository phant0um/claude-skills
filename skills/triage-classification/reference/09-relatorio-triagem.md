---
status: active
parent: "[triage-classification](../SKILL.md)"
kind: reference
name: triage-classification-09-relatorio
type: skill-reference
updated: 2026-10-11
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 após mover o formato do relatório verbatim do SKILL.md (W1 do plano context-engineering-claude5); verify.sh lost_unexpected=0; ponteiro do passo 6 resolve"
---

> Formato do relatório F1 de [triage-classification](../SKILL.md). Carregar no passo 6 (gerar relatório).

```markdown

## Decisão Individual (todos analisados)

| Arquivo | Decisão | Motivo | Interest |
|---------|---------|--------|----------|
| `<path>` | approved | <motivo> | core |
| `<path>` | disapproved | dup | — |
| `<path>` | disapproved | junk (<sinal>) | — |

## Aprovados para Ingest

| Arquivo | Interest | Domínio | Destaque |
|---------|----------|---------|----------|
| `<path>` | core | ai-agents | <1 linha> |
| `<path>` | off | articles ou ambiguous | <1 linha — captura leve/parada segura> |

## Descartados (08-ARCHIVE/disapproved/)

| Arquivo | Motivo |
|---------|--------|
| `<path>` | dup |
| `<path>` | junk (<sinal>) |

## Sugestões de Complementos no Vault (rascunho — caveman ultra)
- complementa: [arquivo] → Y

## Melhorias Identificadas no Vault (rascunho — caveman ultra)
- concept-candidate: `<nome>` (N arquivos)
- entity-candidate: `<nome>` (X, Y)
- skill-candidate: `<nome>` (N arquivos)
- hook-candidate: `<nome>`
- agent-candidate: `<nome>`

> Flags 1-linha, sem prosa/justificativa — versão refinada/priorizada com
> wikilinks fica em `ingest-diario-*.md` F3.2/F3.3 (`report-synthesis`).

## Estatísticas
- Total analisado: N
- Approved: X (core: a, adjacent: b, off: c)
- Disapproved: Y (dup: d, junk: e)
- Taxa de aprovação: Z%
- Domínio dominante: <domínio>
```
