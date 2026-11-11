---
name: context-handoff
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/orchestration/subagent-team/SKILL.md
mode: "BRIEF"
consolidated-by: adr-nx-019
created: 2026-06-19
updated: 2026-09-25
version: 2.0
tags: [orchestration, context, delegation]
description: "Ponteiro do MODO BRIEF de subagent-team: destilar a sessão em campos de TaskPacket antes de delegar. Não é skill invocável."
reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 0 secoes, 25 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
> **Não é skill invocável.** Absorvida como `## MODO BRIEF — destilar a sessão em
> TaskPacket` de [subagent-team](SKILL.md)
> em 2026-09-25 (adr-nx-019).

O único chamador era o PASSO 2 de subagent-team. O formato de brief próprio
(Decisões / Restrições / Estado / Tarefa / Fora do escopo / Ignorar) competia com
o TaskPacket, que é canônico para todo briefing de agente. O modo mantém o filtro
por destino e o limite de 30 linhas, e emite `evidence`, `negatives`, `objective`
e `scope.deny`.

Conteúdo anterior: `git show a255af6ca:04-SYSTEM/automation/skills/orchestration/subagent-team/context-handoff.md`.
