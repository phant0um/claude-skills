---
status: active
parent: "[ingest-proposal](SKILL.md)"
kind: reference
name: reference-ingest-proposal
type: skill-reference
reviewed-scope: "W3c 2026-10-10: poda de 2 pitfalls cobertos (daily-scan, ingest-verify C2/C8), 1 coberto por teste (manifest key) e historico; templates e comandos intactos"
reviewed-by: claude-opus-5
reviewed: 2026-09-20
updated: 2026-09-17
---

## Contents

- Templates (F2.3a / F2.3b)
- Comandos de Execução
- Pitfalls (runs 2026-06-23/24)

## Templates

### F2.3a — Artigos / ai-agents / concurso

`concurso`: source page em `02-AREAS/concurso/sources/<slug>.md`, link entity em
`02-AREAS/concurso/entities/<entity>.md` (concepts seguem em `03-RESOURCES/concepts/`).

Referência: `08-ARCHIVE/system/rotinas/pipeline-semanal.md` § F2.3a (rotina arquivada; a viva é o workflow `pipeline-drain`).

```markdown
---
title: <Title from H1 or filename>
type: source
source: <path>
created: YYYY-MM-DD
ingested: <today>
tags: [<category>]
---

## Tese central
<1-3 frases: argumento principal + contexto necessário para entender sem ler o original>

## Argumentos principais
<Lista completa — preservar nuances, não truncar>

## Key insights
<Todos os insights relevantes — sem cap de número>


## Self-Improvement

Após cada execução com output significativo:
1. Se usuário corrigir output → `/meta-learn` extrai princípio (não regra)
2. Se padrão recorrente de erro (≥2×) → flag para `hill-climb` com contexto
3. Lições append em `06-GENERATED/tasks/lessons.md` (formato: `- YYYY-MM-DD: [<slug>] <observação>`)

> Ver: [meta-learn](../evolve/meta-learn.md) · [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop
## Exemplos e evidências
<Dados concretos, casos, benchmarks, citações>

## Implicações para o vault
<O que muda, contradiz ou confirma em conhecimento existente>

## Links
- <kw>
- <entity> (ou `02-AREAS/concurso/entities/<entity>` se categoria=concurso)
```

### F2.3b — FIAP (material de estudo)

Referência: `08-ARCHIVE/system/rotinas/pipeline-semanal.md` § F2.3b (arquivada — ver nota em F2.3a).

Source page em `02-AREAS/fiap/sources/<slug>.md`, entity de fase em
`02-AREAS/fiap/entities/fiap-<fase-slug>.md`.

**Princípio**: preservar completamente — é material de estudo, condensar = perda.
Ler snippet completo (8000 chars). Incluir todos os conceitos. Não limitar a 5.

```markdown
---
title: <Título do material>
type: study-material
source: .raw/fiap/<fase>/<filename>
created: YYYY-MM-DD
ingested: <today>
tags: [fiap, study-material, <fase-slug>]
fiap_fase: <Fase N — Nome>
---

## Tese central
<O que este material ensina e por que importa para a formação>

## Conceitos-chave
<Todos os conceitos presentes — sem limite fixo — com definição técnica>
1. **<Conceito>**: <definição técnica completa + exemplo concreto>
2. ...

## Exemplos práticos
<Código, diagramas, fluxos — preservar completo e funcional>

## Notas Especialistas Dev/TI
- **Implementação prática**: <como usado em projetos reais>
- **Padrões de mercado**: <ferramentas/frameworks que aplicam este conceito>
- **Armadilhas comuns**: <o que estudantes erram>
- **Por que importa**: <relevância no mercado>

## Exercícios / Autoavaliação
<Se contiver exercícios: preservar enunciados e gabaritos>

## Links
- <kw>
- fiap-<fase-slug>
```

## Comandos de Execução

### Bash — Classificação + snippet

```bash
> /tmp/classify.txt

while IFS='|' read -r f interest domain; do
  [[ -z "$f" ]] && continue
  interest="${interest:-core}"  # fallback se linha sem tag
  bn=$(basename "$f" .md); bn=$(basename "$bn" .pdf)
  slug=$(echo "$bn" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')

  if echo "$f" | grep -qi "fiap\|fase-"; then
    READ_LIMIT=12000; CATEGORY="fiap"
  else
    READ_LIMIT=8000; CATEGORY="articles"
  fi

  if echo "$bn" | grep -qiE "claude|cowork|skill|mcp|agent|llm|rag|prompt"; then CATEGORY="ai-agents"
  elif echo "$bn" | grep -qiE "concurso|portugue|logica|redacao"; then CATEGORY="concurso"
  fi

  if [[ "$f" == *.pdf ]] && command -v liteparse &>/dev/null; then
    liteparse "$f" --max-chars $([ "$CATEGORY" = "fiap" ] && echo 8000 || echo 5000) > /tmp/snippet_$slug 2>/dev/null
  else
    head -c $READ_LIMIT "$f" | CLEAN | head -c $([ "$CATEGORY" = "fiap" ] && echo 8000 || echo 5000) > /tmp/snippet_$slug
  fi

  echo "$f|$slug|$CATEGORY|$interest" >> /tmp/classify.txt
done < /tmp/candidates_aprovados.txt
```

> `interest` propaga para classify.txt → gates F2.9/F2.10 (só `core`) e archive.

### Bash — Concept lookup (bash-first)

```bash
ls 03-RESOURCES/concepts/ 03-RESOURCES/entities/ > /tmp/existing.txt
for kw in $KEYWORDS; do
  grep -qi "^${kw}.md$\|^${kw}-" /tmp/existing.txt && echo "$kw=exists" || echo "$kw=new"
done
```

AI call só se ambíguo. **Cost: ~0–100 tokens.**

### AI Call — Source page generation

Por categoria (perfil `untrusted-ingest`, HR1):
- `articles/ai-agents/concurso` → template F2.3a
- `fiap` → template F2.3b

### Bash — Manifest append (atômico)

**Dedup-gap fix (v1.4.0):** manifest key DEVE ser o basename exato do arquivo
em Clippings/ (com extensão `.md`). Isto alinha com F1.0b scan que procura por
`"basename"` (com aspas coladas). Antes usava `jq --arg k "$bn"` onde `$bn`
vinha de `basename "$f"` (com extensão) mas F1.0b grep procurava sem extensão
— mismatch causava falsos positivos (19/19 em 2026-06-17).

```bash
while IFS='|' read -r f slug category interest; do
  bn=$(basename "$f")  # EX: "The Log Is the Agent.md" — COM extensão
  bn_noext="${bn%.*}"   # "The Log Is the Agent" — sem extensão (fallback)
  _hash=$(md5 -q "$f" 2>/dev/null || md5sum "$f" | cut -d' ' -f1)
  case "$category" in
    fiap) _dir="02-AREAS/fiap/sources" ;;
    concurso) _dir="02-AREAS/concurso/sources" ;;
    *) _dir="03-RESOURCES/sources" ;;
  esac
  _page="${_dir}/${slug}.md"

  # Registra AMBAS as variantes de key (com e sem extensão) para máxima
  # compatibilidade com F1.0b grep (que testa múltiplos formatos)
  jq --arg k "$bn" --arg k2 "$bn_noext" --arg h "$_hash" --arg d "$(date -I)" \
     --arg c "$category" --arg p "$_page" --arg i "${interest:-core}" \
     '.sources[$k] = {hash: $h, ingested_at: $d, category: $c, interest: $i, pages_created: [$p]}
    | .sources[$k2] = {hash: $h, ingested_at: $d, category: $c, interest: $i, pages_created: [$p], alias_of: $k}' \
     .raw/.manifest.json > /tmp/manifest.tmp && mv /tmp/manifest.tmp .raw/.manifest.json
done < /tmp/classify.txt
```

### Bash — Mover approved para archive

Só approved chega ao ingest (disapproved já foi movido pela triagem). Após ingest completo:

```bash
ARCH="08-ARCHIVE/approved/$(date -I)"; mkdir -p "$ARCH"
while IFS='|' read -r f interest domain; do
  [[ -z "$f" ]] && continue
  mv "$f" "$ARCH/" 2>/dev/null && echo "→ approved ($interest): $(basename "$f")"
done < /tmp/candidates_aprovados.txt
```

## Pitfall: Subagent manifest update failure — 2026-06-24

**Sintoma**: subagente reportou "manifest updated with 80 entries" mas verificação
mostrou 0 entries novas para aquele batch.

**Causa**: subagente pode ter falhado ao executar jq/Python sem reportar erro,
ou usado campo de data diferente (`ingested` vs `ingested_at`).

**Fix**: orquestrador deve validar manifest após cada subagente completar:
```python
today_count = sum(1 for k,v in manifest['sources'].items()
                  if isinstance(v,dict) and v.get('ingested_at') == TODAY)
if today_count < expected:
    # Run fix script to add missing entries
```

**Prevenção**: instructions do subagente devem incluir: (1) usar `ingested_at` como
field name, (2) key = basename only (não path), (3) ambos variantes com e sem .md.

Histórico de versões: `git log` deste arquivo.
