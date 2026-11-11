---
status: active
parent: "[ingest-verify](../SKILL.md)"
kind: reference
name: ingest-verify-04-pitfalls-manifest
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 5/5 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 6 secoes, 255 linhas; drift R12: 1 achados resolvidos (A/B/F)"
reviewed-by: R13 (claude-sonnet; drift R12 corrigido)
reviewed: 2026-10-04
---
## Contents

- [Pitfall: fix_broken_links stub creation bug — duplicated paths + .md.md extension — 2026-07-05](#pitfall-fix_broken_links-stub-creation-bug-duplicated-paths-mdmd-extension-2026-07-05)
- [Pitfall: Thin duplicate discovery — pipeline created same article with different filename — 2026-07-06](#pitfall-thin-duplicate-discovery-pipeline-created-same-article-with-different-filename-2026-07-06)
- [Pitfall: Cross-directory thin duplicates with different filenames — 2026-07-06](#pitfall-cross-directory-thin-duplicates-with-different-filenames-2026-07-06)
- [Pitfall: Parallel subagent dispatch — orchestrator must own manifest + link repair (2026-07-12)](#pitfall-parallel-subagent-dispatch-orchestrator-must-own-manifest-link-repair-2026-07-12)
- [Pitfall: Orchestrator-direct batch ingest — no subagents for batches ≤30 (2026-07-12)](#pitfall-orchestrator-direct-batch-ingest-no-subagents-for-batches-30-2026-07-12)


> Seção fatiada de [ingest-verify](../SKILL.md). Carregar sob demanda: pitfalls de manifest e links (stub bug, thin duplicates, parallel dispatch).

## Pitfall: fix_broken_links stub creation bug — duplicated paths + .md.md extension — 2026-07-05

**Sintoma**: `fix_broken_links.py --create-stubs` criou 202 stubs para resolver
broken links, mas 178 stubs foram criados em paths aninhados duplicados
(`concepts/agent-systems/ai-agents/X.md`) e 92 com extensão `.md.md` (dupla).

**Causa**: O script extrai o path do wikilink e cria o stub no path resolvido.
Quando o wikilink é `agent`, o script concatena
`concepts/agent-systems/` (subdir do wikilink) + `ai-agents/` (subdir esperado) +
`agent.md` → path duplicado. A extensão `.md.md` ocorre porque o script
adiciona `.md` ao filename que já termina com `.md` do basename extraction.

**Fix aplicado (3 etapas)**:
1. Mover 86 stubs de paths aninhados para paths canônicos (remover duplicação
   de subdir + extensão .md.md extra)
2. Preencher 94 stubs com definições reais de 1-3 linhas baseadas no nome
3. Deletar 92 duplicatas (stub + arquivo canônico já existente) + 6 lixo

**Lição**: ao criar stubs programaticamente para resolver broken links:
- Validar o path resultante ANTES de escrever (não criar `X/X/Y.md.md`)
- Verificar se arquivo canônico já existe antes de criar stub duplicado
- Usar `os.path.normpath()` para detectar paths aninhados duplicados
- Verificar extensão final (não appendar `.md` se já termina com `.md`)

**Check**: ao verificar stubs criados por fix_broken_links, detectar paths
aninhados duplicados com:
```bash
find 03-RESOURCES/concepts/ -type d | grep -E "/([^/]+)/\1$"
find 03-RESOURCES/concepts/ -name "*.md.md"
# Se output não-vazio, cleanup necessário
```

## Pitfall: Thin duplicate discovery — pipeline created same article with different filename — 2026-07-06

**Sintoma**: Após ingerir 5 source pages via subagentes (quality synthesis, 56-112 linhas),
descoberto que 6 dos mesmos artigos já existiam como thin stubs (37-42 linhas) em
`ai-agents/` e `claude-code-skills/` com filenames completamente diferentes.

**Exemplo**: `ai-agents/the-fable-5-subagent-setup-how-to-run-parallel-agents-exact-config-inside.md`
(37 linhas, pipeline batch) vs `ai-agents-harness/fable-5-subagent-setup-parallel-agents.md`
(112 linhas, subagent ingest). Mesmo artigo, slug diferente, diretório diferente.

**Causa**: O pipeline-semanal batch programático cria source pages com slugs
longos derivados do título completo. Subagentes ingerindo manualmente geram
slugs curtos e descritivos. Ambos são válidos mas produzem arquivos diferentes
para o mesmo conteúdo.

**Fix aplicado**:
1. Após criar novos sources, buscar por keywords do título (não filename) em
   todo `03-RESOURCES/sources/`
2. Para cada hit: comparar `wc -l` — manter a maior, deletar a thinner
3. Redirecionar wikilinks via `execute_code` + `os.walk` full-scan (não
   `search_files` — perde refs em vaults grandes)
4. Verificar zero órfãos com `search_files` count mode

**Lição**: O passo "verificar já ingerido" no approved-archive-ingest workflow
deve buscar por TÍTULO/keywords, não só por filename/slug. Source pages do
mesmo artigo podem ter filenames radicalmente diferentes dependendo do método
de ingest (pipeline batch vs subagent manual).

## Pitfall: Cross-directory thin duplicates with different filenames — 2026-07-06

**Sintoma**: Após dedup inicial (6 thin stubs deletados), descoberto que o `fable-5-agent-stack.md`
concept page ainda linkava para paths que não existiam — os links originais apontavam para
`ai-agents/the-fable-5-subagent-setup-*.md` (deletado) mas a source page nova estava em
`ai-agents-harness/fable-5-subagent-setup-parallel-agents.md` (slug completamente diferente).

**Causa**: O pipeline batch e os subagentes não só geram slugs diferentes — também podem
colocar o mesmo artigo em **diretórios diferentes** (`ai-agents/` vs `ai-agents-harness/`).
A busca por título/keywords no passo de dedup precisa cobrir TODOS os subdirs de sources/,
não só o subdir alvo do ingest.

**Fix aplicado**:
1. Após deletar thin stubs, executar `execute_code` com `os.walk` full-scan em
   `03-RESOURCES/` procurando por wikilinks que apontam para os arquivos deletados
2. Para cada hit: redirecionar o wikilink para o path canônico (a source page maior)
3. Verificar zero órfãos com `search_files` count mode

**Lição**: thin duplicates não são só filename mismatch — são também directory mismatch.
O repair de wikilinks pós-dedup deve usar `os.walk` full-scan, não `search_files` incremental
(perde refs em vaults grandes). O `fable-5-agent-stack.md` era o canário: linkava 5 paths
deletados simultaneamente.

## Pitfall: Parallel subagent dispatch — orchestrator must own manifest + link repair (2026-07-12)

**Sintoma**: 3 subagentes despachados em paralelo para ingest de 85 files.
Subagentes receberam instruções para criar source pages mas NÃO atualizar
manifest nem criar stubs. Isto evita: (1) manifest race condition quando
múltiplos subagentes fazem jq append simultaneamente, (2) stub duplication
quando múltiplos subagentes criam o mesmo concept stub, (3) link repair
scattered across subagents sem visão global.

**Padrão correto para dispatch paralelo de ingest**:

1. **Orchestrator pre-work**: classificar todos os candidatos (path|slug|category|interest),
   dividir em batches de ≤29 files (max_concurrent_children=3 no scheduler legado)
2. **Subagent instructions explícitas**:
   - "Do NOT update manifest — orchestrator handles it"
   - "Do NOT create concept stubs — only link existing concepts"
   - "Do NOT run batch_enrich or fix_links — those run later"
   - "Do NOT move files — orchestrator handles archive"
3. **Orchestrator post-work** (após todos subagentes completarem):
   - Atualizar manifest atomicamente (1 jq/Python call para todas as 85 entries)
   - Rodar `fix_broken_links.py --create-stubs` (1 pass global, não por subagent) <!-- drift:ok: fix_broken_links.py removido; registro histórico (R13) -->
   - Rodar `normalize_stubs.py` se stubs criados
   - Rodar `batch_enrich.py --all` (decision/tese/resumo/links/orphans)

**Causa de não delegar manifest+stubs aos subagentes**:
- Manifest: jq append não é atômico sob concorrência — 3 subagentes fazendo
  `jq --arg k "$bn" '.sources[$k] = ...'` simultaneamente causam lost updates
  (último write vence). O orchestrator faz 1 call após todos completarem.
- Stubs: se 3 subagentes criam stubs para o mesmo concept missing, você
  obtém 3 arquivos duplicados ou race condition no filesystem. O orchestrador
  faz 1 pass global coletando todos os broken links primeiro.
- Link repair: cada subagent só vê seus próprios links quebrados, não tem
  visão do batch inteiro. O orchestrador faz repair global pós-batch.

**Evidência**: pipeline-semanal 2026-07-12, 85 files, 3 subagentes (29+29+27).
  Subagentes instruídos a NÃO tocar manifest/stubs/enrich. Orchestrator
  planejava post-work: manifest update + fix_broken_links + batch_enrich.

## Pitfall: Orchestrator-direct batch ingest — no subagents for batches ≤30 (2026-07-12)

**Sintoma**: Batch de 29 files listed in `/tmp/batch_aa` (format: `path|slug|category|interest`).
Orchestrator reads all source files, creates source pages directly via `write_file`,
links existing concepts/entities only (no stubs), skips manifest, skips file moves.
No subagentes despachados. 22 source pages created (7 `_2.md` variant files missing).

**Quando usar este padrão (orchestrator-direct vs subagent delegation)**:
- **≤30 files**: orchestrator reads + writes directly. Context window can hold all files.
  Faster, no subagent overhead, no race conditions on manifest/stubs.
- **31-90 files**: subagent delegation in batches of ≤30 (max 3 concurrent).
  Orchestrator owns manifest/stubs/link-repair post-work.
- **>100 files**: `execute_code` Python script (programmatic batch, zero AI per file).

**Workflow (orchestrator-direct, ≤30 files)**:

1. **Read batch file** (`/tmp/batch_NN` — format: `path|slug|category|interest` per line)
2. **Path translation**: batch file paths may point to `08-ARCHIVE/approved/<date>/` but
   files are actually in `00-INBOX/clippings/`. Always verify with `ls` or `search_files` first.
   If batch paths don't exist, search `00-INBOX/clippings/` for the actual files.
3. **Inventory existing concepts/entities** for linking:
   ```bash
   ls 03-RESOURCES/concepts/ | sed 's/\.md$//' | tr '\n' '|'
   ls 03-RESOURCES/entities/ | sed 's/\.md$//' | tr '\n' '|'
   ```
   Note: search_files returns max 200 results. Use `ls` via terminal for full lists.
4. **Read source files in parallel** (batch 6 at a time via concurrent `read_file` calls):
   - Articles: 5000 chars is sufficient for synthesis
   - Dense/long files (>10K chars): read with `limit=150`, then `offset=151` for remainder
   - Skip frontmatter when reading (start from content)
5. **Create source pages** via `write_file` (batch 2-3 at a time):
   - Frontmatter: `title`, `type: source`, `source`, `created`, `ingested`, `tags`
   - Sections: `## Tese central`, `## Argumentos principais`, `## Key insights`,
     `## Exemplos e evidências`, `## Implicações para o vault`, `## Links`
   - Link only existing concepts/entities: `<kw>`,
     `<entity>`
   - Do NOT create stub concepts — only link existing ones
   - Do NOT update manifest
   - Do NOT move files
6. **Handle duplicate variants**: `_2.md` and ` 1.md` suffix files:
   - `_2.md` variants often DON'T EXIST — skip silently, report in summary
   - ` 1.md` variants usually DO exist as exact duplicates — create thin stub page
     pointing to the primary source page (avoid duplicate content)
7. **Report**: list all source page paths created + list of skipped missing files

**Key pitfalls discovered**:

### P-O1 — Batch file path mismatch
Batch file paths pointed to `08-ARCHIVE/approved/2026-07-12/` but files were in `00-INBOX/clippings/`.
ALWAYS verify paths exist before reading. If not, search `00-INBOX/clippings/` for the actual files.
This is the same class of problem as the approved-but-not-ingested gap (pre-ingest-dedup v1.7)
but in reverse: the batch file references a destination path, not the actual source location.

### P-O2 — Missing `_2.md` duplicate files
Batch files may include entries for `_2.md` variants that were never created by the
clipper/sync tool. Of 29 entries in batch_aa, 7 `_2.md` files did not exist. Solution:
- Check existence with `terminal` + `ls` before attempting to read
- Skip missing files silently
- Report skipped files in the final summary
- Do NOT create placeholder source pages for non-existent files

### P-O3 — Duplicate ` 1.md` variant files
Some batch entries include both `Article Name.md` and `Article Name 1.md` — the latter
is an exact duplicate clipping. Create a thin stub source page for the ` 1` variant that:
- Has standard frontmatter
- Notes it is a duplicate in `## Tese central`
- Links to the primary source page: `<primary-slug>`
- Prevents the ingest-verify check from flagging it as missing

### P-O4 — search_files 200-result cap
`search_files` returns max 200 results. For vaults with 400+ concepts or 380+ entities,
the full list is capped. Use `terminal` with `ls` + `sed` + `tr` to get complete lists
for concept/entity name matching when linking.

### P-O5 — Context window management for large files
Files >10K chars need multi-read: `read_file` with `limit=150` for first chunk,
then `offset=151` for remainder. Batch reads in parallel (6 concurrent `read_file`
calls) to avoid serial round-trips. For 29 files, 5 batches of 6 reads completes
all source file reading efficiently.

### P-O6 — Context compression mid-batch degrades source page quality

**Sintoma**: Orchestrator-direct batch ingest of 29 files (batch_ab). All 21 found files
read successfully in 3 batches of 7. Context compression occurred after reading batch 1
(but before creating source pages for batch 1). Source pages for batch 1 were created from
compressed/summarized context — the detailed file content was lost. Source pages for batches
2-3 were created from fresh reads (post-compression) and are more detailed.

**Causa**: The orchestrator reads all source files first, then creates source pages. If
context compression fires between the read phase and the write phase, the detailed content
of files read before compression is lost — only the summary survives. Source pages created
from summaries are shorter and less specific (fewer concrete examples, less precise
argument reconstruction).

**Fix**: For batches >15 files, interleave reads and writes per sub-batch instead of
reading all files first then writing all pages:
1. Read sub-batch (6-7 files) → immediately create source pages for those 6-7 files
2. Read next sub-batch → immediately create source pages for those
3. This keeps the detailed file content in active context when creating each source page

**Alternative**: If context compression has already occurred, re-read the affected files
before creating their source pages. The cost is extra read_file calls, but the source pages
will be based on actual content rather than summaries.

**Detection**: After batch completion, check source page sizes. If pages from early
sub-batches are significantly shorter than pages from later sub-batches (after compression),
context degradation likely occurred. Re-create the affected pages from fresh reads.

**Evidência**: pipeline-semanal 2026-07-12 batch_ab, 29 entries → 21 source pages.
Batch 1 (7 pages) created post-compression — shorter, less detailed. Batches 2-3
(14 pages) created from fresh reads — more detailed, better evidence sections.

