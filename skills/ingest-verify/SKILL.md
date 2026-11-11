---
origin: native
status: active
kind: skill-proc
resolver-status: exposed
name: ingest-verify
skill: ingest-verify
version: 2.9
type: skill
updated: 2026-10-28
trigger: "@ingest-verify [path] or post-pipeline gate or verify agent"
tags: [verification, ingest, quality-gate, completeness, post-ingest]
model-profile: economy
description: "Use when: @ingest-verify [path] / post-pipeline gate / verify agent — valida COMPLETENESS de source pages recém-ingestadas (frontmatter, wikilinks, tese central, manifest, seções). Diferente de [triage-scoring](../triage-classification/triage-scoring.md) (pontuação de candidato a ingest antes de entrar); ingest-verify é validação de página já ingerida."
reads:
  - 03-RESOURCES/sources/
  - 02-AREAS/concurso/sources/
  - 02-AREAS/fiap/sources/
  - 03-RESOURCES/concepts/
writes: []
triggers:
  positive:
    - "@ingest-verify [path]"
    - "pós-ingest de source page"
    - "gate pós-pipeline"
    - "verificar ingest"
  negative:
    - "pré-ingest"
    - "triagem de candidatos (triagem-scoring)"
    - "dedup de clippings (pre-ingest-dedup)"
consumes: ["source-page", "manifest"]
tools: []
references:
verifier: ["Require todos os checks de completeness rodados (frontmatter, wikilinks, tese, manifest) e findings reportados com evidência."]
human_gate: false
reviewed-scope: "checagem mecanica + semantica: 15/15 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 15 secoes, 315 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---



# Skill: Ingest Verify

## Propósito

Valida completeness de source pages recém-ingestadas. Detecta: frontmatter incompleto, wikilinks quebrados, stubs sem tese central, ausência no manifest, seções obrigatórias faltando, concept absorption pendente, reflection missing.

Tipo: **Verification skill** — garante que ingest não termina com pages quebradas ou vazias.

## Condições de Ativação

- Após qualquer ingest de source page (individual ou em batch)
- Antes de marcar pipeline como CONCLUÍDO
- `@ingest-verify [caminho_ou_glob]` ou "verifica ingest"
- Trigger automático do agente `verify` ao encerrar sessão de ingest

## Passo 0 — Judge determinístico (obrigatório, antes de qualquer verificação por modelo)

```bash
python3 04-SYSTEM/scripts/judge-ingest.py --scan 03-RESOURCES/sources --quiet
python3 04-SYSTEM/scripts/judge-ingest.py --scan 02-AREAS/fiap/sources --quiet
```

A segunda linha cobre as páginas FIAP (`02-AREAS/fiap/sources/`), que o ingest de apostila grava lá. Ela sai com exit ≠ 0 enquanto o passivo legado existir (5 FAIL hard `campos-minimos`, sem `type`, em 2026-10-28): para fase nova, rode o judge só sobre o glob da fase (`fiap-fase-NN-*.md`), como em `ingest-fiap-batch` passo 5.

Regras em ingest-rulebook — **fonte única**. Exit 0 = nenhum FAIL hard.

Por que primeiro: custa zero token e pega a classe que mais reincidiu (título duplicado do
`generate_resumo()`, 14 ocorrências antes do gate). Sem parada determinística, o agente encerra
por "sensação" e a classe volta.

**Se reprovar:** corrigir o arquivo **e** verificar se a regra já existe no rulebook. Classe
nova → escrever a regra e o check primeiro, reparar depois. Reparar sem gatear foi
exatamente o que produziu as 14 reincidências.

**Revisor ≠ produtor:** quem revisa lê o rulebook e o output, nunca o raciocínio de quem
produziu — verifier que herda o contexto do worker é loop disfarçado de gate. Ver
graph-engineering.

## Checks

**C1 — Frontmatter completo.** Campos obrigatórios: `title`, `type`, `created`, `updated`, `tags`.

**C1.5 — Sem frontmatter embutido (F6 W1 2026-08-03).** Nenhum bloco `^---\s*\n(?:title|type|created|updated|tags):` no corpo após o 1º frontmatter (YAML do clipping colado pelo ingest). FAIL se houver — família second-frontmatter, 458 ocorrências históricas (errors.md).

**C2 — Wikilinks resolvem.** Extrair todos `link` e verificar existência. Sempre fazer fallback por basename (stem lookup) antes de reportar broken — Obsidian resolve por basename, não path completo (ver reference C2). >5% quebrados → FAIL.
```bash
BROKEN=0; TOTAL=0
for f in "$SOURCES_DIR"/*.md; do
  for link in $(grep -oE '\[\[03-RESOURCES/(concepts|entities)/[^]]+\]\]' "$f"); do
    TOTAL=$((TOTAL+1)); path=$(echo "$link" | sed 's/\[\[//;s/\]\]//')
    [[ -f "$VAULT/$path.md" || -f "$VAULT/$path" ]] || BROKEN=$((BROKEN+1))
  done
done
PCT=$((BROKEN*100/TOTAL))
[[ $PCT -gt 5 ]] && echo "FAIL: $BROKEN/$TOTAL ($PCT%)" || echo "OK: $BROKEN/$TOTAL ($PCT%)"
```

**C3 — Tese central presente.** Ao menos 1 parágrafo explicando o que a fonte afirma. Deve NÃO começar com metadata do Clipping (`author:`, `source:`, `published:`, `---`) — se começar → FAIL (ver reference C3).
```bash
TESE_CONTENT=$(grep -i -A2 "^## Tese Central" "$arquivo" | tail -1)
echo "$TESE_CONTENT" | grep -qE "^(author:|source:|published:|original_title:|---|title:|type:|created:|updated:|tags:)" \
  && echo "C3 FAIL: Tese Central contains Clipping metadata, not content"
```

**C4 — Manifest entry existe.** Source page registrada em `.raw/.manifest.json`.

**C5 — Seções obrigatórias.** Pelo menos 1 heading `##` + pelo menos 1 wikilink `...`.

**C6 — Concept Absorption (F2.5)** `[bash]`. Source pages não devem só linkar concepts — devem ter atualizado os concepts com nova evidência. Só válido para ingests pós-2026-06-18.
```bash
CONCEPT_LINKS=$(grep -oE '\[\[03-RESOURCES/concepts/[^]|]+\]\]' "$arquivo" | sed 's/\[\[03-RESOURCES\/concepts\///;s/\]\]//' | sort -u)
for concept in $CONCEPT_LINKS; do
  CF="$VAULT/03-RESOURCES/concepts/${concept}.md"
  [[ -f "$CF" ]] && ! grep -q "$(basename "$arquivo" .md)" "$CF" 2>/dev/null && echo "C6 WARN: concept $concept não absorveu source"
done
echo "C6 OK"
```

**C7 — Personal Reflection (F2.9)** `[bash]`. Sources com `reflect: true` devem ter `## Minha Síntese` cobrindo: o que muda no mental model, conexão com trabalho, próximo passo. Aceita DOIS formatos: estruturado (bold labels) OU prosa (≥2 linhas). Gate binário v2.1 = `reflect: true` (não tier "Score A"). SKIP para FIAP.
```bash
REFLECT=$(grep -m1 '^reflect:' "$arquivo" | awk '{print $2}')
if [[ "$REFLECT" == "true" ]]; then
  if grep -q "^## Minha Síntese" "$arquivo"; then
    if grep -q "^\*\*O que muda" "$arquivo" && grep -q "^\*\*Conexão pessoal" "$arquivo" && grep -q "^\*\*Próximo passo" "$arquivo"; then
      echo "C7 OK (structured)"
    else
      LC=$(grep -A1 "^## Minha Síntese" "$arquivo" | grep -v "^## Minha Síntese" | grep -v "^$" | wc -l)
      [[ $LC -ge 2 ]] && echo "C7 OK (prose)" || echo "C7 WARN: Minha Síntese incompleta"
    fi
  else echo "C7 FAIL: reflect:true sem seção Minha Síntese"; fi
else echo "C7 SKIP: reflect != true"; fi
```

**C8 — Batch Link Integrity (pós-batch)** `[bash]`. C2 verifica por arquivo; C8 verifica o batch inteiro. Se >5% dos links do batch não resolvem → FAIL. Abortar pipeline e reparar antes do commit. (Mesma lógica bash do C2 rodada sobre `$BATCH_SOURCES`.)

**C8b — Wikilink points to directory, not file** `[bash]`. `_index.md` é resolvível no Obsidian — só WARN se nem arquivo nem `_index.md` existem.
```bash
for link in $(grep -oE '\[\^+\]\]' "$arquivo" | sed 's/\[\[//;s/\]\]//;s/|.*//'); do
  [[ -f "$VAULT/${link}.md" || -f "$VAULT/${link}/_index.md" ]] && continue
  found=$(find "$VAULT" -iname "$(basename "$link")*.md" -type f 2>/dev/null | head -1)
  [[ -z "$found" ]] && echo "C8b WARN: '$link' resolves to neither file nor _index.md"
done; echo "C8b OK"
```

**C9 — Placeholder Detection** `[bash]`. C7 verifica presença; C9 detecta placeholder ("A ser analisado", "TODO", "TBD") e campos curtos demais (<3 palavras). Calibração: batch AI → placeholder é FAIL válido; batch programático → placeholder é WARN esperado (dívida técnica, ver reference).
```bash
if [[ "$REFLECT" == "true" ]] && grep -q "^## Minha Síntese" "$arquivo"; then
  grep -A5 "## Minha Síntese" "$arquivo" | grep -qE "(A ser analisado|A ser conectado|placeholder|TODO|TBD)" && echo "C9 WARN: placeholder"
  OQM=$(grep -A1 "^\*\*O que muda" "$arquivo" | tail -1 | wc -w)
  CP=$(grep -A1 "^\*\*Conexão pessoal" "$arquivo" | tail -1 | wc -w)
  PP=$(grep -A1 "^\*\*Próximo passo" "$arquivo" | tail -1 | wc -w)
  [[ $OQM -lt 3 || $CP -lt 3 || $PP -lt 3 ]] && echo "C9 WARN: campos curtos (OQM=$OQM CP=$CP PP=$PP)"
  echo "C9 OK"
fi
```

**C9b — Source page depth vs original clipping** `[bash]`. Se page < 5% do original → WARN (possível stub thin). Não FAIL — boilerplate varia.
```bash
OS=$(wc -c < "$original_clipping" 2>/dev/null || echo 0); PS=$(wc -c < "$arquivo")
[[ "$OS" -gt 0 ]] && python3 -c "print('C9b WARN: thin' if $PS/$OS<0.05 else 'C9b OK')"
```

**C10 — Categoria correta** `[bash]`. Source pages devem estar no diretório correto. Papers de "fiscal policy"/"tributação de algoritmos" não são "concurso".
```bash
KW="CESPE|CEBRASPE|FGV|FCC|SEFAZ|servidor público|carreira pública|concurso"
if echo "$arquivo" | grep -qE '02-AREAS/concurso/sources/'; then
  grep -qiE "$KW" "$arquivo" && echo "C10 OK" || echo "C10 WARN: em concurso/ sem keywords — possível miscategorização"
else echo "C10 SKIP"; fi
```

**C11 — Evidence Boundary / Anti-drift** `[bash+Haiku]`. Gate ativo: toda claim de alta consequência (número, lei, preço, data, autoria, causal forte) numa source page exige lastro na fonte bruta OU rebaixa para `[hyp]`/`[não-verificado]`. Forward-only — nunca FAIL, nunca retroage. Liga a [cite-or-flag](../cite-or-flag/SKILL.md).
```bash
RAW=$(find .raw -maxdepth 2 -name "*$SOURCE_SLUG*" 2>/dev/null | head -1)
grep -nE '\[obs\]' "$arquivo" | while read -r line; do
  claim=$(echo "$line" | grep -oE '[0-9]+([.,][0-9]+)?|art\.[ ]?[0-9]+|R\$[ ]?[0-9]+')
  [[ -n "$claim" && -n "$RAW" ]] && ! grep -qF "$claim" "$RAW" && echo "C11 WARN: [obs] '$claim' sem lastro → rebaixar tag"
done
grep -niE '\b(causa|garante|prova que|sempre resulta em|comprova)\b' "$arquivo" | grep -vE '\[(obs|interp|hyp)\]|não-verificado' && echo "C11 WARN: claim causal sem tag epistêmica"
echo "C11 OK"
```

## Protocolo de Execução

1. Passo 1 (bash, 0 tokens): checks C1, C2, C4, C5, C6 e C7.
2. Passo 2 (Haiku): C3, tese central, só se C4 não falhou.
3. Passo 3 (Haiku): compilar o relatório com veredicto APROVADO, AVISO ou REJEITAR.

Se precisar decidir qual modelo roda cada etapa, leia [modelo por etapa](reference/06-modelo-por-etapa.md).

Relatório: `=== INGEST-VERIFY | <timestamp> === / Arquivo: <path>` seguido de cada check (C1–C7) com `OK | WARN | FAIL | SKIP` + evidência, e linha final `VEREDICTO: APROVADO | AVISO (X) | REJEITAR (Y)`.

- `APROVADO`: todos C1–C7 passam (WARN permitidos)
- `AVISO`: C3=STUB ou C5=sem wikilinks ou C6=absorption pendente
- `REJEITAR`: qualquer C1, C2, C4, C7=FAIL, ou C3=EMPTY

## Restrições

- NUNCA modificar arquivo verificado — apenas reportar
- C3 stub: WARN, nunca FAIL — stub pode ser intencional

**Critério de sucesso:** checks executados com evidência (OK, WARN ou FAIL) e relatório de verificação com veredicto entregue.

## Completion

- [ ] Checks C1–C11 executados com evidência (PASS / WARN / FAIL)
- [ ] Source pages com ratio < 5% (stub): flag WARN
- [ ] Wikilinks apontando para diretórios sem `_index.md`: flag FAIL
- [ ] Categoria correta verificada (C10): keywords match contexto
- [ ] Relatório de verificação entregue

## Relatório

```
=== INGEST-VERIFY | <timestamp> ===
Arquivo: <path>

CHECKS:
  C1  Frontmatter:   OK | FAIL
  C2  Wikilinks:     OK | FAIL: dead links
  C3  Tese central:  OK | WARN: STUB | FAIL: EMPTY
  C4  Manifest:      OK | FAIL
  C5  Seções:        OK | WARN | FAIL
  C6  Absorption:    OK | WARN: N concepts sem evidência
  C7  Reflection:    OK | WARN | FAIL | SKIP
  C8  Batch links:   OK | FAIL: >5% quebrados
  C8b Directory link: OK | WARN | FAIL
  C9  Placeholder:   OK | WARN
  C9b Depth ratio:   OK | WARN: < 5% do original
  C10 Categoria:     OK | WARN | SKIP
  C11 Evidence:      OK | WARN (forward-only)

VEREDICTO: APROVADO | AVISO (X avisos) | REJEITAR (Y erros)
```

- `APROVADO`: todos passam, WARN permitidos
- `AVISO`: C3=STUB, C5 sem wikilinks, ou C6 absorption pendente
- `REJEITAR`: qualquer FAIL em C1, C2, C4, C7, C8, ou C3=EMPTY

## Failure modes

- **Stub acceptance**: aceitar page < 5% do original como completa → WARN, possível stub
- **Directory link**: wikilink aponta para diretório sem `_index.md` → FAIL
- **Miscategorization**: paper de computational finance categorizado como "concurso" por keyword "fiscal" → C10 verifica contexto, não só keyword

## Ver Também

- check-resolvable — auditar agentes vs AGENTS.md
- drift-review — profundidade de conteúdo de concepts
- **content-design** ([content-design](../content-design/SKILL.md)) — este skill valida *presença* (completeness); content-design valida *estrutura* (front-load, 1 ideia/frase). Aplicar antes de salvar: veredito/tese na linha 1.
- Histórico completo de pitfalls + changelog → a seção «Reference» deste arquivo

## Referências

`kind: reference` — carregue o arquivo antes de executar o que depende dele.

- [loose-file-categorization](loose-file-categorization.md) — cascata de categorizacao de arquivo solto
- [batch-enrichment-pipeline](batch-enrichment-pipeline.md) — pipeline de enriquecimento em lote

## Quando NÃO usar

- Auditar wikilinks globais do vault inteiro → usar `wiki-lint`
- Auditar agentes/skills registrados → usar `check-resolvable`
- Avaliar profundidade de conceitos existentes → usar `drift-review`
- Detectar evaporação conceitual temporal (concept stale >30d) → workflow `vault-reconcile-semanal`; arquivo ausente do disco → modo EVAPORATION de `vault-reconciliation`
- Dúvida de DEDUPLICAÇÃO — decidir se um clipping é duplicado/quasi-duplicado antes do ingest → usar [pre-ingest-dedup](../pre-ingest-dedup/SKILL.md).
- Clipping já processado pelo pipeline (pós-ingest) — verificação do clipping em si é outra rota; este skill audita source pages recém-ingestadas, não o clipping bruto.

---

---
status: active
parent: "[ingest-verify](SKILL.md)"
kind: reference
name: ingest-verify-reference
type: skill-reference
reviewed-scope: "checagem mecanica: 7/7 wikilinks resolvem; 5/5 paths citados existem; 0/0 scripts citados resolvem; 0 par modelo-effort invalido; kind=reference, 0 secoes, 17 linhas"
reviewed-by: claude-opus-5
reviewed: 2026-08-16
updated: 2026-08-08
---

## Ingest Verify — Reference (índice)

> Core: [ingest-verify](SKILL.md)

Reference fatiado em seções carregáveis sob demanda (2026-08-15):

- [01-pitfalls-clipping](reference/01-pitfalls-clipping.md) — pitfalls C2/C3/C7/C9/C10/C8 (wikilinks, tese central, placeholder, categorização)
- [02-batch-calibration](reference/02-batch-calibration.md) — calibração batch programático vs AI ingest, large batch patterns
- [03-pitfalls-batch-ingest](reference/03-pitfalls-batch-ingest.md) — pitfalls de batch ingest programático (wikilinks, path mismatch, F2.10)
- [04-pitfalls-manifest](reference/04-pitfalls-manifest.md) — pitfalls de manifest e links (stub bug, thin duplicates, parallel dispatch)
- [05-pitfalls-archive](reference/05-pitfalls-archive.md) — pitfalls de arquivamento e report paths (archive, relatorios, F2.9, changelog)

---

Conteúdo histórico preservado nos arquivos acima, sem edição.
