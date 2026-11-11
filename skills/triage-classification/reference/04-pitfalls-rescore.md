---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-04-pitfalls-rescore
type: skill-reference
updated: 2026-07-16
reviewed-scope: "W3c 2026-10-10: 15 pitfalls podados (batch_score.py/escala A-D/Hermes ausentes; detectores cobertos por rotina-daily-scan.sh e test-pre-ingest-dedup.sh); 4 restantes"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [macOS `declare -A` failure (bash 3.x) — 2026-06-23](#macos-declare--a-failure-bash-3x-2026-06-23)
- [`wc -l` padding breaks grep verification (macOS)](#wc--l-padding-breaks-grep-verification-macos)
- [Pitfall: "Design Loops" not recognized as "loop engineering" (2026-06-30)](#pitfall-design-loops-not-recognized-as-loop-engineering-2026-06-30)
- [Pitfall: Subagent manifest update failure — 2026-06-24](#pitfall-subagent-manifest-update-failure-2026-06-24)


> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: pitfalls de rescore/approval rate (macOS declare-A, drift, inflação).

## macOS `declare -A` failure (bash 3.x) — 2026-06-23

macOS ships bash 3.x which does NOT support `declare -A` (associative arrays).
Any scoring script using `declare -A` will fail silently with:

```
declare: -A: invalid option
```

**Fix**: Use Python for any scoring that needs associative arrays or complex
data structures. Bash 3.x is fine for simple `[[ ]]` regex tests and integer
arithmetic, but anything beyond that should be Python.

```python
# Instead of bash declare -A, use Python dict:
keywords = {'agent': 1, 'llm': 1, 'claude': 1, ...}
matches = sum(1 for kw in keywords if kw in content.lower())
```

## `wc -l` padding breaks grep verification (macOS)

macOS `wc -l` outputs leading whitespace (e.g. `       0` instead of `0`).
When interpolated into strings via `$(wc -l < file)`, the padding creates
unexpected spaces that break regex grep patterns.

**Exemplo (pipeline-semanal self-improvement log):**
```bash
# BROKEN on macOS — wc -l padding creates spaces that break the regex
echo "- $(date -I): [pipeline-semanal] $NEW_COUNT candidatos, $(wc -l < file) aprovados, $VERDICT" >> lessons.md
grep -q "pipeline-semanal.*$(date -I)" lessons.md  # FAILS — extra spaces in line
```

**Fix**: always pipe `wc -l` through `tr -d ' '`:
```bash
COUNT=$(wc -l < file | tr -d ' ')
echo "- $(date -I): [pipeline-semanal] $NEW_COUNT candidatos, $COUNT aprovados, $VERDICT" >> lessons.md
grep -q "pipeline-semanal.*$(date -I)" lessons.md  # WORKS
```

**Alternativa**: usar `grep -qF` (fixed-string) ao invés de regex para verificação
quando o conteúdo exato da linha é conhecido.

---

## Pitfall: "Design Loops" not recognized as "loop engineering" (2026-06-30)

**Sintoma**: "Stop Writing Prompts. Design Loops That Make AI Iterate Until It's Right."
pontuou 3 apesar de ser core loop engineering. Heurística só matchava "loop engineering"
exato, não sinônimos como "design loops" ou "loops that make AI iterate".

**Fix aplicado**: TITLE_POSITIVE pattern expandido:
`loop engineering|autonomous loop|agent loop|design loop|loops that make ai`

**Lição**: sinônimos de core obsessions precisam ser listados explicitamente.
A heurística é literal — não infere semelhança semântica.

## Pitfall: Subagent manifest update failure — 2026-06-24

**Sintoma**: 40 arquivos ingeridos por subagente mas manifest não atualizado (0 entries
novas). Subagente reportou "manifest updated" mas verificação mostrou 0 entries.

**Causa**: subagente usou formato de key diferente (path completo vs basename) e/ou
falhou ao executar o jq/Python de manifest update sem reportar erro.

**Fix**: após cada batch de subagente, verificar manifest:
```python
today_count = sum(1 for k,v in manifest['sources'].items()
                  if isinstance(v,dict) and v.get('ingested_at') == TODAY)
expected = len(batch) * 2  # with + without .md extension
if today_count < expected:
    # Run fix script
    python3 /tmp/fix_manifest.py
```

**Prevenção**: instruir subagentes explicitamente a usar basename (não path completo)
como key do manifest. Validar manifest após cada subagente completar, não apenas
no final do pipeline.
