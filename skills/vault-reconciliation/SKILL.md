---
kind: skill-proc
resolver-status: exposed
type: skill
name: vault-reconciliation
input:
  required_fields: [scope]
output:
  format: json
triggers:
  positive:
    - "reconciliar archive"
    - "fonte órfã"
    - "link quebrado entre sources"
    - "duplicata de source"
    - "arquivo sumiu do disco entre scan e processamento"
    - "file evaporation no pipeline"
  negative:
    - "ingerir item novo"
    - "triagem de inbox"
allowed_effects:
  - read 03-RESOURCES/
  - read 04-SYSTEM/
  - read 06-GENERATED/
  - write 06-GENERATED/audits/
forbidden_effects:
  - write 03-RESOURCES/
  - write 04-SYSTEM/
  - delete source pages
  - modify manifest
  - modify agent files
version: 2.0.0
source_agent: vault-reconciliation
status: active
created: 2026-08-20
description: "Use when: reconcilar archive vs vault (órfãs, links, dupes) ou arquivo evaporado entre scan e processamento — pós-ingest; entrada de item novo vai para pipeline-drain. drift-review cuida de docs×código e pre-ingest-dedup barra duplicata ANTES do ingest: link quebrado ou duplicata entre sources já no vault é aqui."
updated: 2026-10-24
reviewed: 2026-10-24
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Reescrita como ponteiro em 2026-10-24: o procedimento antigo (find/xargs em /tmp, slug por tr, ler raw inteiro) foi superado pelo workflow vault-reconcile-semanal.md e pelos scripts reconcile-gate.py, vault-reconcile-baseline.py e vault-reconcile-join.py. Conferido: docstrings dos tres scripts (gate de idade 14d, matcher sem fuzzy em tiers, join por transliteracao), route/capabilities e modelos do workflow (opus-5-5 medium orquestra, Sonnet 5.5 low na FASE 1 por HR1). Contradicao corrigida: o frontmatter antigo declarava write 03-RESOURCES/ e write 04-SYSTEM/ enquanto o corpo dizia recommendation-only; allowed_effects agora so escreve o relatorio. NAO conferido: corpo completo do workflow alem do cabecalho e do NEXUS GATE; gate DS-18. W5 2026-11-10: modo EVAPORATION fundido (modo-evaporation.md, recommendation-only); shield (opus, somente leitura) conferiu escrita so em 06-GENERATED/audits/, script do passo 3 sem escrever o manifest, triggers sem duplicata e referencias (BLOCK de referencia residual em ingest-verify corrigido em W5b). NAO conferido: existencia de writer de manifest com gate DS-18; find em 08-ARCHIVE sob hook headless."
---

# vault-reconciliation — archive vs vault (semanal)

> **Fonte de verdade:** workflow vault-reconcile-semanal e os scripts
> `reconcile-gate.py`, `vault-reconcile-baseline.py` e `vault-reconcile-join.py` em `04-SYSTEM/scripts/`. Esta página só
> orienta; se divergir deles, eles valem.
> Procedimento histórico (find/xargs em `/tmp`): `git show 24cf4b348:04-SYSTEM/automation/skills/pipeline/vault-reconciliation/SKILL.md`.
>
> **Proveniência:** transplantado de `04-SYSTEM/automation/agents/nexus-agent-system/vault-reconcile.md` @ `6304e261b` (S1, 2026-08-23); reescrito como ponteiro em 2026-10-24. Decisão original: adr-nx-002-vault-reconcile-agent.

## O que faz

Detecta drift entre os raws de `08-ARCHIVE/approved/**` e as source pages de `03-RESOURCES/sources/`. **Só `approved/`**:
`disapproved/` foi rejeitado na triagem. Legado `08-ARCHIVE/{A,B,C,D}/` está congelado.

**Recommendation-only (DS-14).** O adapter só escreve o relatório em `06-GENERATED/audits/`. Propõe append, concept ou entity
faltante e registra wikilink quebrado; não corrige link, não reescreve source page, não cria stub. O Nexus (writer único)
materializa a partir do relatório, sob o gate DS-18.

## Ferramentas determinísticas (0 token)

| Script | Papel |
|--------|-------|
| `reconcile-gate.py` | inventário e gate de idade (14 dias) de `approved/`: `total`, `fresh_lt14d`, `aged_gt14d`, `aged_files`. Python por dentro porque o hook de leitura em massa bloqueia `find`/`ls` em `08-ARCHIVE` em sessão headless |
| `vault-reconcile-baseline.py` | matcher raw→source sem fuzzy, em tiers: source-id, content-hash, normalized-url, alias-redirect, exact-stem, provenance-list; sem match = resíduo. Read-only |
| `vault-reconcile-join.py` | join por transliteração de acento (`Métrica` → `metrica`), também pelo `title:`; slug degenerado vira classe própria. Read-only |

Decisão do gate: `total=0` → pular; `aged=0` → só cobertura determinística; `aged>0` → fase semântica só sobre os raws >14 dias.
A fase semântica lê conteúdo derivado de clipping web: roda em Sonnet 5.5 · low por Hard Rule 1 (ver o workflow).

## Categorias de gap no relatório

`missing-section` (propor append) · `missing-concept` · `missing-entity` · `broken-wikilink` (registrar) · `ok`.
Toda proposta traz tipo, path alvo, evidência citável (raw + trecho) e texto proposto. Raw sem source page: flag para ingest
futuro; não delegue a `ingest-proposal` daqui. Wikilinks propostos têm de resolver.

## Restrições

- Sem subagente recursivo: reconcile é trabalho determinístico direto (lição 2026-07-01: recursão estoura o limite de sessão).
- Só archive >2 semanas; archive fresco tem drift 0.
- Mais de 50 correções propostas: pedir aprovação.
- Handoff humano: `[DECISION NEEDED]` ao Nexus antes de materializar em path canônico, em contradição raw×source
  irreconciliável ou em erro inesperado.

## Modos

- **EVAPORATION** — arquivo some do disco entre o scan e o processamento (`candidates_new.txt` com path ausente, ou "0 ingested" com candidatos): leia [modo-evaporation](modo-evaporation.md). Mesma regra recommendation-only (DS-14): a proposta de entrada retroativa de manifest vai para `06-GENERATED/audits/` e o Nexus materializa.

## Quando NÃO usar

- Item novo do INBOX → `pipeline-drain` (F0–F3). Classificação de candidato → `triage-classification`.
- Duplicata antes do ingest → `pre-ingest-dedup`. Docs×código → `drift-review`.

## Failure modes

- Reescrever source page (perde informação e trilha).
- Corrigir wikilink sem decisão (pode estar conceitualmente certo).
- Materializar direto do adapter.
- Pular o relatório (é o produto principal).
- Rodar diariamente (custo sem ganho).

## Políticas

memory-layer · context-engineering · safety-and-approvals
