---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-01-macos-compat
type: skill-reference
updated: 2026-08-17
reviewed-scope: "checagem mecanica + semantica: 3/3 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 6 secoes, 167 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [macOS Compatibility Pitfalls (2026-06-16)](#macos-compatibility-pitfalls-2026-06-16)
- [Nexus Manual Override](#nexus-manual-override)
- [File Evaporation Pattern (2026-06-16)](#file-evaporation-pattern-2026-06-16)
- [Integracao com triagem-clipping.md](#integracao-com-triagem-clippingmd)
- [Guardrails](#guardrails)


> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: macOS Compatibility, Nexus Manual Override, File Evaporation, triagem-clipping, Guardrails.

## macOS Compatibility Pitfalls (2026-06-16)

### `grep -P` (Perl regex) nao existe no macOS

macOS usa BSD grep, nao GNU grep. `-P` (Perl-compatible regex) gera erro:

```
grep: invalid option -- P
usage: grep [-abcdDEFGHhIjJlLmMnOoPpRSsUVvwXxZz] ...
```

**Fix:** Substituir todas as extracoes `grep -oP` por `sed` ou `grep -o` com BRE/ERE:

```bash
# ANTES (Linux-only, quebra no macOS):
echo "$f" | grep -oP 'curso-\d+' | sort -u

# DEPOIS (macOS-compatible):
echo "$f" | sed -n 's/.*\(curso-[0-9]*\).*/\1/p' | sort -u
# ou
echo "$f" | grep -oE 'curso-[0-9]+' | sort -u
```

### Extracao de aula number

```bash
# ANTES (Linux):
aula_num=$(echo "$bn" | grep -oP 'aula-\K[0-9]+')

# DEPOIS (macOS):
aula_num=$(echo "$bn" | sed -n 's/.*aula-\([0-9]*\).*/\1/p')
```

### Extracao de curso-ID

```bash
# ANTES (Linux):
curso_id=$(echo "$bn" | grep -oP 'curso-\K[0-9]+')

# DEPOIS (macOS):
curso_id=$(echo "$bn" | sed -n 's/.*curso-\([0-9]*\).*/\1/p')
# ou
curso_id=$(echo "$bn" | grep -oE 'curso-[0-9]+' | head -1 | sed 's/curso-//')
```

---

## Nexus Manual Override

Heuristica bash captura ~60-80% dos casos. O resto precisa de julgamento Nexus
(manual). Quando aplicar:

1. **AI agent articles scored C:** Se o artigo cobre um core obsession do vault
   (agent systems, Claude, skills, loops, Obsidian/PKM), bump para A/B mesmo se
   a heuristica pontuou baixo. A heuristica nao conta multiplas matches do mesmo
   dominio - um artigo sobre "loop engineering" pode ter score 4 porque so
   matchou "loop" uma vez, mas e core A.

2. **Concurso aulas:** Seguem padrao estabelecido. 736+ entries similares no
   manifest. Todas A por default - material de estudo RFB e core obsession.

3. **Borderline (score 4-6):** 1 batch AI call (Haiku), nunca loop per-file.
   Abaixo do cache floor 4096 tokens.

---

## File Evaporation Pattern (2026-06-16)

**Problema recorrente:** `find` escaneia 00-INBOX/clippings/ no inicio do pipeline e
gera candidates_all.txt. Mas entre o scan e o processamento (segundos a
minutos depois), arquivos somem do disco. Causas:

1. Readwise sync limpa/substitui arquivos durante o cycle
2. Pipeline anterior moveu arquivos para 08-ARCHIVE/ mas não atualizou manifest
3. Obsidian sync (iCloud/Dropbox) remove arquivos temporariamente

**Sintoma:** `[ -f "$f" ]` retorna false para caminhos em candidates_new.txt.
`cp` falha silenciosamente. Pipeline reporta "0 files ingested" mesmo com
N candidatos aprovados.

**Diagnóstico rápido:**

```bash
EXISTING=0; MISSING=0
while IFS= read -r f; do
  [ -f "$f" ] && EXISTING=$((EXISTING+1)) || MISSING=$((MISSING+1))
done < /tmp/candidates_new.txt
echo "Existing: $EXISTING, Missing: $MISSING"
```

Se MISSING > 0, arquivos evaporaram. Verificar 08-ARCHIVE/ para confirmar
que ja foram processados:

```bash
while IFS= read -r f; do
  [ -f "$f" ] && continue
  bn=$(basename "$f")
  found=$(find 08-ARCHIVE/ -name "$bn" 2>/dev/null | head -1)
  [ -n "$found" ] && echo "ALREADY ARCHIVED: $bn -> $found"
done < /tmp/candidates_new.txt
```

**Mitigação:** Nao tratar file evaporation como erro — tratar como sinal de
que processamento retroativo e necessario (manifest entry + source page check).
O pipeline-diario deve ter um passo de "retroactive manifest reconciliation"
apos detectar file evaporation. Ver [pre-ingest-dedup](../../pre-ingest-dedup/SKILL.md)
para o formato de retroactive manifest entry.

---

## Integracao com triagem-clipping.md

> [obsoleto 2026-08-16] `score_heuristic.sh` nao existe no vault nem no bundle
> `~/.hermes/skills/vault-michel/`, e `triagem-clipping.md` tambem nao existe.
> O loop abaixo esta preservado como registro do padrao; o scoring vivo e
> `~/.hermes/skills/vault-michel/triagem-scoring/scripts/batch_score.py`.

Substituir o Step 1 (Leitura e scoring por AI) pelo loop:

```bash
for f in $(cat /tmp/candidates_new.txt); do
  title=$(basename "$f" .md)
  snippet=$(head -c 4000 "$f" | sed -E '...' | head -c 2000)
  score=$(bash score_heuristic.sh "$title" "$snippet")
  echo "$f $score" >> /tmp/triagem_scores.txt
done

# Grupo borderline (score 4-6): enviar para AI call em batch
# Grupo seguro aprovado (score 7-10): aprovar direto
# Grupo seguro rejeitado (score 0-3): rejeitar direto
```

**Economia estimada:** ~60% dos arquivos resolvidos sem AI call (score <3 ou >7 sao casos claros).

---

## Guardrails

- Heuristicas GitHub README (padrao `username-repoTitle`) sao ~90% precisas - margem 10% de FP
- Score 4 e borderline - nunca rejeitar automaticamente; sempre passar por AI call
- Score 3 ou menos -> rejeitar direto (FN aceitavel: arquivos de score 3 raramente tem ingest util)
- Erros de parse (arquivo sem texto) -> score conservador = 5 (aprovado por default)

---

