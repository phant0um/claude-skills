---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: connection-finder
description: "Use when: varrer fontes dos últimos 7 dias contra o vault · procurar conexões cross-domain e contradições. Scan sources from last 7 days vs entire vault. Surface non-obvious cross-domain connections, contradictions, and converging patterns. Apply high-confidence wikilinks bidirectionally. report-synthesis só agrega receipts F1+F2 em relatório: varrer conexões depois de ingerir 5+ fontes, ou rodar a fase F2 da revisao-semanal de sábado, é aqui."
skill: connection-finder
version: 2.2
schedule: "sábado 5h (fase F2 de revisao-semanal)"
scheduler_task: revisao-semanal
tags: [routine, connections, cross-link, compounding]
sources:
  - CyrilXBT Connection Finder
  - DamiDefi JARVIS
updated: 2026-09-25
reads:
  - 03-RESOURCES/sources/
  - 03-RESOURCES/concepts/
  - 03-RESOURCES/entities/
writes:
  - 06-GENERATED/reports/connections/
  - 04-SYSTEM/system/state/context/hot.md
triggers:
  positive:
    - "@connection-finder"
    - "find connections"
    - "pós-ingest de 5+ fontes"
    - "revisao-semanal F2 (sábado 5h)"
  negative:
    - "varredura já feita no ciclo"
    - "fonte sem ## Tese"
    - "busca dirigida por tema conhecido"
consumes: ["sources-recentes", "concepts", "entities"]
tools: ["bash"]
references: []
verifier: ["Require wikilinks de alta confiança aplicados bidirecionalmente e contradições reportadas."]
human_gate: false
reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 3/3 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 13 secoes, 321 linhas; drift R13/R14: 1 achados resolvidos (decisoes D1-D4 A / SKILL_REF)"
reviewed-by: R15 (claude-sonnet; decisoes D1-D4 A)
reviewed: 2026-10-04
---

# Connection Finder

Scan sources from last 7 days vs entire vault. Surface connections humans wouldn't see.

---

## Trigger

- Scheduled: sábado 5h, fase F2 de revisao-semanal
- Manual e pós-ingest (5+ fontes): ver `triggers.positive` no frontmatter

---

## Execution

1. Coletar fontes recentes com `## Tese` e uma amostra aleatória do vault antigo.
2. Extrair temas das fontes recentes e casar com o vault antigo por overlap de tags.
3. Classificar as conexões e gerar o relatório, com no máximo 10.
4. Reparar links quebrados e criar stubs quando necessário.
5. Atualizar o hot cache e aplicar wikilinks só em alta confiança.

### 1. Collect recent sources

Prefer `ingested:` frontmatter field over `mtime -7` — mtime resets on git checkout/sync and produces false positives/negatives.

```bash
cd $VAULT_DIR
SEVEN_DAYS_AGO=$(date -v-7d -I 2>/dev/null || date -d '7 days ago' -I 2>/dev/null)
grep -rl "^ingested:" 03-RESOURCES/sources/ 2>/dev/null | while read f; do
  date=$(grep "^ingested:" "$f" | head -1 | sed 's/ingested: *//')
  if [[ "$date" > "$SEVEN_DAYS_AGO" ]]; then
    echo "$f"
  fi
done > /tmp/recent_sources_all.txt

# Tese-filter: source sem `## Tese` = stub/thin → polui pool com falsa convergência.
# Só entram no pool os que têm síntese central.
while read f; do grep -q "^## Tese" "$f" && echo "$f"; done < /tmp/recent_sources_all.txt > /tmp/recent_sources.txt
RECENT_COUNT=$(wc -l < /tmp/recent_sources.txt | tr -d ' ')
DROPPED=$(( $(wc -l < /tmp/recent_sources_all.txt) - RECENT_COUNT ))
[ "$DROPPED" -gt 0 ] && echo "Tese-filter: $DROPPED sources sem ## Tese excluídos do pool"
```

0 sources -> stop. Report "No new sources this week."

### 2. Collect older vault content

Pool = top-30 por overlap de tags com os recentes (determinístico) + 20 aleatórios (serendipidade cross-domain) + 30 concepts. Sorteio puro gastava token classificando pares sem relação; o pré-filtro por tag é bash e barato.

```bash
# Portable random sample (gshuf > shuf > sort -R — shuf absent on macOS, L05)
rnd() { if command -v gshuf >/dev/null 2>&1; then gshuf; elif command -v shuf >/dev/null 2>&1; then shuf; else sort -R; fi; }

# Tags dos recentes → set de interesse
TAGS_RECENT=$(for f in $(cat /tmp/recent_sources.txt); do grep "^tags:" "$f"; done \
  | grep -oE '[a-z0-9-]+' | sort -u)

# Candidatos antigos, ranqueados por Nº de tags em comum com o set recente (determinístico)
: > /tmp/old_sources_ranked.txt
for f in $(find 03-RESOURCES/sources/ -name "*.md" | grep -vF -f /tmp/recent_sources.txt); do
  t=$(grep "^tags:" "$f" | grep -oE '[a-z0-9-]+' | sort -u)
  overlap=$(comm -12 <(echo "$TAGS_RECENT") <(echo "$t") | wc -l | tr -d ' ')
  [ "$overlap" -gt 0 ] && echo "$overlap $f"
done | sort -rn | head -30 | awk '{print $2}' > /tmp/old_sources_ranked.txt

# Top-30 por overlap + 20 aleatórios + 30 concepts
cat /tmp/old_sources_ranked.txt > /tmp/old_sources.txt
find 03-RESOURCES/sources/ -name "*.md" | grep -vF -f /tmp/recent_sources.txt \
  | grep -vF -f /tmp/old_sources_ranked.txt | rnd | head -20 >> /tmp/old_sources.txt
find 03-RESOURCES/concepts/ -name "*.md" | rnd | head -30 >> /tmp/old_sources.txt
```

0 overlap em todos os candidatos (tags recentes sem histórico) → o pool cai 100%
para o aleatório (fail-open, não fail-empty).

### 3. Extract themes from each recent source

Ler frontmatter (tags) + primeiras 20 linhas. Extrair: tese central (1 frase), domínio (agent-systems, pkm, ml-research, etc.), entidades-chave.

### 4. Match against older vault

For each recent source, find 2-3 older items with:
- Overlapping tags but **different** domain
- Complementary or contradictory thesis
- Same entity referenced in different context
- Same numerical claim with different magnitude

**Theme clustering shortcut:** com >50 fontes recentes, conte as tags e foque no top 3-5 clusters. Cluster com 3+ fontes convergindo no mesmo insight = Pattern 3+ candidate.

```bash
grep -h "^tags:" $(cat /tmp/recent_sources.txt) 2>/dev/null | \
  sed 's/tags: *\[//;s/\]//' | tr ',' '\n' | \
  sed 's/^ *//;s/ *$//' | sort | uniq -c | sort -rn | head -20
```

**Tese extraction for top clusters:** para cada cluster, leia `## Tese central` de 10-15 fontes:

```bash
grep -l "TAG_NAME" $(cat /tmp/recent_sources.txt) | while read f; do
  echo "=== $(basename $f) ==="
  grep -A2 "^## Tese" "$f" | head -3
done
```

### 5. Classify connections

| Type | Criteria | Value |
|------|----------|-------|
| **Cross-domain** | Different areas, shared insight | HIGH |
| **Contradiction** | Same claim, opposite conclusions | HIGH |
| **Pattern 3+** | 3+ sources converge on same point | HIGH |
| **Q&A** | Older source asks question, recent answers | MEDIUM |
| **Evolution** | Same idea, updated version | MEDIUM |

Only **non-obvious** connections qualify. Same tags + similar thesis = obvious = skip.

### 6. Generate output

Output: `06-GENERATED/reports/connections/YYYY-MM-DD-connections.md`

```markdown
# Non-Obvious Connections of the Week

## Cross-domain
source-A <-> source-B
**Connection:** reason (2-3 sentences max)
**Action:** wikilink to create / concept to consolidate

## Contradictions
...

## Patterns 3+
...

## Suggestions
- Create concept-X — N sources converge
- Consolidate source-A + source-B
- Investigate contradiction X vs Y
```

### 7. Link Repair

Conexões novas são valiosas; links quebrados são dívida. Repare antes de sugerir conexões. Script: `scripts/repair_links.py` (scan, basename match, criação de stubs, verificação). Rodar após batches de ingest.

```bash
python3 scripts/repair_links.py
# Output: /tmp/link_repair_summary.md com links reparados, stubs criados, % resolução
```

Para batches pequenos ou verificação inline, usar o snippet bash abaixo:

```bash
# Scan all source pages for broken concept/entity links
BROKEN_LINKS="/tmp/broken_links.txt"
> "$BROKEN_LINKS"
for f in $(cat /tmp/recent_sources.txt); do
  links=$(grep -oE '\[\[03-RESOURCES/(concepts|entities)/[^\]]+\]\]' "$f" 2>/dev/null)
  for link in $links; do
    path=$(echo "$link" | sed 's/\[\[//;s/\]\]//')
    [[ -f "$VAULT/$path.md" || -f "$VAULT/$path" ]] || echo "$f|$link" >> "$BROKEN_LINKS"
  done
done

BROKEN_COUNT=$(wc -l < "$BROKEN_LINKS" | tr -d ' ')
if [[ $BROKEN_COUNT -gt 0 ]]; then
  echo "## Broken Links Repaired"
  echo "| Source | Broken Link | Action |"
  echo "|--------|-------------|--------|"
  while IFS='|' read -r src link; do
    basename=$(echo "$link" | sed 's/.*\///;s/\]\]//')
    match=$(find "$VAULT/03-RESOURCES/concepts/" "$VAULT/03-RESOURCES/entities/" \
      -name "${basename}.md" -print -quit 2>/dev/null)
    if [[ -n "$match" ]]; then
      correct_path="${match#$VAULT/}"
      correct_path="${correct_path%.md}"
      sed -i '' "s|$link|${correct_path}|g" "$src"
      echo "| $(basename $src) | $link → ${correct_path} | redirected |"
    else
      echo "| $(basename $src) | $link | create stub |"
    fi
  done < "$BROKEN_LINKS"
fi
```

### 8. Update hot cache

Append to `04-SYSTEM/system/state/context/hot.md`:
```
## Connections YYYY-MM-DD | N connections found
**Top:** [most valuable connection in 1 line]
-> `YYYY-MM-DD-connections`
```

### 9. Apply wikilinks

**High confidence** (pattern 3+ or Q&A):
- Add bidirectional wikilink in `## Relations` of involved sources
- Confirm link resolves before adding

**Medium confidence**: only suggest in report. Do NOT edit sources.

---

## Constraints

- Max 10 connections per report (quality > quantity)
- If <3 real connections found, report <3. Never invent forced connections
- Do NOT modify sources without high confidence
- Cross-domain connections > same-domain (higher value)

---

Ver também: daily-brief

**Critério de sucesso:** wikilinks resolvem, sem conexão duplicada, cada conexão com ação concreta e no máximo 10 por relatório.

## Completion

Before finalizing report:
- [ ] Every `wikilink` resolves to existing file
- [ ] No duplicate connections (check previous report)
- [ ] Each connection has concrete action item
- [ ] Hot cache entry added
- [ ] Max 10 connections por relatório (qualidade sobre quantidade)
- [ ] Wikilinks bidirecionais aplicados apenas em alta confiança

## Failure modes

- **Fabricated connections**: inventar convergência com <2 sources concordando → mínimo 2 sources para convergência
- **Orphan inflation por mtime**: usar mtime em vez de `ingested:` frontmatter → false positives de "recentes"
- **Over-linking**: adicionar wikilinks em média confiança → só alta confiança edita source page, média vai no relatório

---

## Passo de síntese (extend)

Após os steps 1-9, gere uma frase-síntese por cluster de conexões que cruza ≥2 domínios (consumida por report-agent F3.8/T7), com grounding via skill `writing/shape`. Não duplique o scanner: só adicione o exploit de síntese.

## Quando NÃO usar

- **Varredura recente já feita no ciclo** (semanal) — rodar de novo é duplicar; connection-finder é cadência, não on-demand.
- **Fonte sem síntese central (`## Tese`)** — stubs poluem o pool com falsa convergência; não incluir.
- **Exploit de síntese específico** — o scanner varre cross-domain; não duplicar a varredura para um único alvo.
- **Busca dirigida por tema conhecido** — para achar conexão específica, busca dirigida ganha da amostragem aleatória.

Disambiguation: `connection-finder` varre fontes recentes vs vault (síntese ampla); `contradiction-sweep` procura contradições entre claims (não convergências); `daily-brief` resume o que mudou — finder conecta o que mudou ao que já existe.

---

## Changelog

- v2.3 (2026-06-23): +Step 7 Link Repair (`scripts/repair_links.py`). Pitfall: criar stubs no path EXATO do wikilink, não no path "correto" do CATEGORY_MAP.
- v2.2 (2026-06-22): tese extraction para top clusters (grep `## Tese central`).
- v2.1 (2026-06-22): `ingested:` no lugar de `mtime -7`; fallback `gshuf||shuf||sort -R`.
- v2.0 (2026-05-25): formalizado; quality gate, trigger pós-ingest, regra de wikilink por confiança.
- v1.0 (2026-05-09): criado (CyrilXBT + DamiDefi).
