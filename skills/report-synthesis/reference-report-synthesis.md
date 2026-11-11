---
status: active
parent: "[report-synthesis](SKILL.md)"
kind: reference
name: reference-report-synthesis
type: skill-reference
reviewed-scope: "checagem mecanica 2026-09-20: 3/3 paths citados existem; 1/1 script citado resolve; 0 wikilink real (os 11 casados pelo regex sao sintaxe bash `[[ ]]` e interpolacao); 6 secoes, 247 linhas; corpo é fatia verbatim de report-synthesis.md movida em f735c0631, conteudo nao reavaliado"
reviewed-by: claude-opus-5
reviewed: 2026-09-20
updated: 2026-09-17
---

## Contents

- F3.4 Contradiction Register
- F3.4b Vault Impact → Kanban
- F3.7 Connection Density Metrics
- Histórico de versões
- Equivalência com report-agent

## F3.4 Contradiction Register `[bash + Sonnet]`

**Princípio**: contradições flagadas em F3.1 são efêmeras — dissolvem-se
no próximo run sem resolução. Register cumulativo acumula tensões até que
sejam resolvidas ou confirmadas como paradoxo.

### Fluxo

1. Extrair contradições de F3.1 (lista do relatório do dia)
2. Para cada contradição:
   - Append em `03-RESOURCES/concepts/_contradiction-register.md`
   - Formato: `| Data | Tópico | Fonte A → tese | Fonte B → tese | Status |`
   - Status: `aberta` (default), `resolvida`, `paradoxo`
3. Verificar contradições `aberta` > 14 dias → flag "stale" no relatório

### Bash — Append ao register

```bash
REGISTER="03-RESOURCES/concepts/_contradiction-register.md"
TODAY=$(date -I)

# Para cada contradição detectada em F3.1 (passada como arg)
while IFS='|' read -r topic src_a thesis_a src_b thesis_b; do
  echo "| ${TODAY} | ${topic} | ${src_a} → ${thesis_a} | ${src_b} → ${thesis_b} | aberta |" >> "$REGISTER"
done < /tmp/contradictions_today.txt
```

### Bash — Stale check

```bash
# Flag contradições ABERTAS há > 14 dias. BUG-FIX 2026-07-11: antes ignorava o
# campo Status → re-flagava entradas já marcadas paradoxo/resolvida (que ficavam
# na tabela ativa por causa da regra append-only). Agora só conta status=aberta.
TODAY_EPOCH=$(date -d "$TODAY" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$TODAY" +%s)
while IFS='|' read -r _ date_str topic src_a src_b st _; do
  date_str="$(echo "$date_str" | xargs)"; st="$(echo "$st" | xargs)"
  [[ "$date_str" == Data* || "$date_str" == ---* ]] && continue
  [[ "$st" != "aberta" ]] && continue   # paradoxo/resolvida não são stale (não usar $status: read-only no zsh)
  d_epoch=$(date -d "$date_str" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$date_str" +%s) || continue
  days_open=$(( (TODAY_EPOCH - d_epoch) / 86400 ))
  # BUG-FIX 2026-07-11: emitir a LINHA COMPLETA do register (não só topic), senão
  # o report reconstrói fonte A/B de memória e inventa teses (sloppiness: run 07-11
  # gerou "Sonnet 4.6/Fable 5" no lugar do real "GLM-5.2/Grok").
  [[ $days_open -gt 14 ]] && echo "⚠️ STALE ${days_open}d | ${date_str} |${topic}|${src_a}|${src_b}| status=${st}"
done < "$REGISTER"
```

> **Regra anti-sloppiness (F3.4 no ingest-diario)**: a tabela de contradições no
> relatório deve ser **cópia verbatim** da linha do register (via stale check acima),
> NUNCA reconstruída/parafraseada de memória. Se a fonte/tese não está no register,
> não inventar — ler o register é a única fonte de verdade.

### Regra

- **Append-only na tabela ativa até resolver** — ao marcar `resolvida`/`paradoxo`, MOVER a entrada para a seção Resolvidas/Paradoxos (não deixar na tabela "Contradições" ativa, senão o stale check a re-flaga)
- **1 linha por contradição** — síntese, não debate longo
- **Stale > 14 dias** → flag para revisão manual (Nexus decide se resolvida/paradoxo)
- **Resolvida** → atualizar status + adicionar link para source que resolveu

## F3.4b Vault Impact → Kanban `[bash]`

**Princípio**: F3.3 gera tabela de melhorias mas nada age sobre elas. Itens
"alta prioridade" ficam pendentes para sempre. Kanban tracking resolve isto.

### Fluxo

1. Após gerar F3.3 Vault Impact, filtrar itens `alta` prioridade
2. Inserir na seção `## Inbox` de `07-QUEUE/kanban/vault-impact-kanban.md` via `04-SYSTEM/scripts/kanban-inbox-append.py`
3. Em runs subsequentes, verificar itens `[ ]` → se skill/agent já foi criado,
   marcar `[x]` **com o rastro** (commit, path, saída de gate). "Feito" sem
   rastro reabre o ticket (`weekly-ops` PARTE C)

### Bash — Append ao kanban

O destino é a seção `## Inbox` — **nunca** `>>` no fim do arquivo. Append cego
caía dentro da última seção (histórico "concluído"), colava `||` na tabela
anterior e sumia da leitura por coluna. O script ancora na seção, deduplica e
reprova se `## Inbox` não existir:

```bash
# Para cada item "alta" da tabela F3.3
while IFS='|' read -r tipo nome esforco fonte; do
  python3 04-SYSTEM/scripts/kanban-inbox-append.py \
    --tipo "$tipo" --nome "$nome" --esforco "$esforco" --fonte "${fonte}"
done < /tmp/vault_impact_high.txt
```

Status escrito é `[ ]` (aberto). O agente **não** promove para `Ready`/`Doing` —
promoção é puxada humana (`weekly-ops` PARTE E).

### Regra

- **Dedup obrigatório** — não re-adicionar item já no kanban
- **Stale > 30 dias pendente** → flag para Nexus decidir (criar ou descartar)
- **Append-only** — nunca remover, só mudar status

## F3.7 Connection Density Metrics `[bash]`

**Princípio**: sem métricas, drift de conectividade é invisível. Orphan
sources, concepts sem backlinks, e coverage gaps crescem silenciosamente.

### Fluxo

Após F3.5, rodar métricas via bash (zero AI cost) e append ao relatório.

### Bash — Métricas

```bash
shopt -s globstar 2>/dev/null   # OBRIGATÓRIO: sem isto, **/*.md degrada p/ 1 nível
                                 # (SRC_TOTAL viria 584 em vez de 3226). bash≥4.
# 1. Orphan sources: source pages sem nenhum wikilink apontando para elas
SRC_DIR="03-RESOURCES/sources"
ORPHAN_COUNT=0
SRC_TOTAL=0
for f in "$SRC_DIR"/**/*.md; do
  [[ -f "$f" ]] || continue
  SRC_TOTAL=$((SRC_TOTAL + 1))
  slug=$(basename "$f" .md)
  # Procura por wikilinks para este slug em todo o vault (exceto o próprio arquivo)
  if ! grep -rl "\[\[.*${slug}\]\]" ~/Obsidian/vault-michel --include="*.md" 2>/dev/null | \
    grep -v "$f" | grep -q .; then
    ORPHAN_COUNT=$((ORPHAN_COUNT + 1))
  fi
done
ORPHAN_RATE=$(echo "scale=1; $ORPHAN_COUNT * 100 / $SRC_TOTAL" | bc 2>/dev/null || echo "?")

# 2. Average backlinks per source.
# BUG-FIX 2026-07-11: fórmula antiga contava ARQUIVOS com o prefixo full-path
# "" → dava ~0 (vault usa slug bare "[[slug", só ~22
# arquivos usam full-path). Corrigido: contar OCORRÊNCIAS inbound de wikilinks
# cujo último segmento = slug de source. (Auditoria 07-11: fórmula antiga=0.0,
# real=5.5. O run acertou 5.6 divergindo deste doc — doc estava errado.)
BL_TOTAL=$(python3 - "$SRC_DIR" <<'PYBL'
import os,re,sys,glob
srcs=glob.glob(os.path.join(sys.argv[1],'**','*.md'),recursive=True)
slugs={os.path.basename(f)[:-3] for f in srcs}
wl=re.compile(r'\[\[([^\]|#]+)'); n=0
for dp,_,fs in os.walk('.'):
    if '/.git' in dp: continue
    for fn in fs:
        if not fn.endswith('.md'): continue
        try: t=open(os.path.join(dp,fn),encoding='utf-8',errors='ignore').read()
        except: continue
        n+=sum(1 for m in wl.findall(t) if m.strip().split('/')[-1] in slugs)
print(n)
PYBL
)
AVG_BL=$(echo "scale=1; $BL_TOTAL / $SRC_TOTAL" | bc 2>/dev/null || echo "?")

# 3. Concept coverage: concepts com pelo menos 1 source linkando
CONCEPT_WITH_SRC=0
CONCEPT_TOTAL=0
for c in ~/Obsidian/vault-michel/03-RESOURCES/concepts/**/*.md; do
  [[ -f "$c" ]] || continue
  CONCEPT_TOTAL=$((CONCEPT_TOTAL + 1))
  cslug=$(basename "$c" .md)
  grep -rl "\[\[.*${cslug}\]\]" ~/Obsidian/vault-michel/03-RESOURCES/sources/ --include="*.md" 2>/dev/null | grep -q . && \
    CONCEPT_WITH_SRC=$((CONCEPT_WITH_SRC + 1))
done
COVERAGE=$(echo "scale=1; $CONCEPT_WITH_SRC * 100 / $CONCEPT_TOTAL" | bc 2>/dev/null || echo "?")

# 4. Manifest health
MANIFEST_ENTRIES=$(jq '.sources | length' .raw/.manifest.json 2>/dev/null || echo "?")

echo "## Connection Density"
echo "| Metric | Value |"
echo "|--------|-------|"
echo "| Source pages total | $SRC_TOTAL |"
echo "| Orphan sources (0 backlinks) | $ORPHAN_COUNT ($ORPHAN_RATE%) |"
echo "| Avg backlinks/source | $AVG_BL |"
echo "| Concepts with source evidence | $CONCEPT_WITH_SRC/$CONCEPT_TOTAL ($COVERAGE%) |"
echo "| Manifest entries | $MANIFEST_ENTRIES |"
```

### Interpretação

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Orphan rate | <15% | 15-30% | >30% |
| Avg backlinks/source | >2.0 | 1.0-2.0 | <1.0 |
| Concept coverage | >60% | 30-60% | <30% |

### Regra

- **Zero AI cost** — bash only, roda em <30s
- **Append ao relatório** — não é arquivo separado
- **Trend tracking** — comparar com run anterior (se disponível em ingest-diario-*.md)
- **Orphan rate >30%** → flag para Nexus: vault precisando de connection-finder skill

## Histórico de versões
**v1.6.0 (2026-06-29):** +F3.9 Hot por Domínio — implementa bash real do append
por domínio (regra existia em prosa desde versões anteriores, mas sem bash —
os 6 `hot-<dominio>.md` ficavam vazios há 2 dias, nunca populados). hot.md
raiz passa a receber só linha de índice quando há shard dedicado pro domínio.

**v1.4.0 (2026-06-18):** +F3.6 Meta-padrões semanais (absorvido de
weekly-synthesis — pipeline agora é semanal, F3.6 é nativo). Referências
atualizadas de "diário" para "semanal". Pipeline-diario → pipeline-semanal.

**v1.3.0 (2026-06-18):** +F3.4 Contradiction Register (contradições acumulam
cumulativamente em `_contradiction-register.md` ao invés de dissolverem a
cada run). +F3.4b Vault Impact → Kanban (itens "alta" do F3.3 viram tickets
tracked em `07-QUEUE/kanban/vault-impact-kanban.md` com auto-resolve).
+F3.7 Connection Density Metrics (orphan rate, avg backlinks, concept
coverage — bash only, zero AI cost). Fixes modelo obsoleto (nemotron/deepseek
→ Sonnet).

**Status:** active desde 2026-06-09
**Pipeline integration:** substitui F3.0–F3.5 + commit gate do `pipeline-semanal.md`
**Próximo na cadeia:** skill `audit-logging` para commit + session log

## Equivalência com report-agent

Este skill executa o mesmo método do report-agent:
- Mesmo input schema (schema-report-packet-v2.json)
- Mesmo output schema (schema-report-result-v2.json)
- Mesma chamada a `pipeline-receipts.py render`
- Mesmas limitações (max 3 itens, sem contagens, sem voz autoral)
- Diferença: não é despachado como agente; é executado pelo chamador
