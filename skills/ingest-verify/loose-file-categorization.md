---
status: active
parent: "[ingest-verify](SKILL.md)"
kind: reference
name: loose-file-categorization
type: reference
updated: 2026-07-26
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 6 secoes, 125 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [When to Use](#when-to-use)
- [⚠️ Nomes canônicos de pasta](#nomes-canônicos-de-pasta)
- [Cascade (stop at first match)](#cascade-stop-at-first-match)
- [Pitfalls](#pitfalls)
- [Script](#script)



# Loose File Categorization

3-tier cascade for moving loose source pages from `03-RESOURCES/sources/` root
into thematic subdirs. Zero AI calls. 564 files in 1s, zero errors.

## When to Use

After batch ingest that creates files in the sources root instead of subdirs,
or when auditing the vault for misplaced files.

## ⚠️ Nomes canônicos de pasta

Roteie **sempre** para o nome curto. Os nomes longos são resíduo de uma
reestrutura de 2026-07-13 que nunca foi concluída — esta tabela continuou
roteando para eles e recriando a duplicação:

| Canônico | Nunca usar |
|---|---|
| `ai-agents` | ~~`ai-agents-harness`~~ |
| `token-economy` | ~~`token-economy-cost`~~ |
| `llm-ml` | ~~`llm-ml-foundations`~~ |
| `pkm-obsidian` | ~~`pkm-obsidian-second-brain`~~ |
| `ml-research` | ~~`ml-research-papers`~~ |
| `open-source` | ~~`open-source-ecosystems`~~ |
| `guides` | ~~`guides-courses-howtos`~~ |
| `claude-code` | ~~`claude-code-tooling`~~ |
| `agent-systems` | ~~`ai-agents`~~ (em `concepts/`) |
| `articles` | ~~`articles-misc`~~ |

Critério: nome curto vence em inbound wikilinks nos 10 pares (`agent-systems`
12129 vs 357). Ver dedup-merge-2026-07-26.

## Cascade (stop at first match)

### Tier 1 — Frontmatter `category:` field

```python
cat_match = re.search(r'^category:\s*(.+?)$', content, re.MULTILINE)
if cat_match and cat.strip() in existing_subdirs:
    target_dir = cat.strip()
```

### Tier 2 — Tag matching

Map individual tags to thematic subdirs:

```python
tag_to_dir = {
    'ai-agents': 'ai-agents',
    'agent': 'ai-agents',
    'harness': 'ai-agents',
    'claude-code': 'claude-code-skills',
    'skill': 'skills-prompting-mcp',
    'mcp': 'skills-prompting-mcp',
    'memory': 'memory-context-rag',
    'rag': 'memory-context-rag',
    'llm': 'llm-theory',
    'transformer': 'llm-theory',
    'token': 'token-economy',
    'finance': 'financial-trading',
    'quant': 'financial-trading',
    'obsidian': 'pkm-obsidian',
    'pkm': 'pkm-obsidian',
    'arxiv': 'ml-research',
    'paper': 'ml-research',
    'open-source': 'open-source',
    'article': 'articles',
    # ... extend as needed
}
```

### Tier 3 — Content keyword matching

Scan first 3000 chars of file content for domain keywords:

```python
keyword_to_dir = {
    'ai-agents': ['agent', 'agentic', 'loop engineering', 'harness', 'autonomous'],
    'memory-context-rag': ['memory', 'rag', 'retrieval', 'context window', 'kv cache'],
    'llm-theory': ['transformer', 'attention', 'lora', 'fine-tun'],
    'llm-ml': ['inference', 'quantiz', 'speculative decoding', 'prompt caching', 'model routing', 'kv-cache'],
    'financial-trading': ['trading', 'quant', 'hedge fund', 'portfolio', 'stock'],
    'pkm-obsidian': ['obsidian', 'second brain', 'pkm', 'knowledge graph'],
    # ... etc
}
# Score by keyword frequency, pick highest scoring dir
```

### Fallback — `misc-low-confidence`

Files with no matchable metadata or content signals.

## Pitfalls

- **Tag substring false positives**: `'ai' in 'brain'` → match on full tags only,
  or require `len(tag) > 3` for substring matching.
- **Collision on move**: `os.path.exists(target_path)` → skip if already exists
  (don't overwrite existing file in target dir).
- **sources-index.md**: Always skip — stays in root as index file.

## Script

Full implementation: `scripts/batch_enrich.py` (future integration),
or inline `execute_code` in session (validated 2026-06-28: 564 files, 0 errors).
