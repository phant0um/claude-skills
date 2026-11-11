---
status: active
parent: "[ingest-verify](../SKILL.md)"
kind: reference
name: ingest-verify-02-batch-calibration
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 3 secoes, 91 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---

> Seção fatiada de [ingest-verify](../SKILL.md). Carregar sob demanda: calibração batch programático vs AI ingest, large batch patterns.

## Batch programático vs AI ingest — F2.9 calibration (2026-06-28)

**Padrão**: batch ingest via `execute_code` (zero AI calls) produz F2.9 Minha
Síntese como placeholder ("A ser analisado em revisão manual") em ~70% das
`reflect: true` pages. Isto é **dívida técnica esperada**, não defeito.

**Calibração do C9**:
- Batch AI (subagentes): C9 FAIL em placeholder é válido — AI deveria gerar reflection
- Batch programático: C9 WARN em placeholder é o correto — placeholder é esperado,
  precisa de pass posterior com AI ou revisão manual seletiva

**Check**: se >60% das `reflect: true` pages têm placeholder E o batch foi processado
via execute_code (zero AI), reportar como "dívida técnica esperada" não como
"batch com defeito sistêmico". F2.10 adversarial-gate-v2 deve considerar o
método de ingest ao avaliar placeholder rate.

When a batch ingest produces source pages with many unresolved wikilinks pointing
to non-existent concepts/entities, the fix is NOT to remove the links — it's to
CREATE the missing concepts/entities. This is the primary mechanism by which the
vault knowledge graph grows.

**Pattern**:
1. After ingest, run wikilink resolution check (C2) across all new source pages
2. Collect all unresolved links, grouped by target path
3. Sort by frequency (concepts linked by 3+ sources = high priority)
4. Create each missing concept/entity with:
   - Frontmatter (title, type, created, updated, tags)
   - Definition (1-2 sentences)
   - Key points or patterns
   - `## Evidências` section linking back to source pages
   - `## Links` section with cross-references
5. Re-run resolution check — should be near 100%

**Session result**: 18 source pages → 80 wikilinks → 40 unresolved (50%) →
created 24 concepts/entities → 134/134 resolved (100%).

**Pitfall**: don't create stub concepts with only a definition and no evidence.
Each concept should link back to at least 1 source page that provides evidence.
A concept with zero backlinks is an orphan — it exists but has no foundation.

## Large Batch Ingest Pattern — execute_code > subagent delegation (2026-06-28)

When batch >100 files, subagent delegation is impractical (max 3 concurrent children, each
needs full context). Instead, use `execute_code` with a Python script that:

1. Loads approved candidates from `/tmp/candidates_aprovados.txt` (`<path>|<interest>|<domain>`)
2. For each file: reads content, cleans boilerplate, categorizes, creates source page
   (frontmatter + Tese Central + Resumo sections + wikilinks + Minha Síntese for `reflect: true`)
3. Updates manifest atomically (JSON load→modify→write, with + without extension keys)
4. Moves approved files to `08-ARCHIVE/approved/YYYY-MM-DD/`
5. Reports category breakdown + errors

**Performance**: 722 files in 1.2s, 0 errors, 1444 manifest entries (with aliases).

**When to use**: batch >100 approved files where source pages follow a template pattern.
**When NOT to use**: batch <20 (overhead of script setup > value) or files requiring
deep AI analysis per source (FIAP apostilas, concurso aulas with question extraction).

**Key**: the script must handle file evaporation gracefully (`os.path.isfile` check before
processing each file), and generate wikilinks from a pre-built keyword→link map that is
verified against the actual vault structure (see "Batch ingest programmatic wikilinks"
pitfall above).

## Approved Archive Ingest Pattern — subagent delegation for 5-20 files (2026-07-06)

When 5-20 approved files in `08-ARCHIVE/approved/` need quality synthesis (not programmatic
batch), despachar subagentes via `delegate_task`. Diferente do large batch, este padrão
produz source pages com síntese rica (Tese central, Argumentos, Key insights, Minha Síntese)
porque cada subagent lê e sintetiza um artigo.

> **Reference completo**: `references/approved-archive-ingest.md` — workflow de 6 passos,
> pitfalls (subagent path mismatch, dedup, max_concurrent_children=3, concept enrichment).

**Key steps**: (1) verificar já não ingerido, (2) despachar em batches de 3, (3) verificar
arquivos criados, (4) deduplicar, (5) concept page enrichment com evidence refs, (6) verificação
zero órfãos.

