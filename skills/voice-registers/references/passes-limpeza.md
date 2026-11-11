---
name: voice-registers-passes-limpeza
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/content/voice-registers/SKILL.md
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Itens 1-19 citados nao conferidos um a um contra o SKILL."
---

## Passes de limpeza (só com autorização explícita)

Ordem fixa — nunca pule, cada passe re-lê o texto inteiro:

1. Cortar throat-clearing e hedges vazios (itens 2, 5) — remoção pura, zero risco de mudar sentido.
2. Reescrever colon reveals e falsos grupos de três (6, 7) — colapse mantendo o dado.
3. Substituir palavras-banidas pela palavra concreta (3) — cada troca conferida com a frase inteira.
4. Cortar importance puffery e repetição de tese (4, 8) — manter só a primeira tese + dados novos.
5. Reestruturar seção genérica (9) — realocar peso para o ponto com mais evidência; nunca inventar conteúdo para equilibrar.
6. **Re-verificar** (regression check): rode o Procedimento inteiro no texto limpo. Zero ocorrências dos itens 1–19, zero fatos sem fonte, `voice-lint` sem `error` = done.
