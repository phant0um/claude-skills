---
status: active
parent: "[pre-ingest-dedup](SKILL.md)"
kind: reference
name: pre-ingest-dedup-reference
type: skill-reference
updated: 2026-07-25
tags: [hook, dedup, pre-ingest, edge-cases, pitfalls, reference]
reviewed-scope: "W3c 2026-10-10: poda de snippets cobertos por vault-reconcile-join.py, indice parse-first (manifest-index.py), integracao triagem-clipping e large batch obsoletos, changelog"
reviewed-by: R13 (claude-sonnet; drift R12 corrigido)
reviewed: 2026-10-04
size-exception: "303 linhas; corte restante removeria licoes sem cobertura de gate (slug prefix, F1.0 hidden files)"
size-exception-review: 2027-01-10
---
## Contents

- [Estratégia de Similaridade (detalhe)](#estratégia-de-similaridade-detalhe)
- [Dedup-Gap Pattern (2026-06-16 achado) — detalhe completo](#dedup-gap-pattern-2026-06-16-achado-detalhe-completo)
- [File Evaporation Pattern (2026-06-16) — detalhe completo](#file-evaporation-pattern-2026-06-16-detalhe-completo)
- [Approved-but-not-ingested Gap (2026-07-06 achado)](#approved-but-not-ingested-gap-2026-07-06-achado)
- [Manifest Key Dual-Registration (2026-06-18 fix)](#manifest-key-dual-registration-2026-06-18-fix)
- [Slug Prefix Length Tuning (2026-06-22 achado)](#slug-prefix-length-tuning-2026-06-22-achado)
- [F1.0 Pre-dedup False Positives — Hidden/System Files (2026-06-23 achado)](#f10-pre-dedup-false-positives-hiddensystem-files-2026-06-23-achado)
- [Shell Variable Persistence Across terminal() Calls (2026-06-23 achado)](#shell-variable-persistence-across-terminal-calls-2026-06-23-achado)



Core: [pre-ingest-dedup](SKILL.md)

# Pre-Ingest Dedup — Reference (edge cases, pitfalls, histórico)

> Progressive disclosure (skill-audit-pocock P0+P4). Carregar só ao debugar
> falso positivo/negativo de dedup, file evaporation, ou ao afinar prefix/slug.
> Consolidado 2026-07-16: funde o antigo `_pre-ingest-dedup-edge-cases.md`
> (extraído 2026-06-28) + narrativas datadas do core.

---

## Estratégia de Similaridade (detalhe)

**Problema real:** `colbymchenrycodegraph Pre-indexed code knowledge graph for Claude Code, Codex, Cursor, and OpenCode` vs. `colbymchenrycodegraph Pre-indexed code knowledge graph for Claude Code, Codex, Cursor, OpenCode, and Hermes Agent`

Os primeiros 40 chars são idênticos: `colbymchenrycodegraph Pre-indexed code k`

**Solução:** prefix-match nos primeiros 40 chars (captura esse caso).

**Limitação:** não detecta duplicatas com títulos completamente diferentes que
cobrem mesmo conteúdo — para isso, precisaria de embedding similarity (custo de
tokens; fora do escopo deste hook).

### Falsos Positivos Esperados

- Séries do mesmo autor: "29 LLM Evaluation Concepts" vs "21 Reinforcement Learning Concepts" — prefixos diferentes, sem FP
- Versões de mesmo repo (v1 vs v2): detecta corretamente, requer atenção manual
- Tradução do mesmo artigo (EN + CN): não detecta (basenames diferentes) — aceitável, traduções têm valor complementar

---

## Dedup-Gap Pattern (2026-06-16 achado) — detalhe completo

**Problema recorrente:** F1.0b manifest check declara arquivo como "novo" quando na
verdade já foi ingerido em sessão anterior. Causa raiz:

1. Arquivo original em `00-INBOX/clippings/` foi processado → source page criada em
   `03-RESOURCES/sources/<category>/` → original movido para `08-ARCHIVE/A/`
2. Mas manifest entry NÃO foi criada (ou usa chave com formato divergente)
3. Próximo pipeline run: `find` pega o arquivo (se ainda em 00-INBOX/clippings/ ou se Readwise
   re-sincronizou), F1.0b checa manifest → não encontrado → marca como "novo"
4. Resultado: re-triagem de arquivo já ingerido, desperdício de tokens

**Frequência:** 2026-06-10 (42 files ghost-ingest), 2026-06-16 (209 curso files +
21 articles — 100% já tinham source pages). Padrão, não exceção.

### Concurso-Specific Dedup

Concurso aulas seguem padrão `curso-NNNNNN-aula-NN-HASH-completo.md`. O curso-ID +
aula-NN é a chave semântica — o HASH varia entre conversões. Para evitar re-ingest:

1. Extrair `curso-{CID}-aula-{NN}` do filename
2. Checar se `materias/<disciplina>/(pe-)aula-{NN}.md` já existe
3. Se existe → registro retroativo no manifest, não copiar

### macOS Filename Quirks

Arquivos com `$`, `&`, `…`, curly quotes (`'"`), parênteses e vírgulas no nome
quebram `cp` mesmo quando o path vem de `find`. Workarounds:

- Usar `find ... -exec cp {} dest/ \;` em vez de `cp "$path" dest/`
- Ou usar `while IFS= read -r f; do cp "$f" dest/; done < <(find ...)`
- NUNCA usar `for f in $(find ...)` — quebra em espaços e chars especiais

### Índice parse-first e slug conservador (2026-08-01)

`manifest-index.py` lê e parseia o manifest uma vez e cria índices exatos,
normalizados e fuzzy. Contrato pinado por `test-manifest-index.py`.

```bash
python3 04-SYSTEM/scripts/manifest-index.py build --manifest .raw/.manifest.json > "$MANIFEST_INDEX_FILE"
python3 04-SYSTEM/scripts/manifest-index.py filter --index "$MANIFEST_INDEX_FILE" --candidates "$CANDIDATES_ALL_FILE" > "$CANDIDATES_NEW_FILE"
```

---

## File Evaporation Pattern (2026-06-16) — detalhe completo

**Problema recorrente:** `find` escaneia 00-INBOX/clippings/ no início do pipeline e
gera `candidates_all.txt`. Mas entre o scan e o processamento (segundos a
minutos depois), arquivos somem do disco. Causas:

1. **Readwise sync** limpa/substitui arquivos durante o cycle
2. **Pipeline anterior** moveu arquivos para 08-ARCHIVE/ mas não atualizou manifest
3. **Obsidian sync** (iCloud/Dropbox) remove arquivos temporariamente

**Sintoma:** `[ -f "$f" ]` retorna false para caminhos em candidates_new.txt.
`cp` falha silenciosamente. Pipeline reporta "0 files ingested" mesmo com
N candidatos aprovados.

**Diagnóstico rápido:**

```bash
EXISTING=0; MISSING=0
while IFS= read -r f; do
  [ -f "$f" ] && EXISTING=$((EXISTING+1)) || MISSING=$((MISSING+1))
done < /tmp/candidates_concurso.txt
echo "Existing: $EXISTING, Missing: $MISSING"
```

Se MISSING > 0, arquivos evaporaram. Verificar 08-ARCHIVE/ para confirmar
que já foram processados:

```bash
# Para cada arquivo "missing", checar se está no archive
while IFS= read -r f; do
  [ -f "$f" ] && continue
  bn=$(basename "$f")
  find 08-ARCHIVE/ -name "$bn" 2>/dev/null | head -1
done < "$CANDIDATES_NEW_FILE"
```

**Mitigação:** Não tratar file evaporation como erro — tratar como sinal de
que processamento retroativo é necessário (manifest entry + source page check).
O pipeline-diario deve ter um passo de "retroactive manifest reconciliation"
após detectar file evaporation.

---

## Approved-but-not-ingested Gap (2026-07-06 achado)

**Problema:** Arquivos movidos para `08-ARCHIVE/approved/` (triagem aprovada)
mas nunca ingeridos para `03-RESOURCES/sources/`. O usuário assume que
"approved" = "ingested" mas o pipeline tem duas etapas distintas: triagem
(aprova) → ingest (cria source page). Files podem estagnar entre as duas.

**Sintoma:** Usuário pergunta sobre conteúdo de 7 artigos em
`08-ARCHIVE/approved/2026-07-06/`. Ao verificar `03-RESOURCES/sources/`,
apenas 3 de 7 têm source pages. Os outros 4 foram aprovados na triagem
mas o ingest nunca ocorreu (ou ocorreu parcialmente — ex: só moved to archive
sem criar source page).

**Diagnóstico e reconciliation pass:** `04-SYSTEM/scripts/vault-reconcile-join.py` (join raws `08-ARCHIVE/approved/` x source pages, com cobertura).

**Fix:** O pipeline precisa de um gate pós-approval que verifica se o ingest
realmente ocorreu. Não basta mover para `08-ARCHIVE/approved/` — é preciso
confirmar que a source page foi criada em `03-RESOURCES/sources/`.

**Lição:** `08-ARCHIVE/approved/` é um estado intermediário, não final.
Files approved podem estagnar se o ingest-agent não processá-los. O
reconciliation pass deve rodar após cada pipeline-semanal para detectar
gaps antes que o usuário os encontre.

---

## Manifest Key Dual-Registration (2026-06-18 fix)

**Problema:** F1.0b grep testa múltiplos formatos de key (`"basename.md"`,
`/basename"`, `"stem"`, `slug_stem`) mas o manifest-write registrava só
uma key (basename com extensão). Se o grep procurava sem extensão, não batia.
Triagem 2026-06-17: 19/19 falsos positivos por mismatch.

**Fix:** registrar AMBAS as variantes de key (com e sem extensão) no
manifest-write:

```bash
bn=$(basename "$f")          # "The Log Is the Agent.md"
bn_noext="${bn%.*}"           # "The Log Is the Agent"
jq --arg k "$bn" --arg k2 "$bn_noext" --arg h "$_hash" --arg d "$(date -I)" \
   --arg c "$category" --arg p "$_page" \
   '.sources[$k] = {hash: $h, ingested_at: $d, category: $c, pages_created: [$p]}
  | .sources[$k2] = {hash: $h, ingested_at: $d, category: $c, pages_created: [$p], alias_of: $k}' \
   .raw/.manifest.json > /tmp/manifest.tmp && mv /tmp/manifest.tmp .raw/.manifest.json
```

O `alias_of` field marca a secondary key como espelho, não duplicata real.
Isso alinha com F1.0b que testa ambos formatos via grep -F.

**Quando aplicar:** todo manifest-write pós-ingest (ingest-agent F2.6).
**Quando NÃO aplicar:** retroactive entries onde só uma variante é conhecida.

---

## Slug Prefix Length Tuning (2026-06-22 achado)

O second-pass check usa `slug[:30]` como prefix de busca. Para filenames longos
(títulos de blog posts com 60+ chars), 30 chars não é suficiente para match
único — retorna 0 encontrados mesmo quando source page existe.

**Sintoma:** `TRULY_NEW=0, RETRO=0` para todos os 157 candidatos, mas source
pages claramente existem no vault (1243+ pages). Second-pass não reduziu
falsos positivos.

**Exemplo real:** filename `Claude Code Skills The Hidden System Prompt Layer That Turns Claude Into a Senior Engineer.md`
→ slug = `claude-code-skills-the-hidden-system-prompt-layer...` (70+ chars)
→ source page: `claude-code-skills-the-hidden-system-prompt-layer-that-turns-claude-into-a-senior-engineer.md`
→ prefix 30 = `claude-code-skills-the-hidden-sy` — matcha, mas só por sorte.

Para `Sparser, Faster, Lighter Transformer Language Models`:
→ slug = `sparser-faster-lighter-transformer-language-models`
→ prefix 30 = `sparser-faster-lighter-transfor` — não matcha o full slug.

**Fix:** usar prefix 40-50 chars ou, melhor, buscar pelo slug completo com fallback:

```bash
# ANTES (30 chars — muito curto):
found=$(find 03-RESOURCES/sources/ -iname "*${slug:0:30}*" -type f 2>/dev/null | head -1)

# DEPOIS (50 chars — cobre maioria dos filenames):
found=$(find 03-RESOURCES/sources/ -iname "*${slug:0:50}*" -type f 2>/dev/null | head -1)

# MELHOR (slug completo + fallback first-30):
found=$(find 03-RESOURCES/sources/ -iname "*${slug}*" -type f 2>/dev/null | head -1)
[ -z "$found" ] && found=$(find 03-RESOURCES/sources/ -iname "*${slug:0:30}*" -type f 2>/dev/null | head -1)
```

**Escalação (batches >50, prefix ainda insuficiente):** fuzzy match (Levenshtein/SequenceMatcher):

```python
from difflib import SequenceMatcher
def slug_match(s1, s2, threshold=0.6):
    return SequenceMatcher(None, s1, s2).ratio() > threshold

for page_stem in all_page_stems:
    if slug_match(candidate_slug, page_stem, 0.6):
        ...  # Found existing source page — retroactive manifest entry
```

**Trade-off:** prefix mais longo = menos falsos negativos, mais falsos positivos
(raro mas possível em vault com 1200+ source pages — 50 chars é o sweet spot).
Para batches pequenos (<20), 30 chars é adequado.

**Quando NÃO otimizar:** se file evaporation já removeu os C/D files (como
observado em 2026-06-22), o second-pass é menos crítico — evaporation age
como dedup natural.

---

## F1.0 Pre-dedup False Positives — Hidden/System Files (2026-06-23 achado)

**Problema:** O F1.0 stem-dedup (`find ... | sed 's/\.[^.]*$//' | sort | uniq -d`)
detecta falso positivo em arquivos de sistema como `.manifest.json.bak` — o stem
`.manifest.json` existe tanto em `.raw/` quanto em `00-INBOX/clippings/`, mas são arquivos
de infraestrutura (backup, metadata), não duplicatas de conteúdo.

**Sintoma:** `uniq -d` reporta `.raw/.manifest.json.bak` como duplicata, mas não
há par real — é o backup do manifest aparecendo ao lado do original.

**Fix:** Filtrar hidden files e arquivos de metadata antes do stem comparison:

```bash
# ANTES (gera falsos positivos):
find .raw/ 00-INBOX/clippings/ -type f | sed 's/\.[^.]*$//' | sort | uniq -d

# DEPOIS (exclui hidden files e metadata):
find .raw/ 00-INBOX/clippings/ -type f \
  ! -name ".*" ! -name "*.json" ! -name "*.jsonl" ! -name "*.txt" \
  | sed 's/\.[^.]*$//' | sort | uniq -d
```

**Quando aplicar:** sempre que F1.0 rodar em diretórios que contêm arquivos de
metadata/manifest/backup alongside conteúdo real.

**Updated 2026-06-28:** Em batch de 810 candidatos (pipeline-semanal 2026-06-28), F1.0
rodou limpo — 0 duplicatas encontradas. O filtro acima resolveu os falsos positivos
de system files. Padrão confirmado como estável.

---

## Shell Variable Persistence Across terminal() Calls (2026-06-23 achado)

**Problema:** Quando a rotina daily-scan é executada via `terminal()` tool do scheduler legado,
variáveis de shell (`NEW_COUNT`, etc.) **não persistem** entre chamadas separadas
de `terminal()`. Cada call inicia um shell fresh. O F1.0c e o Volume threshold flag
rodam em calls separadas — `NEW_COUNT` chega vazia no threshold check.

**Sintoma:** `daily-scan:  candidatos (abaixo de threshold 30)` — string vazia
onde deveria estar o número. O `-ge` comparison falha ou avalia incorretamente.

**Fix:** Recalcular `NEW_COUNT` do arquivo de output no início de cada call que
precisa do valor:

```bash
# No início do threshold check call:
NEW_COUNT=$(wc -l < "$CANDIDATES_NEW_FILE" | tr -d ' ')
THRESHOLD=30
# ...então usar $NEW_COUNT normalmente
```

Alternativamente, executar F1.0b + F1.0c + threshold em uma única `terminal()`
call (um bloco bash contínuo), garantindo que todas as variáveis estejam no
mesmo escopo de shell.

**Quando aplicar:** qualquer rotina vault que use `terminal()` em múltiplas
chamadas e dependa de variáveis calculadas em calls anteriores. Verificar
sempre com `echo "NEW_COUNT=$NEW_COUNT"` antes do uso.

Histórico de versões: `git log` deste arquivo.
