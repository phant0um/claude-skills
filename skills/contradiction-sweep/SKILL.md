---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
voice: gold
voice-register: C
name: contradiction-sweep
skill: contradiction-sweep
version: 1.0
schedule: "Bi-weekly Saturday 8 AM (after connection-finder)"
scheduler_task: revisao-semanal
tags: [routine, quality, contradictions, reconciliation, vault-health]
sources:
  - obsidian-second-brain (Eugeniu Ghelbur) — /obsidian-reconcile
  - connection-finder v2 — contradiction type
updated: 2026-09-25
description: "Use when: scan do vault por claims contraditórias entre sources/conceitos — reconciliar ou flagar para decisão humana. Diferente de [connection-finder](../connection-finder/SKILL.md) (que produz as conexões e já sinaliza contradições no scan dos últimos 7 dias); contradiction-sweep consome `06-GENERATED/reports/connections/` e reconcilia ou flaga o conflito para decisão humana."
reads:
  - 06-GENERATED/reports/connections/
writes:
  - 06-GENERATED/reports/
  - 04-SYSTEM/system/state/context/hot.md
triggers:
  positive:
    - "scan de claims contraditórias no vault"
    - "reconciliar ou flagar contradição entre fontes"
  negative:
    - "claim único sem contradição"
    - "conteúdo novo ainda não cruzado"

reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 11 secoes, 172 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
 Contradiction Sweep

Scan vault for contradictory claims across sources and concepts. Reconcile or flag for human decision.

---

## Quando NÃO usar

- **Corpus pequeno e estável** — sem fontes novas, sweep não encontra contradição nova.
- **Semana sem ingest** — rodar sweep sem material novo é custo sem retorno.
- **Conflito de opinião entre humanos** — sweep é para claims contraditórios; desacordo de preferência não é contradição.

Disambiguation: `contradiction-sweep` procura claims contraditórios; `connection-finder` procura convergências; `drift-review` audita docs vs código — sweep é semântico no vault.


## Trigger

- Scheduled: bi-weekly Saturday 8 AM
- Manual: `@contradiction-sweep` or "sweep contradictions"
- Post-connection-finder: when connection report has >2 contradictions

---

## Execution

1. Coletar pares candidatos: relatórios de conexão com seção de contradição e fontes com tags sobrepostas.
2. Classificar o tipo: factual, metodológica, temporal, perspectiva ou superseded.
3. Auto-resolver só factual ou temporal com confiança de pelo menos 80%.
4. Gerar `06-GENERATED/reports/contradiction-sweep-YYYY-MM-DD.md`; metodológicas e perspectiva vão para decisão humana.
5. Atualizar o hot cache só se houver pendentes.

### 1. Collect candidate pairs

Sources of contradictions:
```bash
cd $VAULT_DIR
# Recent connection reports with contradiction sections
grep -l "## Contradi" 06-GENERATED/reports/connections/*.md | tail -5
# Sources with overlapping tags but different conclusions
# (cross-reference via frontmatter tags)
```

Also scan:
- Concepts with >3 sources linked — higher chance of conflicting claims
- Sources from same domain published >30 days apart (knowledge evolves)

### 2. Detect contradiction types

| Type | Description | Resolution |
|------|-------------|------------|
| **Factual** | Different numbers for same metric | Find primary source, update stale one |
| **Methodological** | Same goal, opposite approach recommended | Document both with context where each applies |
| **Temporal** | Claim was true, no longer is | Add temporal marker, update concept |
| **Perspective** | Valid from different viewpoints | Create synthesis noting both perspectives |
| **Superseded** | Newer evidence invalidates older | Mark older as superseded, link to newer |

### 3. Auto-resolve (high confidence only)

Automatically fix:
- **Temporal**: source from 2024 says X, source from 2026 says NOT X with evidence -> mark 2024 claim as `[superseded YYYY-MM-DD]`
- **Factual with primary source**: official docs > blog post > social media

Do NOT auto-resolve:
- Methodological (both can be valid)
- Perspective (requires judgment)
- Any contradiction where confidence < 80%

### 4. Generate report

Output: `06-GENERATED/reports/contradiction-sweep-YYYY-MM-DD.md`

```markdown

# Contradiction Sweep

## Auto-Resolved
### [Type] Short description
- **Source A**: path — claim
- **Source B**: path — counter-claim
- **Resolution**: what was done and why
- **Confidence**: HIGH

## Pending Human Decision
### [Type] Short description
- **Source A**: path — claim
- **Source B**: path — counter-claim
- **Options**:
  A) Adopt Source A because [reason]
  B) Adopt Source B because [reason]
  C) Keep both with context note
- **Recommendation**: [A/B/C]
```

### 5. Update hot cache (only if pending items)

If pending_human > 0, append to `04-SYSTEM/system/state/context/hot.md`:
```
## Contradictions YYYY-MM-DD | N pending human decision
-> `contradiction-sweep-YYYY-MM-DD`
```

---

## Constraints

- Max 20 contradiction pairs per sweep (focus on highest impact)
- Never auto-resolve methodological contradictions
- Never delete source content — only add markers/notes
- If >20 contradictions found: likely a systemic issue (e.g., outdated domain). Flag for `review` agent
- Primary source hierarchy: academic paper > official docs > expert blog > social media

---

**Critério de sucesso:** contradições com claim, fontes e tipo; só factual ou temporal auto-resolvidas com evidência, sem source sobrescrito.

## Completion

- [ ] Contradições identificadas com: claim, source A, source B, tipo (factual/temporal/metodológica)
- [ ] Contradições factual/temporal auto-resolvidas com evidência citada
- [ ] Contradições metodológicas flagadas para decisão humana
- [ ] Source content não deletado nem sobrescrito (append-only)
- [ ] Wikilinks no report resolvem
- [ ] Primary source hierarchy respeitada (academic > official docs > expert blog > social)

## Failure modes

- **Auto-resolve metodológica**: resolver automaticamente contradição metodológica → requer decisão humana
- **Content deletion**: sobrescrever source ao reconciliar → append-only, nunca destruir informação
- **Vague pending**: deixar contradição pendente sem opções concretas → sempre ter A/B/C

---

## Quality Gate

- [ ] Every `wikilink` in report resolves
- [ ] Auto-resolved items cite evidence for resolution
- [ ] Pending items have concrete options (not vague)
- [ ] No source content was deleted or overwritten

---

## Changelog

- v1.0 (2026-05-25): Created. Inspired by Ghelbur's /obsidian-reconcile + connection-finder contradiction detection.
