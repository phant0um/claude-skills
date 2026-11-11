---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-07-pitfalls-links
type: skill-reference
updated: 2026-07-16
reviewed-scope: "W3c 2026-10-10: poda de 8 pitfalls obsoletos/cobertos (scripts ausentes; teste planted); 5 secoes restantes"
reviewed-by: R13 (claude-sonnet; drift R12 corrigido)
reviewed: 2026-10-04
---
## Contents

- [Pitfall: Subagent concept path mismatch — 2026-06-30](#pitfall-subagent-concept-path-mismatch-2026-06-30)
- [Pitfall: Manifest boolean values — 2026-06-30](#pitfall-manifest-boolean-values-2026-06-30)
- [Pitfall: F2.10 quality gate false-positive broken links — Obsidian basename resolution (2026-07-06)](#pitfall-f210-quality-gate-false-positive-broken-links-obsidian-basename-resolution-2026-07-06)
- [Pitfall: Daily-scan producer writes phantom paths to candidates_new.txt (2026-07-12)](#pitfall-daily-scan-producer-writes-phantom-paths-to-candidates_newtxt-2026-07-12)
- [Pitfall: `10X` regex matches tech content "10x" as clickbait (2026-07-11)](#pitfall-10x-regex-matches-tech-content-10x-as-clickbait-2026-07-11)


> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: pitfalls de wikilinks, manifest, F2.10, daily-scan, 10X.

## Pitfall: Subagent concept path mismatch — 2026-06-30

**Sintoma**: 46 broken wikilinks em 21 source pages recém-criadas (32.6%).
Links `X` não resolvem porque o concept está em
`03-RESOURCES/concepts/agent-systems/agent-systems/X.md` (subdir).

**Causa**: subagentes criam concepts em subdirs (`concepts/agent-systems/`,
`concepts/llm-ml/`, etc.) mas linkam como `concepts/X` (sem subdir)
nas source pages. O vault tem concepts organizados em ~15 subdirs, mas o
template do ingest-agent diz `<kw>` sem especificar
subdir.

**Fix programático**: após ingest batch, rodar script que:
1. Extrai todos `X` das source pages
2. Para cada link quebrado, busca X em todos subdirs de `concepts/`
3. Se encontrado: substitui link por `X`
4. Se não encontrado: cria stub em `concepts/<subdir>/X.md` (subdir inferido
   da categoria da source page)

**Prevenção**: template do ingest-agent deve dizer:
"Link concepts com path completo: `<name>`.
Se não souber o subdir, usar `concepts/agent-systems/` como default para ai-agents
category, `concepts/llm-ml/` para papers, etc."

**Evidência**: pipeline-semanal 2026-06-30, 3 subagentes, 21 source pages,
46/141 links quebrados (32.6%). Fix aplicado: 15 links corrigidos + 30 stubs
criados.

## Pitfall: Manifest boolean values — 2026-06-30

**Sintoma**: script Python que mapeia source pages do manifest falha com
`TypeError: unsupported operand type(s) for /: 'PosixPath' and 'bool'`.

**Causa**: alguns entries do `.raw/.manifest.json` têm `source_page: true`
(boolean) ao invés de `source_page: "path/to/file.md"` (string). Isto acontece
em runs antigos onde o manifest foi atualizado com `jq` mas o campo
`source_page` foi setado como flag boolean em vez de path.

**Fix**: sempre validar tipo antes de usar campos do manifest:
```python
if source_page and isinstance(source_page, str):
    sp = VAULT / source_page
```

**Evidência**: pipeline-semanal 2026-06-30, mapeamento de 150 candidatos,
12 entries com `source_page: true` em vez de string.

## Pitfall: F2.10 quality gate false-positive broken links — Obsidian basename resolution (2026-07-06)

**Sintoma**: F2.10 Batch Quality Gate reportou 103 "broken" wikilinks → veredito
`PIPELINE FAIL` (83.1% critical issues). Mas inspeção manual mostrou que 101/103
links resolvem corretamente no Obsidian por basename matching — apenas 1 era
truly broken (`graphify` sem target no vault).

**Causa**: O checker de broken links faz filesystem check direto: procura
`VAULT / "{link}.md"` ou `VAULT / link`. Mas Obsidian resolve wikilinks curtos
(`X`) por basename match em qualquer parte do vault — não exige path completo.
Source pages linkam entre si por basename (`you-have-1-day-to-clone-fable-5`)
sem path prefix, e o Obsidian resolve isso. O checker não simula esta resolução.

**Fix**: Quality gate broken-link check DEVE simular Obsidian basename resolution:
1. Construir índice basename → path de todos .md files do vault (excluindo
   08-ARCHIVE/ e .git/)
2. Para cada link sem path prefix (não começa com `03-RESOURCES/`, `04-SYSTEM/`,
   etc.), procurar por basename no índice
3. Só flagar como truly broken se basename não existe em NENHUM subdir do vault
4. Classificar: broken_concept (links p/ concepts/entities com path), broken_source
   (links p/ sources com path), broken_other (links curtos sem path — resolver por
   basename)

**Verificação rápida**:
```python
# Build basename index once
basename_idx = {f.stem.lower(): str(f.relative_to(VAULT))
                for f in VAULT.rglob("*.md") if "08-ARCHIVE" not in str(f)}
# For each short link, check basename resolution
stem = link.split("/")[-1].split("|")[0].strip().lower()
if stem in basename_idx:
    resolved += 1  # Obsidian resolves it
else:
    truly_broken.append(link)  # genuinely missing
```

**Impacto**: Sem este fix, F2.10 gera false-positive `PIPELINE FAIL` em quase
todo run com >20 source pages (source pages linkam entre si por basename).
Veredito correto requer classificação: broken concept/entity links (crítico) vs
short links resolved by Obsidian (não-crítico).

**Evidência**: pipeline-semanal 2026-07-06, 124 source pages, 103 "broken" links
reportados → 101 resolved by basename, 1 truly broken, 1 duplicate. Veredito
correto: `PIPELINE OK` (não FAIL).

## Pitfall: Daily-scan producer writes phantom paths to candidates_new.txt (2026-07-12)

**Sintoma**: Pipeline-semanal F1.0 carrega `candidates_new.txt` (producido pelo
`daily-scan`). Evaporation guard dropa TODOS os 77 paths — nenhum existe no disco.
Recovery scan é forçado, rerodando F1.0b completo desnecessariamente.

**Causa**: O `daily-scan` (produtor) escaneia diretórios que podem não existir
no ambiente atual. Neste caso, `.raw/articles/` foi removido/movido em run
anterior, mas o `daily-scan` ainda grava paths como `.raw/articles/X.md` no
snapshot. O `f10b_scan.py` não valida `[ -f "$f" ]` antes de escrever o path
no arquivo de output.

**Diagnóstico**:
```bash
# Verificar se paths no snapshot existem
MISSING=0
while IFS= read -r f; do
  [ -f "$f" ] || MISSING=$((MISSING+1))
done < 06-GENERATED/tasks/candidates_new.txt
echo "Phantom paths: $MISSING / $(wc -l < 06-GENERATED/tasks/candidates_new.txt)"
# Se MISSING > 50% do total, o snapshot é unreliable — force recovery
```

**Fix (producer-side)**: `daily-scan` deve validar `[ -f "$f" ]` antes de
escrever cada path no snapshot. Paths inexistentes não devem entrar no arquivo.
Alternativa: o `f10b_scan.py` deve fazer `os.path.exists()` check antes de
append ao output.

**Fix (consumer-side)**: O evaporation guard no pipeline-semanal F1.0b já
dropa paths inexistentes — isto é correto. Mas quando 100% dos paths são
phantoms, o pipeline deve logar isto como anomalia (não como normal evaporation)
e flagar o `daily-scan` como bugado.

**Diferenciação**: evaporation normal = arquivos somem DEPOIS do scan (Readwise
sync, iCloud). Phantom paths = arquivos NUNCA existiram no momento do scan
(diretório escaneado não existe). Evaporation guard não distingue os dois —
ambos são dropados silenciosamente. Phantom paths indicam bug no produtor,
evaporation indica race condition benigno.

**Evidência**: pipeline-semanal 2026-07-12, 77 paths no snapshot do daily-scan,
todos referenciando `.raw/articles/` (diretório inexistente). Recovery scan
encontrou 126 files reais em `.raw/` + `00-INBOX/clippings/`, 71 genuinely new.

## Pitfall: `10X` regex matches tech content "10x" as clickbait (2026-07-11)

**Sintoma**: 7 arquivos legítimos de tech content (ex: "10x lower cost") falsamente
classificados como junk pelo gate G2 porque o regex `10X` (sem word boundary,
case-insensitive no Python `re.I`) matchava "10x" em contextos técnicos.

**Causa**: No `batch_score.py`, o pattern `JUNK_PATTERNS` tinha `10X` sem `\b`
(word boundary), e o regex era compilado com `re.I` (case-insensitive). "10x lower
cost" em artigos de token economy / cost optimization é conteúdo legítimo, não
clickbait "10X productivity" ou "10X your revenue".

**Fix aplicado (portado p/ skill 2026-07-11)**: `10X` → `(?-i:\b10X\b)` nesta skill
(regra Python e bash na seção Extended Title Patterns). O `\b` = word boundary (não matcha "10x"
dentro de "10x lower cost"); `(?-i:...)` desliga o `re.I` só nesse token → case-sensitive,
matcha capital "10X" (clickbait), não lowercase "10x" (notação técnica). Antes vivia só
em `/tmp/batch_score.py` (volátil) — agora persistido na skill. Testado 5/5.

**Lição**: patterns de clickbait que coincidem com notação técnica (10X vs 10x,
"escape wage" vs "escape sequence") precisam de word boundary `\b` E verificação
de case. Notação técnica em lowercase ("10x faster", "10x cheaper") é legit;
hype em uppercase ("10X your results", "10X productivity") é clickbait.

**Evidência**: pipeline-semanal 2026-07-11, 296 candidatos, 7 falsos positivos
iniciais corrigidos, 0 disapproved final (100% approval legítima — Readwise-curated).

---

