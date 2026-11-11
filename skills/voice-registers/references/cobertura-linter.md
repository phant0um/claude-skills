---
name: voice-registers-cobertura-linter
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/content/voice-registers/SKILL.md
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. test-voice-lint-planted.py existe e passa 22/22 hoje; o texto cita 20/20 em 2026-09-24 (data da medicao, mantida). Contagens do corpus (921, 1843, 2173) sao medicoes datadas, nao refeitas."
---

## Cobertura do linter

`voice-lint.py` cobre só o mecânico. `error` = léxico de hype, abertura
proibida, tweet 1 gordo, não-imperativo em C. `warn` = A3, A2, A5b, B3, C4, C7 —
tem lastro grande no corpus (A3: 921/921 concepts sem o bloco em 2026-08-09),
então reprovar por eles produziria número que ninguém lê. A1, A4, B2, B6, C2 e
C5 exigem leitura e ficam fora do script de propósito — são desta skill.

Casos plantados: `04-SYSTEM/scripts/test-voice-lint-planted.py` (20/20 em
2026-09-24). Um deles prova que A3 **desaparece** quando o bloco entra — regra
com backlog total passaria por "detectada" mesmo travada em FAIL.

**Modo externo** (arquivo fora do vault ou `type: external`): liga `EN-hype`
(error), `EN-vague`, `EN-slop` e `GEN` (warn) e desliga A6. Fica fora dos
arquivos do vault de propósito. Ligado neles, somaria warn em 1843 arquivos
(`EN-vague`) e 2173 (`GEN`), medido em 2026-09-24. Tradução entre aspas
(não-invenção 4) e fato de memória (não-invenção 6) não têm detector: são do
passe de fatos.
