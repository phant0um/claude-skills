---
name: triage-scoring
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/pipeline/triage-classification/SKILL.md
mode: "LOTE MANUAL"
consolidated-by: adr-nx-016
created: 2026-05-23
updated: 2026-10-25
version: 3.1
tags: [triagem, scoring, bash]
description: "Ponteiro do MODO LOTE MANUAL de triage-classification: gates determinísticos (triage-gates.py) para lote grande fora do pipeline. Não é skill invocável."
reviewed-scope: "2026-10-25: removido frontmatter duplicado do meio do corpo (pertencia a um arquivo de indice fundido); `git show` do conteudo anterior apontava um commit onde o arquivo nao existe, trocado por bce013b52^ (verificado com git cat-file); indice ganhou a reference 09. Conferido: docstring de triage-gates.py bate com o procedimento (G2 por word_count e hype, G1 interest, read-only, --against-state; G0 em F1.0, G3 em scan-external-skill.py). NAO conferido: a medicao 1049 decisoes/recall 0,9%/precisao 25% (numero citado de adr-nx-016, nao re-rodado) e o conteudo das 9 references."
reviewed-by: claude-sonnet-5-5 (achados: leitura direta)
reviewed: 2026-10-25
---
> **Não é skill invocável.** Absorvida como `## MODO LOTE MANUAL` de
> [triage-classification](SKILL.md) em 2026-09-25
> (adr-nx-016). G3 (scan de skill externa) virou gate da própria F1.

As duas skills emitiam `approved|disapproved` na F1, e a F1 usava estes gates
como pré-filtro ("approved direto / junk direto"). A medição de 2026-09-23
(`triage-gates.py --against-state`, 1049 decisões) deu recall de 0,9% e
precisão de 25%. O pré-filtro saiu da F1; a heurística ficou só para lote manual,
com revisão dos descartes.

O que continua aqui:

- Implementação: `04-SYSTEM/scripts/triage-gates.py` (porta de G2 e G1), teste
  em `test-triage-gates.py`.
- Heurísticas de título e conteúdo, pitfalls macOS, rescore e changelog:
  a seção «Reference» deste arquivo.

Conteúdo anterior: `git show bce013b52^:04-SYSTEM/automation/skills/pipeline/triage-classification/triage-scoring.md`.

---

## Triagem Scoring — Reference (índice)

> Core: [triage-scoring](triage-scoring.md)

Reference fatiado em seções carregáveis sob demanda (2026-08-15). Carregue só a seção necessária:

- [01-macos-compat](reference/01-macos-compat.md) — macOS Compatibility, Nexus Manual Override, File Evaporation, triagem-clipping, Guardrails
- [02-heuristics-expanded](reference/02-heuristics-expanded.md) — Expanded Heuristics for Large Batches
- [03-title-patterns](reference/03-title-patterns.md) — Extended Title Patterns (2026-06-22)
- [04-pitfalls-rescore](reference/04-pitfalls-rescore.md) — pitfalls de rescore/approval rate (macOS declare-A, drift, inflação)
- [05-dominio-extend](reference/05-dominio-extend.md) — Regra de domínio (extend)
- [06-batch-ingest-patterns](reference/06-batch-ingest-patterns.md) — Batch ingest programático, SKILL.md vs scripts, phantom paths
- [07-pitfalls-links](reference/07-pitfalls-links.md) — pitfalls de wikilinks, manifest, fix_links, F2.10, 10X
- [08-changelog](reference/08-changelog.md) — Changelog de versões
- [09-relatorio-triagem](reference/09-relatorio-triagem.md) — formato do relatório de triagem

---

O histórico completo (cronológico 2026-06-16 → 2026-07-12) foi preservado nos arquivos acima, sem edição de conteúdo.

## Procedimento do modo (movido de SKILL.md, 2026-10-11)

- **Quando:** lote manual com >20 candidatos, fora do `pipeline-drain`, onde o
  custo de uma chamada de modelo por lote pesa mais que a perda de recall.
- **Como:** `python3 04-SYSTEM/scripts/triage-gates.py FILE...` roda G2 (junk por
  word_count e sinais de spam/hype) e G1 (interest) e imprime um veredito JSON por
  arquivo. Só lê: não move nem arquiva. G0 fica no F1.0; G3 fica com
  `scan-external-skill.py`.
- **Obrigatório:** revisar à mão todo `disapproved` antes de mover. Precisão medida
  de 25%: 3 de 4 descartes da heurística eram fonte que o modelo aprovou (2 por
  `10X` no título).
- **Medir de novo:** `triage-gates.py --against-state` compara com as decisões já
  gravadas pela F1.

Saída: `decision` + `interest` por arquivo, sem `score:`/`grade:`. Os scripts
antigos (`batch_score.py` e afins) vivem no bundle Hermes com a escala A/B/C/D
aposentada; não usar.
