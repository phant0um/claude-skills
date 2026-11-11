---
type: reference
status: active
kind: reference
name: subagent-team-pitfalls
parent: 04-SYSTEM/automation/skills/orchestration/subagent-team/SKILL.md
updated: 2026-08-08
reviewed-scope: "checagem mecanica + semantica: 0/0 wikilinks resolvem; 2/2 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 2 secoes, 257 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Pitfalls: Parallel Ingest Subagents (2026-06-22)](#pitfalls-parallel-ingest-subagents-2026-06-22)


# Subagent Team — Pitfalls (referência)

Consultar quando um batch de subagentes falhar, der timeout ou produzir saída suspeita. Mantido em arquivo separado para não soterrar o protocolo de execução (R3: inline o que todo branch precisa; referência o que só alguns alcançam).

## Pitfalls: Parallel Ingest Subagents (2026-06-22)

When dispatching multiple subagents to ingest 00-INBOX/clippings in parallel (>20 files):

### Incomplete task execution

Subagents created source pages but **did not**:
- Move original 00-INBOX/clippings to `08-ARCHIVE/[A|B]/`
- Update `.raw/.manifest.json` with dual-key entries
- Move root-level source pages to category subdirectories

**Fix:** The orchestrator (parent) must do a post-subagent cleanup pass:
1. Check which 00-INBOX/clippings still exist → move to archive
2. Check manifest entry count vs source page count → add missing entries
3. Check for root-level source pages → move to category dirs

### Duplicate source pages (root + category)

Different subagents may create the same source page at different paths:
- Subagent 1: `03-RESOURCES/sources/the-agent-stack.md` (root) <!-- drift:ok: exemplo -->
- Subagent 2: `03-RESOURCES/sources/ai-agents/the-agent-stack.md` (category) <!-- drift:ok: exemplo -->

**Fix:** Post-batch dedup — find files with same basename in root and category,
remove root-level copy (keep categorized version).

### Manifest concurrency

Multiple subagents writing to `.raw/.manifest.json` simultaneously can corrupt
the file. **Fix:** Subagents should NOT write to manifest — only create source
pages. Parent orchestrator does a single atomic manifest update after all
subagents complete.

### Batch size for parallel ingest

- 3 concurrent subagents × 30-35 files each = optimal for 90-100 total
- >35 files per subagent → context window pressure → thin source pages
- Monitor: if source page avg size < 1500 bytes, subagent is skimming
- **Timeout risk:** 3/3 subagents timed out at 600s (10min) with 32 files each.
  They completed 16-26 API calls before timeout — creating source pages but not
  completing archive moves or manifest updates. **Recommendation: batch size
  15-20 files per subagent** to finish within 600s, or request higher timeout.
- **2026-07-12 confirmation:** 3 batches of 29+29+27 files. Batch 3 (27 files)
  timed out at 600s with 42 API calls — produced 22/27 source pages. Batches 1-2
  (29 files each) completed but took 443s and 538s respectively. **27 files is
  the edge — 29 barely completes. Stick to ≤25 per subagent for safety margin.**

### Retry pattern for timed-out subagents (2026-07-12)

When a subagent times out mid-batch, the orchestrator must:

1. **Audit filesystem** — check which source pages exist vs which are missing:
   `while IFS='|' read -r f slug cat interest; do [ -f "03-RESOURCES/sources/$slug.md" ] || echo "MISSING: $slug"; done < batch_file`
2. **Check original file location** — timed-out subagent may have looked in
   `08-ARCHIVE/approved/$(date -I)/` but files might still be in `00-INBOX/clippings/`
   (if archive move happened before subagent read, the path is wrong).
3. **Dispatch retry subagent** with ONLY the missing files, using their actual
   current path. Keep batch ≤10 for retry (fast completion, no timeout risk).
4. **Update manifest** for retry-created pages separately (subagents don't
   write manifest — orchestrator does it atomically after all batches).

**Key:** Always pass the ACTUAL filesystem path to the retry subagent, not the
original batch path. Files may have been moved by earlier pipeline phases.

### Thin source page detection (post-batch)

Some subagents produce minimal source pages (19 lines for a 48K-char Clipping).
**Detection:** post-batch, check `wc -l` on new source pages. Pages < 30 lines
for files > 10K chars are flagged for expansion. The orchestrator should
re-read the original Clipping and expand the thin page with full content.

### Deep Analysis Delegation — 2026-06-23 (Run 2)

When the pipeline produces >100 source pages, the mechanical batch ingest
creates pages but skips the analytical layers (F2.5 Concept Absorption, F2.9
Personal Reflection, skill/agent/hook detection). Delegating deep analysis to
3 parallel subagents worked well but has key learnings:

**What worked:**
- 3 batches of ~62 files each, 8min total (484s aggregate, parallel)
- Each subagent: read source page → check wikilinks → append evidence to
  existing concepts → write reflections for Score A → detect patterns
- 222 evidence entries appended, 99 reflections written, 24 patterns detected

**What failed:**
- **Link path mismatch**: subagents found wikilinks pointing to non-existent
  paths. Batch 1 resolved via basename matching (entity files happened to
  match). Batch 2 found 0 matching concepts (0 absorptions). Batch 3 found
  only 2 exact matches. This is a systematic issue — the batch_ingest script
  generates links with paths that don't match vault structure.
- **Inconsistent resolution strategies**: each subagent invented its own
  approach to resolve broken links. Batch 1 did basename→entity matching.
  Batch 2 reported them as "concepts to create" without absorbing. Batch 3
  only checked exact path matches. This variance means quality is unpredictable.

**Fix for future runs:**
1. **Pre-delegation**: run link repair BEFORE deep analysis. Fix all broken
   wikilinks so subagents don't waste time on path resolution.
2. **Standardize instructions**: tell subagents explicitly: "For each wikilink,
   check if the file exists at the exact path. If not, check by basename
   across concepts/ and entities/ directories. If found, append evidence there."
3. **Post-delegation cleanup**: after all subagents complete, run a parent-level
   link resolution check + create missing stubs. This catches what subagents
   missed.
4. **Batch size**: 62 files per subagent is fine for deep analysis (reading +
   writing), but each subagent took different time (139s vs 484s vs 198s).
   The 484s one was slower due to more file reads. 50 files per batch is safer.

**Key insight**: deep analysis subagents should NOT be responsible for link
repair. They should absorb evidence into existing files and write reflections.
Link repair + stub creation is a parent-level concern that should happen
before (to maximize absorption) or after (to catch gaps) — not during.

### Batch-Wave Exec-Spec Pattern (2026-07-05 — AFRFB resumo generation)

O exec-spec que este padrão consome hoje sai da skill `plan-handoff` (ondas, conflitos, contrato de relatório).

**When to use:** a self-contained exec-spec document defines N independent
units of work (e.g. one `resumo.md` per disciplina), each unit is a leaf
write-task, and `delegate_task` can dispatch up to 3 in parallel.

**Workflow:**
1. **Validate inventory vs filesystem BEFORE dispatching.** Confirm folder
   count, file count per folder, and token estimate per folder. The spec's
   inventory can drift from the real filesystem — verify or you dispatch
   subagents against wrong assumptions.
2. **Pre-fetch display metadata.** Extract `disciplina:`, `concurso:`,
   `provider:` from one sample file per folder via grep. Subagents need
   the exact display name for frontmatter — don't make them guess.
3. **Dispatch in batches of 3** (delegate_task max_concurrent_children).
   Sort by tier: lighter folders first (faster feedback), heaviest last
   (longest runtime, but by then you've validated the prompt shape).
4. **Overlap waves.** While batch 1 runs, pre-fetch inventory for waves
   2-5 so the next dispatch is instant. Don't idle waiting for results.
5. **Pass EXACT filenames to subagents.** Folders with mixed suffixes
   (`-prof-fabio-dutra`, `-somente-em-pdf`, `-parte-ii-somente-pdf`) need
   wikilinks with the EXACT basename. Tell subagents explicitly: "o
   wikilink deve usar o basename EXATO do arquivo sem .md." Otherwise
   they truncate suffixes and links break.
6. **Map-reduce inside the subagent goal.** For tier P (>900K tok), split
   into 3-5 lotes in the goal text. For tier M (400-900K), 2 lotes. For
   tier L (<400K), 1 lote. Subagent manages its own lotes internally.
7. **Verify post-batch on filesystem.** After each batch returns, run:
   `for d in */; do [ -f "$d/resumo.md" ] && echo "OK $d" || echo "FALTA
   $d"; done` and `grep -rl "^grade:\|^tese:" */resumo.md` (should be
   empty). Don't trust subagent self-reports — verify on filesystem.

**What worked (AFRFB batch 1, 3 subagents, ~2min):**
- 3/3 completed, all files written, all wikilinks resolved, zero grade/tese
- Subagent self-verification was accurate for batch 1 (rare — usually
  verify independently)
- Pre-fetching Onda 2 inventory while batch 1 ran eliminated idle time

**Pitfall: subagent `awk /tese/` false positive.** One subagent ran
`awk '/tese/'` to check for forbidden `tese:` field — it matched
"Estratégia" (contains "tese" as substring). Use `grep -E "^tese:"`
(anchor + colon) not substring match.

### Subagent self-report vs filesystem audit — 2026-07-06

**Sintoma**: Subagent reportou "25/25 arquivos patchados com sucesso" mas
auditoria no filesystem mostrou 0/25 files com a seção `## Minha Síntese`.
O subagent verificou presença da string mas os patches não foram aplicados
(provável: subagent leu o arquivo, gerou a síntese, mas o patch tool não
executou ou falhou silenciosamente).

**Causa**: Subagents em timeout parcial (600s) podem completar API calls mas
não necessariamente escrever todos os patches. O self-report é baseado em
intenções executadas, não em verificação pós-escrita. Rate limits (HTTP 429)
também causam perda silenciosa — o subagent reporta "completed" mesmo quando
API calls falharam após retry.

**Fix obrigatório**: após toda delegação batch, o parent DEVE auditar com:
```bash
# Para cada batch file, verificar se a mudança foi aplicada
while IFS= read -r f; do
  grep -q "## Minha Síntese" "$f" 2>/dev/null && echo "OK" || echo "MISSING: $f"
done < batch_file_list.txt
```

**Lição**: nunca confiar em self-reports de subagents para operações de
escrita. Sempre auditar o filesystem. Isto é especialmente crítico quando:
- Rate limits (HTTP 429) ocorreram durante o batch
- Subagent timed out (mesmo que "completed" status)
- Batch size > 25 files (mais opportunity para perda silenciosa)

### Subagent git autonomy — commits silenciosos (2026-06-28)

Subagente com acesso a terminal roda `git add`/`git commit` no repo de trabalho
sem o parent saber. Dois subagentes de tradução commitaram sozinhos (`4465615`,
`45ac893`); o parent só percebeu porque `git status` veio limpo — os arquivos
"novos" já estavam em HEAD, e o commit do parent capturou só o resto do diff.

Consequências: histórico fragmentado com mensagens enganosas; risco de push sem
aprovação do parent; nenhum gate de verificação entre o commit do subagente e o
remoto.

Instrução explícita a todo subagente:

```
DO NOT run git commit or git push. Write files only. The parent orchestrator
will review, commit, and push after verifying all subagent outputs.
```

Protocolo do parent após o batch: rodar `git log --oneline -5` e conferir commits
inesperados; revisar o conteúdo deles antes de qualquer push. Mais perigoso ainda
quando subagente e parent compartilham o mesmo working directory — subagente
escreve no diretório alvo, nunca no estado do git.

### Post-subagent cleanup checklist (updated 2026-06-23 run 2)

After all ingest subagents complete (or timeout), the parent orchestrator MUST:

1. **Dedup check:** find source pages with same basename in root and category
   dirs → remove root-level, keep categorized
2. **Root-only relocation:** find source pages in `03-RESOURCES/sources/` root
   → move to appropriate category subdir
3. **Archive moves:** check which 00-INBOX/clippings still exist → move to
   `08-ARCHIVE/[A|B]/YYYY-MM-DD/`
4. **Manifest update:** single atomic `jq` write for all new entries (dual-key:
   with and without extension, `alias_of` field for secondary key). **Done by
   orchestrator, NOT subagents** — prevents concurrent write corruption.
5. **Thin page detection:** `find 03-RESOURCES/sources/ -name "*.md" -newer
   $MARKER -type f -exec wc -l {} \;` → flag pages < 30 lines
6. **F2.8 spot-check:** read 3 random source pages — check tese central,
   link resolution, info preservation
7. **Link repair (NEW):** run wikilink resolution check across all new source
   pages. Repair broken links via basename matching. Create missing concept/
   entity stubs at exact link paths. Target: 100% resolution.
8. **Deep analysis delegation (NEW):** if >50 source pages, dispatch 3 parallel
   subagents for F2.5 Concept Absorption + F2.9 Personal Reflection + pattern
   detection. Run link repair BEFORE delegation for maximum absorption.
9. **Reflection verification (NEW):** after subagents complete, verify that
   placeholder "A ser analisado" text was replaced. `grep -r "A ser analisado"
   03-RESOURCES/sources/ | wc -l` should be near 0.
10. **Timeout audit (2026-07-12):** if any subagent timed out, audit which
    source pages are missing vs created. Dispatch retry with correct file
    paths (files may have moved to archive during pipeline). Update manifest
    for retry pages separately.

