---
status: active
parent: "[ingest-verify](SKILL.md)"
kind: reference
name: batch-enrichment-pipeline
type: reference
updated: 2026-07-06
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 8 secoes, 146 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [When to Use](#when-to-use)
- [Operations](#operations)
- [Script](#script)
- [Performance](#performance)
- [Integration with Pipeline Semanal](#integration-with-pipeline-semanal)
- [Pitfalls](#pitfalls)
- [Session Validation (2026-06-28)](#session-validation-2026-06-28)



# Batch Enrichment Pipeline

Programmatic decision assignment, Tese/Resumo generation, and Links creation
for source pages. Zero AI calls. Validated at scale: 1685 files decided,
1788 sections generated, 2491/2491 pages → 100% completeness.

> Modelo binário v2.1 (BinEval): `decision: approved|disapproved`, sem escala A/B/C/D
> (o campo `score:` foi removido; `migrate_grade_to_decision.py` migrou 3479 files).
> `batch_enrich --assign-decision` (alias legado `--assign-grades`). Só dup/junk viram
> `disapproved`. Ver migration-triagem-binary.

## When to Use

- Post-ingest: after batch ingest creates source pages without decision/sections
- Vault audit: when discovering files missing structural sections
- Pre-verify: run before `ingest-verify` to fix programmatic issues first

## Operations

### 1. Decision Assignment

2-tier heuristic for files without `decision:` frontmatter (binary — approved unless junk):

| Tier | Signal | Rule |
|------|--------|------|
| 1 | word_count / spam signals (G2) | `<100 words` OR spam/ads/clickbait → `disapproved`; else `approved` |
| 2 | Content heuristics | Has Tese/Resumo/Links OR >500 chars → `approved`; empty/boilerplate-only → `disapproved` |

`interest` (core|adjacent|off) é atribuído em paralelo por keyword match — **roteia**
profundidade, não descarta. Validated: 1682 files decided (≈97% approved sob binário —
por isso o sinal de alto valor virou o gate `reflect: true`, não o tier).

### 2. Bold Tese Fix

Recurring formatting issue: `**Tese central**:` (bold text) instead of
`## Tese Central` (proper heading). Pattern:

```python
patterns = [
    (r'\*\*Tese central\*\*:\s*', '## Tese Central\n\n'),
    (r'\*\*Tese Central\*\*:\s*', '## Tese Central\n\n'),
    (r'\*\*Tese\*\*:\s*', '## Tese Central\n\n'),
]
```

### 3. Tese Generation

For files with no Tese Central (not even bold): extract first 2 sentences
of content body (after frontmatter, skipping headings). Insert as
`## Tese Central` after frontmatter.

### 4. Resumo Generation

For files with Tese Central but no Resumo: take first 3 sentences of Tese
Central text. Insert `## Resumo` section immediately after Tese Central.

```python
tese_match = re.search(r'^## Tese[^\n]*\n+(.+?)(?=\n##|\Z)', content, re.MULTILINE | re.DOTALL)
sentences = re.split(r'(?<=[.!?])\s+', tese_text)
resumo_text = ' '.join(sentences[:3])
```

### 5. Links Generation

For files with no concept/entity wikilinks: match file tags against concept
tag index. Build `tag → concept_stem` mapping from concept frontmatter.
Insert top 3 matches as `## Links` section.

Fallback: substring matching (`tag.lower() in stem.lower()`, `len(tag) > 3`).
Final fallback: category-based default concepts.

## Script

`scripts/batch_enrich.py` — CLI with `--all` flag or individual operations.

```bash
python3 04-SYSTEM/scripts/batch_enrich.py --all
# or
python3 04-SYSTEM/scripts/batch_enrich.py --assign-decision --fix-bold-tese
```

## Performance

| Operation | Files | Time | AI calls |
|-----------|-------|------|----------|
| Decision assignment | 1682 | 2.8s | 0 |
| Bold Tese fix | 8 | <1s | 0 |
| Tese generation | 407 | <1s | 0 |
| Resumo generation | 1226 | <1s | 0 |
| Links generation | 155 | <1s | 0 |

Total: ~6s for 2491 files. Compare: subagent-based enrichment of 441 files
took 600s+ (with timeouts requiring 2 waves).

## Integration with Pipeline Semanal

This should run as **F2.11 Batch Enrichment** — after F2.10 (adversarial gate)
and before F2.8 (Nexus spot-check). Programmatic enrichment eliminates
structural debt before AI verification, so AI spot-checks focus on content
quality instead of missing sections.

## Pitfalls

- **Tese from body may be low quality**: first 2 sentences of content aren't
  always a thesis. Acceptable for approved scaffold; `reflect: true` sources
  should get AI refinement.
- **Resumo from Tese is redundant**: when Resumo = first 3 sentences of Tese,
  it's essentially a longer Tese. Acceptable as placeholder — AI subagents
  can refine later.
- **Links by tag matching may create false connections**: tag overlap ≠
  semantic relevance. Acceptable as scaffold — connection-finder or manual
  review can prune later.
- **Decision heuristic false-disapprove**: a thin-but-novel source (word_count
  just under threshold) risks `disapproved` as junk. Off-interest novelty is
  still preserved as captura leve — never disapprove on `interest` alone, only
  on dup/junk (G0/G2).

## Session Validation (2026-06-28)

```
Before: 452 A, 356 B, 0 C, 0 D, 1685 NO_GRADE → 49% overall completeness
After:  879 A, 1374 B, 227 C, 11 D, 0 NO_GRADE → 100% overall completeness
```