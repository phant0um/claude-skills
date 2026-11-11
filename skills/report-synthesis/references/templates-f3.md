---
status: active
parent: "[report-synthesis](../SKILL.md)"
kind: reference
name: report-synthesis-templates-f3
type: skill-reference
updated: 2026-10-11
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 após mover blocos verbatim do SKILL.md (W2 do plano report-synthesis-progressive-disclosure); verify.sh lost_unexpected=0; 5 âncoras citadas pelo SKILL.md conferidas contra os headings"
---

> Templates e scripts-especificação de [report-synthesis](../SKILL.md). O Nexus materializa; esta skill não escreve. Carregar quando a fase citada pedir.

## F3.3 Vault Impact — tabela

Tabela de impacto:

| Melhoria | Prioridade | Esforço | Status | Fonte |
|----------|-----------|---------|--------|-------|
| Skill: `<nome>` | alta/média/baixa | horas/dias | pendente | `source` |
| Agent: `<nome>` | alta/média/baixa | horas/dias | pendente | `source` |
| Hook: `<nome>` | alta/média/baixa | horas/dias | pendente | `source` |
| Concept: `<nome>` | alta/média/baixa | horas/dias | pendente | `source` |
| Entity: `<nome>` | alta/média/baixa | horas/dias | pendente | `source` |

**Prioridade:** alta = bloqueia vault saudável · média = nice-to-have · baixa = backlog
**Status:** pendente · em-progresso · done

## F3.9 Hot por domínio — script

```bash
DOMAIN="$1"      # domínio dominante do run (campo `dominios` do triagem)
RESUMO="$2"      # síntese 1-linha de F3.1-F3.3
HOT_DOMAIN="04-SYSTEM/system/state/context/hot-${DOMAIN}.md"

if [[ -f "$HOT_DOMAIN" ]]; then
  echo "- $(date -I): ${RESUMO} → ingest-diario-$(date -I)" >> "$HOT_DOMAIN"
  echo "- $(date -I): hot-${DOMAIN} atualizado — ${RESUMO}" >> 04-SYSTEM/system/state/context/hot.md
else
  echo "- $(date -I): ${RESUMO} → ingest-diario-$(date -I)" >> 04-SYSTEM/system/state/context/hot.md
fi
```

## Notas de Execução

- O que foi feito neste ciclo (triagem → ingest → report)
- Gargalos encontrados (arquivos duplicados, manifest corrompido, Ollama timeout)
- Decisões tomadas autonomamente (quais skills/agents criar)
- Pendências para próxima sessão

## F3.5 — append do veredito em hot.md

```bash
{
  echo ""
  echo "## Pipeline Diário $(date -I)"
  echo "**Veredito:** $VERDICT"
  echo "**Triagem:** $TRIAGEM_STATS"
  echo "**Ingest:** $INGEST_STATS"
  echo "**Top action:** $TOP_ACTION"
  echo "→ ingest-diario-$(date -I)"
} >> 04-SYSTEM/system/state/context/hot.md
```

## Output — frontmatter do relatório

Frontmatter:
```yaml
---
title: Ingest Diário <DATA>
type: report
period: YYYY-MM-DD
sources_analyzed: N
clusters: N
generated_by: report-synthesis
created: YYYY-MM-DD
verdict: PIPELINE OK | PIPELINE FAIL
---
```

## Exemplo

**Input:** "executar `report-synthesis` — fechar pipeline diário 2026-06-09"
**Output:** "Relatório gerado: 14 sources em 3 clusters (RAG patterns, MCP integrations, FIAP MVC). 4 contradições detectadas. 6 melhorias vault: 2 skills alta prioridade, 1 hook, 3 concepts. Veredito: PIPELINE OK. hot.md atualizado. `audit-logging` disparado → commit abc1234."
