---
name: adversarial-probe
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/reasoning/hill-climb/probe.md
mode: "B3"
consolidated-by: adr-nx-014
created: 2026-08-27
updated: 2026-09-25
version: 2.0.0
tags: [adversarial, behavioral-drift, testing]
id: adversarial-probe
description: "Ponteiro do MODO B3 de probe: casos adversariais de drift (scope creep, identidade, escalação) para a etapa B3 do system-audit. Não é skill invocável."
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 0 secoes, 25 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
> **Não é skill invocável.** Absorvida como `## MODO B3 — casos de drift (system-audit)`
> de [probe](probe.md) em 2026-09-25 (adr-nx-014).

Os 3 tipos daqui (scope creep, identity violation, escalation) eram subconjunto
das 7 categorias de probe. O procedimento (2 casos por agente ligados ao drift
medido, Expected antes de rodar, execução sem efeito externo, formato de output)
vive agora no modo B3. Quem chama:
PB-agent-drift, etapa B3.

Conteúdo anterior: `git show d88fedb2d:04-SYSTEM/automation/skills/reasoning/hill-climb/adversarial-probe.md`.
