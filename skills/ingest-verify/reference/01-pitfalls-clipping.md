---
status: active
parent: "[ingest-verify](../SKILL.md)"
kind: reference
name: ingest-verify-01-pitfalls-clipping
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 3/3 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 6 secoes, 198 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [C2 pitfalls — wikilink resolution](#c2-pitfalls-wikilink-resolution)
- [C3 pitfalls — Tese Central contains Clipping frontmatter bruto (2026-07-05)](#c3-pitfalls-tese-central-contains-clipping-frontmatter-bruto-2026-07-05)
- [C7 / C9 pitfalls — Personal Reflection & Placeholder](#c7-c9-pitfalls-personal-reflection-placeholder)
- [C10 pitfalls — categorização](#c10-pitfalls-categorização)
- [C8 pitfall — Batch Link Integrity](#c8-pitfall-batch-link-integrity)


> Seção fatiada de [ingest-verify](../SKILL.md). Carregar sob demanda: pitfalls C2/C3/C7/C9/C10/C8 (wikilinks, tese central, placeholder, categorização).

## C2 pitfalls — wikilink resolution

**Pitfall (2026-06-23 run 2):** 224/1215 wikilinks (18%) não resolviam porque o
ingest script gerou paths que não existem no filesystem. O check C2 deve:
1. Extrair todos `link` que apontam para `03-RESOURCES/concepts/` ou `03-RESOURCES/entities/`
2. Para cada link, verificar se `vault_path/link.md` existe
3. Se >5% links quebrados → FAIL (não PASS com warning). Abortar batch e reparar.
4. Reportar lista de links quebrados para reparo imediato

**Pitfall (2026-06-24):** Spot-check com `os.path.isfile()` reportou "6/6 broken"
mas verificação completa do batch com stem/basename matching mostrou 0 broken.
Causa: wikilinks gerados com paths como `agent`
não existem como path exato, mas o arquivo `concepts/agent-systems/agent.md` existe
e o Obsidian resolve por basename (não por path completo). O check C2 deve
sempre fazer fallback por basename (stem lookup) antes de reportar "broken":
```python
# 1. Try exact path
if os.path.isfile(f"{vault}/{link}.md"): continue
# 2. Try basename fallback
stem = link.rsplit('/', 1)[-1]
for root, _, files in os.walk("03-RESOURCES/concepts/"):
    if f"{stem}.md" in files: break  # resolves via Obsidian basename
else:
    broken.append(link)  # truly broken
```
Isto evita falsos positivos de "broken" que disparam repair desnecessário.

---

## C3 pitfalls — Tese Central contains Clipping frontmatter bruto (2026-07-05)

**Sintoma**: 313 source pages com `## Tese Central` contendo metadata bruta do
Clipping original (`author:`, `source:`, `published:`, `original_title:`, `---`).
O `generate_tese()` do `batch_enrich.py` extrai "first content paragraph" mas não
filtra linhas de metadata embutidas no body do Clipping.

**Causa**: 00-INBOX/clippings do Readwise/web clipper embedem frontmatter YAML no corpo
do artigo. Quando `generate_tese()` pega as primeiras linhas não-`#` e não-`---`,
ele captura `author: @user` e `source: https://...` como se fosse conteúdo.

**Fix aplicado (2 etapas)**:

1. **Prevenção** — patch em `batch_enrich.py generate_tese()`: após extrair body,
   verificar se começa com `---` (embedded frontmatter) e fazer skip. Filtrar
   linhas que começam com `title:`, `type:`, `created:`, `updated:`, `tags:`,
   `source:`, `author:`, `published:`, `original_title:`, `---`.

2. **Correção retroativa** — script Python que para cada file com Tese Central
   contaminada: extrai primeiro parágrafo real do corpo do artigo (após Tese Central
   + Resumo sections), filtra metadata lines, pega 2 primeiras sentenças.
   309 files corrigidos de 313 detectados (4 não tinham conteúdo real extraível).

**Lição**: C3 (Tese Central check) deve verificar não apenas presença da seção,
mas também se o conteúdo NÃO começa com patterns de metadata (`author:`, `source:`,
`published:`, `---`). Se começar → C3 FAIL com "Tese Central contains metadata, not
content".

---

## C7 / C9 pitfalls — Personal Reflection & Placeholder

**Placeholder Detection (Pitfall 2026-06-23 run 2):** 100 source pages com
`## Minha Síntese` contendo apenas "A ser analisado em revisão manual" passaram
pelo C7. C9 foi adicionado para detectar conteúdo placeholder.

### F2.9 prose format + variable Relations anchor — 2026-07-05 batch

**Sintoma**: Batch de 50 source pages processadas com formato F2.9 prosa
(2-4 linhas sem bold labels) ao invés do formato estruturado (`**O que muda**`,
`**Conexão pessoal**`, `**Próximo passo**`). C7 original reportaria WARN falso
em todas — o formato prosa é válido e foi requestado explicitamente pelo usuário.

**Causa**: C7 hardcoded o formato estruturado como único aceitável. O usuário
pode requestar "2-4 linhas sobre: o que muda, conexão, próximo passo" sem
labels bold — formato legível e válido.

**Fix**: C7 agora aceita dois formatos — structured (bold labels) e prose
(≥2 linhas de conteúdo após heading). Verificação de linha de conteúdo
detecta prosa válida sem exigir labels.

**Segundo issue**: o anchor `## Relations\n- zyphra-2 — shared tag: ai-agents, source`
não é universal. Source pages de 00-INBOX/clippings (não-pipeline) têm Relations
diferentes (`signal-the-key-to-self-healing-software`, `wildclawbench-...`)
ou nenhuma seção Relations. Patches append-only devem:
1. Ler o arquivo completo antes de patch
2. Identificar o anchor real (última seção `## Relations` ou último `## Links`)
3. Adaptar o old_string ao anchor real, não assumir `zyphra-2`

**Lição**: nunca assumir um anchor fixo para append em batch de source pages
de origens variadas (pipeline-semanal vs 00-INBOX/clippings vs manual). Sempre ler
primeiro e adaptar o patch ao conteúdo real.

### F2.9 cap misunderstood — pipeline allows 50/subagent, not 3/run — 2026-07-05

**Sintoma**: Backlog F2.9 reportado como 534 Score A files sem Minha Síntese. O
operador impôs cap artificial de 3 reflections por run, tratando como limitação
do pipeline. Na verdade, o pipeline F2.9b permite até 50 files por subagentente
e recomenda split em batches ≤50 quando backlog >80.

**Causa**: O cap de 3/run foi confundido com limitação do pipeline. O pipeline
F2.9b é um **batch-sizing guard**, não um rate limiter. O guard decide quantos
subagentes despachar (1 se ≤50, 2 se 51-100, waves se >100), não quantas
reflections escrever por run.

**Fix**: Despachar 3 subagentes paralelos com 50 files cada (150 total) via
`delegate_task tasks=[]`. Backlog 534 → 384 residual após batch. Próximas
rodadas atacam o residual em waves de 150.

**Lição**: ao ler specs de pipeline, distinguir entre:
- **Batch-sizing guards** (quantos despachar por vez) — F2.9b
- **Rate limiters** (quantos fazer por run) — não existe no pipeline
- **Quality caps** (máx por arquivo/subagent) — F2.9 não tem

O backlog de 534 era parcialmente auto-infligido pelo cap errado. Sem o cap,
4 runs de 150 zerariam o backlog.

### F2.9 batch sizing — 50 files/subagent times out, 25 is sweet spot — 2026-07-06

**Sintoma**: 3 subagentes despachados com 50 files cada para F2.9 reflections.
2/3 timed out at 600s (com 13-14 API calls). 1 completou 50/50 mas levou 530s.
Re-dispatch com 25 files/subagent completou 75/75 em 53-305s.

**Causa**: F2.9 Personal Reflection parece simples (read + 2-4 linhas + patch)
mas cada file exige: 1 API call para ler source page + 1 API call para gerar
reflection + 1 patch tool call. Com 50 files, são ~150 tool calls sequenciais.
O bottleneck é latência cumulativa de API round-trips, não complexidade.

**Fix**: batch size 25 files/subagent para F2.9 enrichment. 3 subagentes × 25
= 75 files por wave. Backlog de 534 zerado em ~4 waves (~20 min total).

**Lição**: o pipeline F2.9b recomenda ≤50 files/subagent, mas empiricamente
25 é o sweet spot confiável. 50 funciona apenas para articles curtos; para
papers densos (ml-research-papers, guides-courses-howtos), 25 é mais seguro.

---

## C10 pitfalls — categorização

**Pitfall (2026-06-23 run 2):** 74/230 source pages miscategorizadas como
"concurso" porque a função `categorize()` do batch_ingest.py matchava
`fiscal` e `tribut` isoladamente. Isto moveu papers para
`02-AREAS/concurso/sources/` incorretamente.

> **Reference**: `references/loose-file-categorization.md` — cascade 3-tier (frontmatter
> `category:` → keyword → fallback) p/ mover source pages soltas de `03-RESOURCES/sources/`
> root p/ subdirs temáticos. Zero AI, 564 files/1s. Rodar quando C10 flagar misplaced em massa.

### GitHub README ingest — miscategorization by README content keywords — 2026-06-28

**Sintoma**: 21 GitHub repo READMEs ingestados. 2 miscategorizados:
- JavaGuide → `memory-context-rag` (README menciona "memory" em contexto JVM)
- llm-course → `financial-trading` (README menciona "stock" em examples)

**Causa**: `categorize()` faz keyword matching no conteúdo do README. READMEs de
repos técnicos frequentemente mencionam keywords de outros domínios em exemplos,
seções de "related projects", ou metadata. Um README sobre Java menciona "memory"
(JVM heap) e um curso de LLM usa "stock market prediction" como exemplo.

**Fix**: Para READMEs de GitHub repos, a categorização deve pesar o TÍTULO do repo
e a descrição do GitHub API (`gh api repos/owner/repo --jq '.description'`) mais
que o conteúdo do README. Ou usar a tag `source: "gh:repos/..."` no frontmatter
para identificar READMEs e aplicar categorização mais conservadora.

**Evidência**: 21 repos baixados via `gh api`, 2/21 miscategorizados (9.5%).
Fix aplicado: mover arquivos para categoria correta + atualizar frontmatter.

---

## C8 pitfall — Batch Link Integrity

**Pitfall (2026-06-23 run 2):** 224/1215 links (18%) quebrados passaram pelo C2
individual porque C2 só reporta WARN (não FAIL). C8 (batch link integrity) foi
adicionado para catchar o problema no nível do batch.

---

