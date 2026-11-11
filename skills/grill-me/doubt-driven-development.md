---
name: doubt-driven-development
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/foundational/grill-me/SKILL.md
mode: "PREMISSAS"
consolidated-by: adr-nx-018
created: 2026-06-19
updated: 2026-09-25
version: 2.0
source: addyosmani/agent-skills
tags: [pre-implementation, doubt, premissas]
description: "Ponteiro do MODO PREMISSAS de grill-me: enumerar premissas e classificar com 5 dúvidas, sem entrevista. Não é skill invocável."
reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 0 secoes, 25 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
> **Não é skill invocável.** Absorvida como `## MODO PREMISSAS — solo, sem
> entrevista` de [grill-me](SKILL.md) em
> 2026-09-25 (adr-nx-018).

A skill se declarava "upstream do grill" e mandava não ativar quando grill-me já
tinha rodado; o único consumidor era o próprio grill-me. O método inteiro (tipos
de premissa, dúvidas D1-D5, vereditos, output) vive agora no modo. `@doubt`
aciona o modo.

Conteúdo anterior: `git show f0b62ff0e:04-SYSTEM/automation/skills/foundational/grill-me/doubt-driven-development.md`.
