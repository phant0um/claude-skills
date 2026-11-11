---
status: active
parent: "[ingest-verify](../SKILL.md)"
kind: reference
name: ingest-verify-05-pitfalls-archive
type: skill-reference
updated: 2026-07-16
reviewed-scope: "W3c 2026-10-10: poda C8-diretorio (coberto por check-links.py) e changelog (git log); report-path mantido ate decidir relatorios vs ingest-report"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Pitfall: Report output path — use canonical 06-GENERATED/relatorios/ not ingest-report/ — 2026-07-12](#pitfall-report-output-path-use-canonical-06-generatedrelatorios-not-ingest-report-2026-07-12)
- [Implementações dos checks C6–C11](#implementações-dos-checks-c6c11)
- [Post-pipeline proactive patching (preferência do usuário)](#post-pipeline-proactive-patching-preferência-do-usuário)


> Seção fatiada de [ingest-verify](../SKILL.md). Carregar sob demanda: pitfalls de arquivamento e report paths (archive, relatorios, F2.9).

## Pitfall: Report output path — use canonical 06-GENERATED/relatorios/ not ingest-report/ — 2026-07-12

**Sintoma**: FASE 3 relatório salvo em `06-GENERATED/ingest-report/2026-07-12-relatorio-semanal-reexec.md`.
O path canônico é `06-GENERATED/relatorios/` (confirmado via `ls` em runs anteriores).
`ingest-report` é o nome do AGENTE (em `04-SYSTEM/automation/procedures/core/ingest-report.md`), não
o path de output.

**Causa**: O subagente despachado para FASE 3 não conhecia o path canônico e usou
o nome do agente como diretório. O operador não verificou o path antes de aceitar
o output do subagente.

**Fix**: Ao despachar subagentes para gerar relatórios, SEMPRE especificar o path
canônico explícito: "Salve em `06-GENERATED/relatorios/YYYY-MM-DD-relatorio-semanal.md`".
Não assumir que o subagente sabe o path — ele não tem contexto do vault.

**Check**: após subagente completar, verificar se o arquivo está no path canônico.
Se não, mover com `mv` e atualizar wikilinks que apontam para o path errado.

**Evidência**: pipeline-semanal 2026-07-12, relatório salvo em `ingest-report/` em
vez de `relatorios/`. Corrigido com `mv` + patch no hot.md wikilink.

**Evidência**: pipeline-semanal 2026-07-12 batch_aa, 29 entries → 22 source pages
created (20 full + 2 duplicate stubs), 7 `_2.md` variants skipped (files missing
from 00-INBOX/clippings/). All pages follow template F2.3a. Only existing concepts/entities
linked — no stubs created. No manifest updated, no files moved.

---

## Implementações dos checks C6–C11

Movidas de `skills/ingest-verify.md` em 2026-08-01. O entry lista
cada check em uma linha; o bash que o executa vive aqui.

### C6 — Concept Absorption (F2.5) `[bash]`

**Princípio**: source pages não devem apenas linkar concepts — devem ter
atualizado os concepts com nova evidência (seção `## Evidências` no concept).

```bash
VAULT=~/Obsidian/vault-michel
CONCEPT_LINKS=$(grep -oE '\[\[03-RESOURCES/concepts/[^]|]+\]\]' "$arquivo" | \
  sed 's/\[\[03-RESOURCES\/concepts\///;s/\]\]//' | sort -u)

for concept in $CONCEPT_LINKS; do
  CONCEPT_FILE="$VAULT/03-RESOURCES/concepts/${concept}.md"
  if [[ -f "$CONCEPT_FILE" ]]; then
    SOURCE_SLUG=$(basename "$arquivo" .md)
    if ! grep -q "$SOURCE_SLUG" "$CONCEPT_FILE" 2>/dev/null; then
      echo "C6 WARN: concept $concept não absorveu $SOURCE_SLUG"
    fi
  fi
done
echo "C6 OK"
```

**Veredicto:** OK / WARN / Skip. Só válido para ingests pós-2026-06-18.

### C7 — Personal Reflection (F2.9) `[bash]`

**Princípio**: sources com `reflect: true` devem ter seção `## Minha Síntese` cobrindo 3
aspectos: "o que muda no mental model", "conexão com trabalho do vault",
"próximo passo acionável". (Sob o modelo binário v2.1 o gate é `reflect: true`, não
o antigo tier "Score A" — ver migration-triagem-binary.) Aceita DOIS formatos:

- **Formato estruturado** (labels bold): `**O que muda**`, `**Conexão pessoal**`,
  `**Próximo passo**` como linhas prefixadas.
- **Formato prosa** (2-4 linhas): texto corrido cobrindo os 3 aspectos sem
  labels bold. O usuário pode requestar este formato explicitamente
  ("2-4 linhas sobre: o que muda, conexão, próximo passo").

C7 deve aceitar ambos — não WARN em formato prosa válido.

```bash
# Gate binário: reflect: true no frontmatter (não mais tier "Score A")
REFLECT=$(grep -m1 '^reflect:' "$arquivo" | awk '{print $2}')
if [[ "$REFLECT" == "true" ]]; then
  if grep -q "^## Minha Síntese" "$arquivo"; then
    # Formato estruturado (bold labels)
    if grep -q "^\*\*O que muda" "$arquivo" && \
       grep -q "^\*\*Conexão pessoal" "$arquivo" && \
       grep -q "^\*\*Próximo passo" "$arquivo"; then
      echo "C7 OK (structured)"
    # Formato prosa (2+ linhas de conteúdo após o heading)
    else
      LINE_COUNT=$(grep -A1 "^## Minha Síntese" "$arquivo" | grep -v "^## Minha Síntese" | grep -v "^$" | wc -l)
      if [[ $LINE_COUNT -ge 2 ]]; then
        echo "C7 OK (prose)"
      else
        echo "C7 WARN: Minha Síntese incompleta (nem structured nem prose ≥2 linhas)"
      fi
    fi
  else
    echo "C7 FAIL: reflect:true sem seção Minha Síntese"
  fi
else
  echo "C7 SKIP: reflect != true"
fi
```

**Veredicto:** OK (structured) / OK (prose) / WARN / FAIL / SKIP. Só artigos/ai-agents (não FIAP).

### C8 — Batch Link Integrity (pós-batch) `[bash]`

**Princípio**: C2 verifica por arquivo. C8 verifica o batch inteiro. Links quebrados
são visíveis no agregado, não por arquivo. Se >5% dos links do batch não resolvem,
algo sistêmico está errado (ex: ingest script gerou paths inválidos).

O pitfall que motivou este check está em `## C2 pitfalls — wikilink resolution`,
acima; não repetido aqui.

```bash
# Rodar APÓS processar todos os arquivos do batch
BROKEN=0
TOTAL=0
for f in $BATCH_SOURCES; do
  links=$(grep -oE '\[\[03-RESOURCES/(concepts|entities)/[^\]]+\]\]' "$f" 2>/dev/null)
  for link in $links; do
    TOTAL=$((TOTAL+1))
    path=$(echo "$link" | sed 's/\[\[//;s/\]\]//')
    [[ -f "$VAULT/$path.md" || -f "$VAULT/$path" ]] || BROKEN=$((BROKEN+1))
  done
done
if [[ $TOTAL -gt 0 ]]; then
  PCT=$((BROKEN*100/TOTAL))
  [[ $PCT -gt 5 ]] && echo "C8 FAIL: $BROKEN/$TOTAL links broken ($PCT%) — batch link integrity compromised" || echo "C8 OK: $BROKEN/$TOTAL broken ($PCT%)"
else
  echo "C8 SKIP: no concept/entity links in batch"
fi
```

**Veredicto:** OK / FAIL. Se FAIL, abortar pipeline e reparar links antes do commit.

### C9 — Placeholder Detection `[bash]`

**Princípio**: F2.9 Personal Reflection deve ter conteúdo real, não placeholders.
C7 verifica se a seção existe mas não detecta conteúdo placeholder como
"A ser analisado em revisão manual" ou "A ser conectado com projetos".

**Pitfall (2026-06-23 run 2):** 100 source pages com `## Minha Síntese` contendo
apenas "A ser analisado em revisão manual" passaram pelo C7.

```bash
REFLECT=$(grep -m1 '^reflect:' "$arquivo" | awk '{print $2}')
if [[ "$REFLECT" == "true" ]]; then
  if grep -q "^## Minha Síntese" "$arquivo"; then
    # Detectar placeholders
    if grep -qE "(A ser analisado|A ser conectado|placeholder|TODO|TBD|Nenhum próximo passo imediato.*revisão)" "$arquivo" | grep -A5 "## Minha Síntese"; then
      echo "C9 WARN: Minha Síntese contém placeholder"
    fi
    # Verificar se os 3 campos têm conteúdo real (não apenas label)
    OQM=$(grep -A1 "^\*\*O que muda" "$arquivo" | tail -1 | wc -w)
    CP=$(grep -A1 "^\*\*Conexão pessoal" "$arquivo" | tail -1 | wc -w)
    PP=$(grep -A1 "^\*\*Próximo passo" "$arquivo" | tail -1 | wc -w)
    [[ $OQM -lt 3 || $CP -lt 3 || $PP -lt 3 ]] && echo "C9 WARN: Minha Síntese campos curtos demais (OQM=$OQM CP=$CP PP=$PP)"
    echo "C9 OK"
  else
    echo "C9 FAIL: reflect:true sem seção Minha Síntese"
  fi
else
  echo "C9 SKIP: reflect != true"
fi
```

**Veredicto:** OK / WARN / FAIL / SKIP.

---

### C9 — Source page depth vs original clipping `[bash]`

**Princípio**: source page deve preservar informação relevante do clipping
original — não condensar artificialmente. Guardrail "profundidade > brevidade".

```bash
ORIGINAL_SIZE=$(wc -c < "$original_clipping" 2>/dev/null || echo 0)
PAGE_SIZE=$(wc -c < "$arquivo" 2>/dev/null || echo 0)

# Ratio: if page < 5% of original, likely a stub
if [[ "$ORIGINAL_SIZE" -gt 0 ]]; then
  RATIO=$(python3 -c "print(f'{$PAGE_SIZE/$ORIGINAL_SIZE*100:.1f}')")
  if (( $(python3 -c "print(1 if $PAGE_SIZE/$ORIGINAL_SIZE < 0.05 else 0)") )); then
    echo "C9 WARN: source page is ${RATIO}% of original (${PAGE_SIZE}b vs ${ORIGINAL_SIZE}b) — possible thin page"
  else
    echo "C9 OK: ${RATIO}% of original"
  fi
fi
```

**Veredicto:** OK / WARN: page < 5% do original. Não é FAIL — alguns clippings
são 90% boilerplate/menus. Mas < 5% com conteúdo técnico no original é suspeito.

**Achado**: pipeline-semanal 2026-06-22 spot-check encontrou page de 739 bytes
vs clipping original de 8660 bytes (8.5%) — era um stub real, expandido para
7020 bytes (81%) após correção.

### C10 — Categoria correta `[bash]`

**Princípio**: source pages devem estar no diretório correto conforme categoria.
Papers acadêmicos sobre "fiscal policy" ou "tributação de algoritmos" não são
"concurso" — são articles ou ai-agents.

O pitfall que motivou este check está em `## C10 pitfalls — categorização`,
acima; não repetido aqui.

```bash
# Check: se source page está em 02-AREAS/concurso/sources/ mas não contém
# keywords de concurso (CESPE, CEBRASPE, FGV, FCC, SEFAZ, servidor público)
CONCURSO_KEYWORDS="CESPE|CEBRASPE|FGV|FCC|SEFAZ|servidor público|carreira pública|concurso"
CATEGORY_DIR=$(echo "$arquivo" | grep -oE '02-AREAS/concurso/sources/')
if [[ -n "$CATEGORY_DIR" ]]; then
  if ! grep -qiE "$CONCURSO_KEYWORDS" "$arquivo"; then
    echo "C10 WARN: source page in concurso/ but no concurso keywords found — possible miscategorization"
  else
    echo "C10 OK"
  fi
else
  echo "C10 SKIP: not in concurso dir"
fi
```

**Veredicto:** OK / WARN: possível miscategorização / SKIP: não é concurso.


### C11 — Evidence Boundary / Anti-drift `[bash+Haiku]`

**Princípio** (agentkit-seo grounding): reescrita repetida causa *fact drift* —
claim de alta consequência ganha certeza que a fonte não sustenta. Gate **ativo**
(não só rotula como epistemic-tagging passivo): toda claim de alta consequência
numa source page exige lastro na fonte bruta OU rebaixa para `[hyp]`/`[não-verificado]`.

Alta consequência = número, lei/norma, preço, data, atribuição de autoria, causal forte
("X causa Y"). Separa fato verificado de aspiração/inferência.

```bash
# 1. Claims taggeadas [obs] devem ter lastro na fonte bruta (.raw ou clipping original)
# find (não glob) — evita "no matches found" em zsh
RAW=$(find .raw -maxdepth 2 -name "*$SOURCE_SLUG*" 2>/dev/null | head -1)
grep -nE '\[obs\]' "$arquivo" | while read -r line; do
  # claim [obs] com número/lei/preço deve aparecer no source bruto
  claim=$(echo "$line" | grep -oE '[0-9]+([.,][0-9]+)?|art\.[ ]?[0-9]+|R\$[ ]?[0-9]+')
  if [[ -n "$claim" && -n "$RAW" ]]; then
    grep -qF "$claim" "$RAW" || echo "C11 WARN: [obs] claim '$claim' sem lastro na fonte bruta → rebaixar p/ [interp]/[hyp]"
  fi
done
# 2. Claims causais fortes sem tag epistêmica → WARN (força tag)
grep -niE '\b(causa|garante|prova que|sempre resulta em|comprova)\b' "$arquivo" | \
  grep -vE '\[(obs|interp|hyp)\]|não-verificado' && \
  echo "C11 WARN: claim causal sem tag epistêmica — add [interp]/[hyp] ou lastro"
echo "C11 OK"
```

**Veredicto:** OK / WARN: claim sem lastro (rebaixar tag) / SKIP: sem `.raw` disponível.
Nunca FAIL — anti-drift é forward-only (não retroage páginas antigas, ver CLAUDE.md
epistemic tagging). Liga a [cite-or-flag](../../cite-or-flag/SKILL.md) (mesmo mecanismo,
aplicado a source pages) e epistemic-tagging concept.

---

## Post-pipeline proactive patching (preferência do usuário)

Após `pipeline-semanal` ou qualquer rotina multi-fase, patchear proativamente as
skills/agentes/rotinas afetadas — bugs observados **e** otimizações — na mesma
sessão, antes de o usuário pedir. O sinal do usuário costuma ser "nenhuma melhoria
em skills, hooks, agentes, rotinas existentes?".

1. Varrer os outputs da rotina em busca de bugs e oportunidades
2. Registrar o pitfall observado na skill afetada
3. Registrar o passo de otimização (novo check, fluxo melhor)
4. Ligar agentes/rotinas a skills ainda não conectadas
5. Atualizar memória com fatos estáveis (contagens, version bumps)
6. Commitar tudo atomicamente

---

Histórico de versões: `git log` deste arquivo.
