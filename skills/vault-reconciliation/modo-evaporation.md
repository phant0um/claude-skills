---
kind: reference
parent: 04-SYSTEM/automation/skills/pipeline/vault-reconciliation/SKILL.md
name: modo-evaporation
type: skill
version: 2.0
status: active
updated: 2026-11-10
description: "Modo EVAPORATION de vault-reconciliation: diagnóstico de arquivo que sumiu do disco entre o scan e o processamento, e proposta de entrada retroativa de manifest. Não é skill invocável."
migrated-from: "evaporation-reconcile v1.0 (2026-06-28), fundida em 2026-11-10 (plano W5)"
---
# Modo EVAPORATION — arquivo some entre scan e processamento

File evaporation: o arquivo está em `candidates_new.txt` (scan inicial do pipeline), mas some do disco segundos ou minutos depois. Trate como **sinal**, não como bug: o manifest talvez precise de entrada retroativa.

**Contrato de escrita (DS-14).** Este modo é recommendation-only, como o resto de `vault-reconciliation`. Ele só lê e escreve a proposta em `06-GENERATED/audits/`. **Nunca modifica `.raw/.manifest.json`.** O Nexus materializa as entradas pelo writer determinístico do manifest, sob o gate DS-18. (A skill `evaporation-reconcile` v1.0 escrevia o manifest direto; isso foi retirado na fusão.)

## Quando entrar neste modo

- F1.0 detecta paths de `candidates_new.txt` onde `[ -f "$f" ]` é falso.
- O pipeline reporta "0 files ingested", mas `candidates_new.txt` tem N > 0 entradas.
- Pipeline diário ou semanal reporta discrepância entre candidatos e ingeridos; `cp` falha em path que existia no scan; a triagem aprova mais do que foi processado.

**Fora deste modo:** o arquivo nunca existiu (erro de path); batch vazio por design; erro de permissão; clipping ainda em `00-INBOX` (presença no disco não é evaporation, é triagem); reparo de wikilink quebrado (use `fix-broken-links.py`).

## Passo 1 — Diagnosticar (read-only)

```bash
VAULT_DIR="~/Obsidian/vault-michel"
EXISTING=0; MISSING=0; MISSING_PATHS=""
while IFS= read -r f; do
  if [ -f "$f" ]; then EXISTING=$((EXISTING+1))
  else MISSING=$((MISSING+1)); MISSING_PATHS="$MISSING_PATHS\n$f"; fi
done < /tmp/candidates_new.txt
echo "Existing: $EXISTING  Missing: $MISSING"
[ $MISSING -gt 0 ] && echo -e "Missing paths:$MISSING_PATHS"
```

## Passo 2 — Separar "já arquivado" de "sumiu de vez" (read-only)

```bash
VAULT_DIR="~/Obsidian/vault-michel"
: > /tmp/evaporated_already_archived.txt
: > /tmp/evaporated_truly_gone.txt
while IFS= read -r f; do
  [ -f "$f" ] && continue
  bn=$(basename "$f")
  archived=$(find "$VAULT_DIR/08-ARCHIVE/" -name "$bn" 2>/dev/null | head -1)
  if [ -n "$archived" ]; then echo "$f|$archived" >> /tmp/evaporated_already_archived.txt
  else echo "$f" >> /tmp/evaporated_truly_gone.txt; fi
done < /tmp/candidates_new.txt
echo "Arquivados (entrada retroativa): $(wc -l < /tmp/evaporated_already_archived.txt)"
echo "Sumiram de vez (sync): $(wc -l < /tmp/evaporated_truly_gone.txt)"
```

## Passo 3 — Propor entradas retroativas (só proposta, não escreve o manifest)

Para cada arquivo já arquivado e sem entrada no manifest, o script **só lê** o manifest e escreve a proposta em `06-GENERATED/audits/evaporation-retro-<data>.json`.

```python
#!/usr/bin/env python3
import json, os, re
from datetime import date

VAULT = "~/Obsidian/vault-michel"
MANIFEST = os.path.join(VAULT, ".raw/.manifest.json")      # só leitura
ARCHIVE_MAP = "/tmp/evaporated_already_archived.txt"
today = date.today().isoformat()
OUT = os.path.join(VAULT, "06-GENERATED/audits", f"evaporation-retro-{today}.json")

sources = json.load(open(MANIFEST)).get("sources", {})
proposals = []
for line in open(ARCHIVE_MAP):
    line = line.strip()
    if "|" not in line:
        continue
    original, archived = line.split("|", 1)
    bn = os.path.basename(original)
    stem = os.path.splitext(bn)[0]
    if bn in sources or stem in sources:
        continue                                            # já tem entrada
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]", "-", stem.lower())).strip("-")
    page = None
    for root, _, files in os.walk(os.path.join(VAULT, "03-RESOURCES", "sources")):
        page = next((os.path.join(root, n) for n in files if slug and slug[:40] in n.lower()), None)
        if page:
            break
    proposals.append({
        "key": bn, "alias_key": stem,                      # AMBAS as chaves: com e sem extensão
        "hash": "evaporated-reconcile", "ingested_at": today, "category": "articles",
        "pages_created": [page or archived],
        "source_page_found": bool(page),
        "note": "evaporation: arquivo sumiu entre scan e processamento, já arquivado",
    })
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({"proposals": proposals}, open(OUT, "w"), indent=2, ensure_ascii=False)
print(f"{len(proposals)} propostas em {OUT}")
```

O Nexus lê a proposta e materializa as chaves `key` e `alias_key` pelo writer do manifest. Proposta sem `source_page_found` volta ao humano: sem source page existente o item seria reingerido.

## Passo 4 — Relatório

Contadores no relatório da reconciliação: candidatos, existentes, evaporados, já arquivados (com proposta) e sumidos de vez (sync Readwise/iCloud, não bug do pipeline). Arquivos sumidos de vez voltam no próximo sync; a próxima execução os pega.

## Mitigação

1. Não entre em pânico: evaporation é padrão recorrente (2026-06-16: 51 arquivos; 2026-06-22: similar).
2. Rode os passos 1 e 2 para quantificar existentes, ausentes e arquivados.
3. Rode o passo 3 e entregue a proposta ao Nexus.
4. Re-rode o pipeline só depois da materialização.

## Causas raiz

1. Sync do Readwise limpa ou substitui arquivos durante o ciclo.
2. Pipeline anterior moveu arquivos para `08-ARCHIVE/` sem atualizar o manifest.
3. Sync do Obsidian (iCloud/Dropbox) remove arquivos temporariamente.
4. Seletividade: arquivos Score D evaporam mais (2026-06-28: 51 dos 52 rejeitados eram evaporados).

## Failure modes

- **Misdiagnosis:** tratar como bug e depurar o `find`. Evaporation é sync, não bug.
- **Escrever o manifest daqui:** viola DS-14; só o Nexus materializa.
- **Reconcile incompleto:** propor entrada sem buscar a source page existente causa reingest.
- **Slug curto:** `slug[:30]` em nome longo dá 0 matches; use 40 a 50 caracteres ou o slug completo.
- **Chave única:** propor só a chave com extensão faz o próximo grep sem extensão marcar falso "novo". Proponha as duas.

## Completion

- [ ] Existentes e ausentes contados (passo 1)
- [ ] Arquivados e sumidos de vez separados (passo 2)
- [ ] Proposta gravada em `06-GENERATED/audits/` com as duas chaves por item (passo 3)
- [ ] Nenhuma escrita em `.raw/.manifest.json` por este modo
- [ ] Entregue ao Nexus para materializar sob DS-18
