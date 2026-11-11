---
status: active
parent: "[ingest-verify](../SKILL.md)"
kind: reference
name: ingest-verify-03-pitfalls-batch-ingest
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 2/2 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 7 secoes, 200 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Pitfall: Batch ingest programmatic wikilinks — 2026-06-28](#pitfall-batch-ingest-programmatic-wikilinks-2026-06-28)
- [Pitfall: Batch ingest link path mismatch — 2026-06-23 (Run 2)](#pitfall-batch-ingest-link-path-mismatch-2026-06-23-run-2)
- [Pitfall: F2.10 False-positive wikilinks from article content — 2026-06-28](#pitfall-f210-false-positive-wikilinks-from-article-content-2026-06-28)
- [Pitfall: Subagent link path mismatch — concepts/X vs concepts/agent-systems/X — 2026-06-30](#pitfall-subagent-link-path-mismatch-conceptsx-vs-conceptsagent-systemsx-2026-06-30)
- [Pitfall: Retroactive manifest enrichment — 504 entries sem ingested_at — 2026-06-30](#pitfall-retroactive-manifest-enrichment-504-entries-sem-ingested_at-2026-06-30)
- [Pitfall: Mapping script false negatives — slug matching para comprehensive reports — 2026-06-30](#pitfall-mapping-script-false-negatives-slug-matching-para-comprehensive-reports-2026-06-30)


> Seção fatiada de [ingest-verify](../SKILL.md). Carregar sob demanda: pitfalls de batch ingest programático (wikilinks, path mismatch, F2.10).

## Pitfall: Batch ingest programmatic wikilinks — 2026-06-28

**Sintoma**: 722 source pages criadas via script Python. Wikilinks gerados por keyword matching
apontam para paths como `agent-evaluation` que não
existem no filesystem. F2.10 reportou 32.1% broken links (159/496).

**Causa**: o script de ingest gera wikilinks com paths pré-determinados (`link_keywords` dict)
que não correspondem à estrutura real de subdiretórios do vault. O vault tem 471 concepts
em 16 subdirs e 339 entities — paths não são previsíveis.

**Fix aplicado (3 etapas)**:
1. Construir índice basename→full_path de TODOS os concepts/entities em 1 pass
2. Coletar broken links únicos (após basename fallback)
3. Criar concept/entity stubs NO PATH EXATO do link (não no path "correto")
   - 8 stubs criados → 0.5% broken (3 falsos positivos: "Books.base" e "wikilinks" são
     conteúdo de texto em artigos sobre Obsidian, não wikilinks reais)

**Lição**: quando gerar wikilinks programaticamente em batch:
- SEMPRE verificar contra estrutura real do vault antes de escrever
- Repair é passo obrigatório pós-ingest, não opcional
- Falsos positivos do regex `...` existem — verificar se o "link" é conteúdo de texto
  (ex: artigos sobre Obsidian contêm `wikilinks` como exemplo de sintaxe)

## Pitfall: Batch ingest link path mismatch — 2026-06-23 (Run 2)

**Sintoma**: 230 source pages criadas por script Python batch. Wikilinks gerados
por keyword matching apontam para paths como `agent`
que não existem no vault. O vault tem `concepts/agent-systems/ai-agents.md` e
`entities/agent.md` — paths e estruturas diferentes.

**Causa**: O script de ingest gera wikilinks com paths pré-determinados
(`concept_map = {'agent': 'ai-agents', ...}`) que não correspondem à estrutura
real de subdiretórios do vault. O vault evoluiu organicamente com subdirs
como `agent-systems/`, `llm-ml-foundations/`, `memory-context-rag/` mas o
script assume `ai-agents/` como subdir.

**Impacto**: 
- Batch 1 subagent resolveu via basename matching (216 absorções em entities)
- Batch 2 subagent não resolveu nenhum (0 absorções — paths não bateram)
- Batch 3 só achou 2 que batiam exatamente
- 224/1215 wikilinks unresolved (18%) antes do repair

**Fix aplicado**: 
1. Script de repair mapeia broken links → existing files por basename
2. Concepts/entities faltantes criados como stubs NO PATH EXATO que o link
   referencia (não no path que o script acha "correto")
3. Verificação: 1215/1215 links resolvem (100%) após repair + stub creation

**Lição**: quando gerar wikilinks programaticamente, SEMPRE verificar contra
a estrutura real do vault antes de escrever. O vault tem 441 concepts em 16
subdirs e 323 entities — paths não são previsíveis. Duas opções:
1. **Pre-generation scan**: ler estrutura de subdirs antes de gerar links
2. **Post-generation repair**: gerar com paths plausíveis, depois reparar
   com script que faz basename matching + cria stubs nos gaps

A opção 2 é mais pragmática (não exige refatorar o script de ingest) mas
sempre executar o repair como passo obrigatório pós-ingest, não opcional.

**Pitfall secundário**: `CATEGORY_MAP = {'ai-agents': 'agent-systems'}` no script
de repair tentou criar stubs em `agent-systems/` mas os links apontam para
`ai-agents/`. O repair deve criar no path DO LINK, não no path "correto".
Verificar sempre com: `python3 -c "target = VAULT / f'{link}.md'; print(target.exists())"`

## Pitfall: F2.10 False-positive wikilinks from article content — 2026-06-28

**Sintoma**: F2.10 batch quality gate reports 32.1% broken links. After creating
stubs for 8 genuinely missing concepts/entities, re-verification still shows 21.8%
broken. Investigation: the remaining "broken" links are `wikilinks` and
`Books.base` — text inside article content ABOUT Obsidian syntax, not actual
wikilinks pointing to vault notes.

**Causa**: The regex `\[\[([^\]]+)\]\]` matches ANY `...` in the file content,
including inline code examples, quoted syntax demonstrations, and article text
that describes wikilink syntax. Articles about Obsidian/PKM naturally contain
`wikilinks` as examples.

**Fix**: When running F2.10 link integrity checks, exclude matches that are:
1. Inside inline code (backtick-wrapped): `` `wikilinks` ``
2. Inside code blocks (``` blocks)
3. Known syntax examples: `Books.base`, `wikilinks` — these are
   content describing Obsidian features, not vault references
4. Very short single-word targets that match common English words

**Implementation**: filter after regex extraction:
```python
# Remove inline-code wrapped matches
content_no_code = re.sub(r'`[^`]*\[\^+\]\][^`]*`', '', content)
# Remove code blocks
content_no_code = re.sub(r'```.*?```', '', content_no_code, flags=re.DOTALL)
# Then extract wikilinks from cleaned content
links = re.findall(r'\[\[([^\]]+)\]\]', content_no_code)
```

**Evidência**: pipeline-semanal 2026-06-28, 722 source pages. Initial F2.10
showed 159/496 (32.1%) broken. After creating 8 stubs for real missing targets,
re-check showed 108/496 (21.8%) broken. All remaining were false positives from
article content (`wikilinks`, `Books.base`). After filtering code blocks,
0 real broken links.

## Pitfall: Subagent link path mismatch — concepts/X vs concepts/agent-systems/X — 2026-06-30

**Sintoma**: 21 source pages criadas por 3 subagentes paralelos. F2.10 link
integrity check reportou 46/141 broken links (32.6%). Majoritariamente do
batch 3: concepts criados em `concepts/agent-systems/` mas linkados como
`concepts/X` (sem subdir).

**Causa**: Subagentes geram wikilinks com paths curtos (`vertical-ai`)
ao invés do path completo com subdir (`vertical-ai`).
O vault tem 117+ concepts em 16+ subdirs — paths não são previsíveis sem
consultar a estrutura real.

**Fix aplicado (3 etapas)**:
1. Script Python constrói índice basename→full_path de todos concepts/entities
2. Para cada broken link: buscar por basename em subdirs → rewrite link no
   source page com path correto
3. Para links truly missing: criar concept/entity stubs no path exato

**Resultado**: 15 links fixed (found in subdir), 30 stubs criados (16 concepts
+ 14 entities), 0 broken links após fix.

**Lição**: subagentes não conhecem a estrutura de subdirs do vault. O
post-ingest link repair é passo obrigatório, não opcional. O script de repair
deve:
1. Construir índice completo concepts + entities (basename → full_path)
2. Fazer case-insensitive lookup por basename
3. Criar stubs apenas para truly missing (após basename fallback)

**Diferença vs pitfall 2026-06-28**: aquele era sobre script Python de ingest
com paths pré-determinados. Este é sobre subagentes que geram paths curtos
sem saber o subdir. Mesma solução (post-ingest repair), causa diferente.

## Pitfall: Retroactive manifest enrichment — 504 entries sem ingested_at — 2026-06-30

**Sintoma**: 504 entries no manifest com `ingested_at: ""` (vazio). 68 aparecem
como "unknown" no mapeamento de 150 Clippings.

**Causa**: Runs pré-v4.0 (antes de 2026-06-09) não registravam `ingested_at`
no manifest. O campo existia mas ficava vazio. Batch_enrich.py assigna grades
nos arquivos mas não atualiza o manifest retroativamente.

**Fix**: Script Python `/tmp/retroactive_enrich.py`:
1. Para cada entry com `ingested_at` vazio: ler `source_page` frontmatter
   → extrair `ingested` ou `created` date
2. Se não tem source_page: tentar `pages_created[0]`
3. Fallback: setar explicitamente `"unknown"` (não vazio)
4. Para entries sem `grade`: ler `grade:` do source page frontmatter

**Resultado**: 425 dates preenchidos, 79 permanecem "unknown" (sem source page),
1222 grades assignados de source pages.

**Lição**: manifest retroativo enrichment é uma operação segura e de alto
valor. Backup do manifest antes de modificar é obrigatório. O script deve ser
idempotente — rodar múltiplas vezes não causa problemas.

## Pitfall: Mapping script false negatives — slug matching para comprehensive reports — 2026-06-30

**Sintoma**: Relatório comprehensive de 150 00-INBOX/clippings reportou 10 "source pages
não encontradas". 7 destas na verdade existiam com slugs diferentes.

**Causa**: Script de mapeamento usa `slug[:30] in md_file.stem.lower()` para
encontrar source pages. Para filenames longos ou com caracteres especiais,
o slug truncado não bate com o stem do arquivo real.

**Exemplo**: Clipping "How to Build Vertical AI that Actually Works w Christophe
Rimann" → slug `how-to-build-vertical-ai-that-actually-works-w-christophe-rimann`
→ source page criada pelo subagente como `build-vertical-ai-camber` (slug curto).
O slug[:30] (`how-to-build-vertical-ai-tha`) não matcha `build-vertical-ai-camber`.

**Fix**: Para relatórios comprehensive, usar manifest `source_page` field
diretamente ao invés de slug matching. O manifest é a fonte canônica de
verdade. Para entries sem `source_page` no manifest, fazer busca flexível por
keywords do título (não slug truncado).

**Lição**: slug matching é frágil para filenames longos. O manifest já tem
o caminho exato da source page — usar esse campo diretamente. Slug matching
só como fallback para entries sem manifest entry.

