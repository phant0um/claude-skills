---
type: reference
status: active
kind: reference
name: prd-grade
description: "Spec do MODO GRADEAR de [spec-lifecycle](SKILL.md). Não é skill invocável. Avalia um PRD/spec: gates binários sim/não por critério (objetivo claro, done mensurável, escopo fechado, riscos mapeados) + decompõe em grafo de tarefas dependency-ordered com evidence-gate por nó. Use antes de delegar "
version: 2.0
tags: [spec, prd, planning, task-graph, evidence-gate, vertical-slices]
attach: [spec, nexus]
source: "anombyte93/prd-taskmaster + tweet Glaucia Lemos (vertical slices)"
updated: 2026-08-09
parent: "[spec-lifecycle](SKILL.md)"
mode: "GRADEAR"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 4/4 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 4 secoes, 52 linhas; itens do pacote R16 resolvidos (21=B, 22=B; letras = recomendacao do pacote, bloco vazio)"
reviewed-by: R17 (claude-sonnet; pacote R16)
reviewed: 2026-10-04
---
> **Não é skill invocável.** MODO GRADEAR de [spec-lifecycle](SKILL.md) — carregado por ela, não resolvido pelo router.



# Skill: prd-grade

## Propósito
Antes de codar: validar o PRD e fatiar em vertical slices ordenadas por dependência.

## Protocolo
1. **Gates binários** (sim/não, BinEval — sem nota A-F escalar). 4 perguntas atômicas:
   - Objetivo claro? (uma frase, sem ambiguidade)
   - Done mensurável? (critério verificável, não "melhorar X")
   - Escopo fechado? (o que está fora está dito)
   - Riscos mapeados? (≥1 risco + mitigação)
   **Qualquer "não" → devolver p/ refinar, NÃO executar.** Cada "não" nomeia o gap (auditável, ao contrário de "nota C"). PRD passa só com 4/4 sim.
2. **Seams de teste (`meta/spec-lifecycle`):** esboce os seams onde a feature será testada.
   Prefira seams **existentes** a novos. Use o seam **mais alto** possível. Menos seams =
   melhor; ideal = **um só**. Confirme com o user que os seams batem com a expectativa.
   Vocabulário: [codebase-design](../codebase-design/SKILL.md).
3. **Vertical slices:** decompor em issues pequenas end-to-end (não camadas).
4. **Grafo de deps:** ordem topológica. Nenhuma slice inicia sem Evidence da dependência.
5. **Evidence-gate por nó:** slice só fecha com teste/log (skill `tdd`). Sem Evidence = bloqueado.
6. **Loop:** por slice → implement → tdd → HITL → progress.md → gate contexto →
   `handoff` (@55-60%) → sessão nova. (handoff já existe — handoff-file-pattern.)

## Liga a
- `tdd` (existe) · `handoff` (existe) · `codebase-design` (novo, seams) · `domain-modeling` (novo, glossário) · T16 (prd-taskmaster).

## Completion

- [ ] PRD lido integralmente; cada secção pontuada contra a rubrica.
- [ ] Notas por critério com justificativa textual (não só nota).
- [ ] Relatório de priorização de correções (obrigatório vs opcional).
