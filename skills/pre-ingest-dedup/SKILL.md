---
status: active
kind: skill-proc
name: pre-ingest-dedup
skill: pre-ingest-dedup
version: 1.7
tags: [hook, dedup, pre-ingest, clippings, quality, bash, dedup-gap, retroactive-manifest]
type: skill
resolver-status: not-exposed  # design do hook; quem roda e o .sh instalado, nao esta pagina
updated: 2026-11-10
description: "Use when: Hook Design: pre-ingest-dedup — Detectar arquivos duplicados ou quasi-duplicados antes que entrem em 00-INBOX/clippings/ ou .raw/. Motivação: triagem 2026-05-23 detectou dois arquivos `colbymchenrycodegraph` com basenames similares — versão sem He..."
reads:
  - 00-INBOX/clippings/.manifest.json
  - 00-INBOX/clippings/
writes:
  - 00-INBOX/clippings/.manifest.json
triggers:
  positive: ["escrita em 00-INBOX/clippings/ ou .raw/", "hook PostToolUse de dedup"]
  negative: ["arquivo único importado manualmente", "traduções EN/PT complementares", "versões intencionalmente diferentes (v1 vs v2)"]
consumes: ["clipping", "manifest"]
tools: ["bash"]
references:
  - 04-SYSTEM/automation/skills/pipeline/pre-ingest-dedup/reference
verifier: ["Require detecção de duplicata reportada e retroactive manifest entry quando houver gap."]
human_gate: false
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7: corpo completo lido pelo shield (opus, somente leitura); W7a: exit 2, stdin e writes do manifest alinhados ao hook instalado; checks frontmatter/lint/evals verdes; 205 linhas, 8 secoes"
---



# Hook Design: pre-ingest-dedup

Detectar arquivos duplicados/quasi-duplicados antes de entrarem em `00-INBOX/clippings/` ou `.raw/`. Inclui dedup-gap pattern (manifest check vs source page existence) e retroactive manifest entry.

> Edge cases, pitfalls datados e histórico → [reference](reference.md)

## Propósito

Detectar arquivos duplicados ou quasi-duplicados antes que entrem em 00-INBOX/clippings/ ou .raw/. Motivação: triagem 2026-05-23 detectou dois arquivos `colbymchenrycodegraph` com basenames similares — versão sem Hermes Agent e versão com Hermes Agent. Sem dedup, ambos entram e um é descartado manualmente.

## Tipo de Hook

**PostToolUse** — dispara após qualquer escrita em `00-INBOX/clippings/` ou `.raw/`.

Alternativa mais efetiva: **hook de download/importação** no Readwise ou web clipper (pré-vault). Mas como não há controle sobre importadores externos, o hook fica no vault.

## Quando NÃO Usar

- Arquivo único importado manualmente (check visual mais rápido)
- Traduções do mesmo artigo (EN/PT) — complementares, não duplicatas
- Versões intencionalmente diferentes do mesmo projeto (v1 vs v2)
- Quando importador externo já faz dedup (verificar antes de ativar)
- Objetivo de VALIDAR conteúdo/clipping (completeness, wikilinks, tese) → usar [ingest-verify](../ingest-verify/SKILL.md).
- Dedup de outputs gerados (06-GENERATED) — o hook cobre apenas entradas (00-INBOX/clippings/ e .raw/), não artefatos gerados.
- Base canônica inexistente (nenhum manifest de clippings/.raw) — sem base de comparação não há dedup.

## Implementação Sugerida

### Lógica de Detecção

1. Checar exact match no manifest e prefix similarity do basename (40 chars).
2. Cross-check do campo `source` das source pages existentes (F1.0c).
3. Quando o manifest falha, checar a source page por slug antes de declarar candidato novo.
4. Detectar quasi-duplicatas com slug normalization e file evaporation (arquivo some entre find e processamento).
5. Emitir só os candidatos genuinamente novos.

```bash
#!/bin/bash
# pre-ingest-dedup.sh
# Ilustrativo. O hook instalado (04-SYSTEM/system/hooks/pre-ingest-dedup.sh) lê tool_input.file_path do JSON em stdin e não bloqueia.
# Neste exemplo: $1 = path do arquivo recém-adicionado

NEW_FILE="$1"
NEW_BASENAME=$(basename "$NEW_FILE" .md)

# 1. Exact match no manifest
MANIFESTS=(
  "~/Obsidian/vault-michel/.raw/.manifest.json"
  "~/Obsidian/vault-michel/00-INBOX/clippings/.manifest.json"
)
for manifest in "${MANIFESTS[@]}"; do
  if grep -qF "\"$(basename "$NEW_FILE")\"" "$manifest" 2>/dev/null; then
    echo "DEDUP: exact match '$(basename "$NEW_FILE")' já no manifest" >&2
    exit 2  # alerta ao agente: PostToolUse não bloqueia (a escrita já ocorreu)
  fi
done

# 2. Prefix similarity (primeiros 40 chars do basename)
PREFIX="${NEW_BASENAME:0:40}"
EXISTING=$(find ~/Obsidian/vault-michel/00-INBOX/clippings/ \
  -maxdepth 1 -name "*.md" | while read f; do
    bn=$(basename "$f" .md)
    [[ "${bn:0:40}" == "$PREFIX" ]] && echo "$f"
  done)

if [[ -n "$EXISTING" ]]; then
  echo "DEDUP WARNING: basename similar detectado:" >&2
  echo "  Novo:      $NEW_BASENAME" >&2
  echo "  Existente: $(basename "$EXISTING" .md)" >&2
  echo "  Ação: comparar manualmente antes de prosseguir" >&2
  # Não bloquear (exit 0) — só alertar. Usuário decide.
fi

exit 0
```

Prefix-match nos primeiros 40 chars captura o caso `colbymchenrycodegraph...` (com/sem Hermes Agent). Não detecta títulos completamente diferentes cobrindo mesmo conteúdo — precisaria embedding similarity (fora do escopo). Detalhe em reference.

### Registro em settings.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "command": "bash ~/Obsidian/vault-michel/04-SYSTEM/system/hooks/pre-ingest-dedup.sh"
      }
    ]
  }
}
```

> **Nota:** o hook instalado recebe o JSON do hook em stdin (`tool_input.file_path`), sem argv. Implementação exata depende da API de hooks do Claude Code. Verificar `~/.claude/settings.json` formato atual antes de configurar.

## Dedup-Gap Pattern (core)

F1.0b manifest check declara arquivo como "novo" quando já foi ingerido antes (source page criada + original movido para `08-ARCHIVE/A/`, mas manifest entry ausente ou com key divergente). Resultado: re-triagem, desperdício de tokens. Padrão recorrente desde 2026-06-10, não exceção.

### Fix: Second-Pass Source-Page Check

Após manifest check falhar (arquivo parece "novo"), verificar se source page já existe por slug antes de declarar candidato:

```bash
# Após /tmp/candidates_new.txt gerado
> /tmp/candidates_truly_new.txt
while IFS= read -r f; do
  bn=$(basename "$f" .md)
  # Slug normalizado (igual ao que wiki-ingest cria)
  slug=$(echo "$bn" | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' | tr -s '-' | sed 's/^-//;s/-$//')
  # Buscar source page existente pelo slug (50 chars — ver tuning em reference)
  found=$(find 03-RESOURCES/sources/ -iname "*${slug:0:50}*" -type f 2>/dev/null | head -1)
  if [ -n "$found" ]; then
    echo "RETRO:$f:$found" >> /tmp/retroactive_manifest.txt
  else
    echo "$f" >> /tmp/candidates_truly_new.txt
  fi
done < /tmp/candidates_new.txt
```

Reduz falsos positivos em ~90% quando o dedup-gap está ativo.

### Retroactive Manifest Entry (formato)

Quando source page existe mas manifest entry falta, adicionar retroativamente:

```python
sources[basename] = {
    "hash": "batch-moved",
    "ingested_at": "2026-06-16",
    "category": "articles",  # ou "concurso", "fiap"
    "pages_created": [page_path],
    "note": "article — source page exists, retroactive manifest entry",
    "path_corrected_at": "2026-06-16"
}
```

Para concurso aulas (`curso-NNNNN` pattern), usar `category: "concurso"`, `pages_created: [materia_path]` e note referindo `curso-{cid}`. Concurso-specific dedup e demais variantes em reference.

## File Evaporation Pattern (core)

`find` escaneia 00-INBOX/clippings/ e gera candidatos, mas entre scan e processamento arquivos somem do disco (Readwise sync, Obsidian sync, pipeline anterior). Sintoma: `[ -f "$f" ]` false, `cp` falha silenciosa, "0 files ingested".

```bash
EXISTING=0; MISSING=0
while IFS= read -r f; do
  [ -f "$f" ] && EXISTING=$((EXISTING+1)) || MISSING=$((MISSING+1))
done < /tmp/candidates_new.txt
echo "Existing: $EXISTING, Missing: $MISSING"
```

**Mitigação:** não tratar como erro — é sinal de que processamento retroativo é necessário (manifest entry + source page check). Diagnóstico completo em reference.

**Critério de sucesso:** saída contém só candidatos genuinamente novos, com cross-check de source e file evaporation verificados.

## Completion

- [ ] Dedup por basename similarity executada (F1.0)
- [ ] Cross-check campo source: das source pages existentes (F1.0c)
- [ ] Quasi-duplicatas com slug normalization verificadas
- [ ] File evaporation detectada (arquivos somem entre find e processamento)
- [ ] Output: lista de candidatos genuinely novos (não duplicatas)

## Failure modes

- **Basename-only check**: só comparar basename × manifest → slug temático divergente passa (F1.0c obrigatório)
- **Slug quoting bug**: inline python3 -c com regex quebra no macOS bash 3.x → usar arquivo externo
- **File evaporation misdiagnosis**: arquivos somem por Readwise sync, não por bug → confirmar antes de debugar
- **Short slug match**: slug < 40 chars gera falsos negativos no second-pass → usar 40+ chars ou fuzzy match

> Pitfalls datados (manifest key dual-registration, slug prefix tuning, hidden/system files, shell var persistence, approved-but-not-ingested gap) + changelog → [reference](reference.md)

