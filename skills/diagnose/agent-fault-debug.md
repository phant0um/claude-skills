---
name: agent-fault-debug
kind: reference
type: skill
status: active
resolver-status: not-exposed
parent: 04-SYSTEM/automation/skills/reasoning/diagnose/SKILL.md
mode: "ALVO = SESSÃO DE AGENTE"
consolidated-by: adr-nx-020
created: 2026-08-09
updated: 2026-09-25
version: 2.0.0
source_repo: affaan-m/ecc
source_analysis: 03-RESOURCES/sources/github/p0/affaan-m-ecc.md
tags: [debugging, agents, recovery]
description: "Ponteiro do MODO ALVO = SESSÃO DE AGENTE de diagnose: conter e recuperar sessão de agente viva em falha (loop, 429, overflow). Não é skill invocável."
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Ponteiro: o MODO ALVO = SESSAO DE AGENTE existe em diagnose/SKILL.md; commit e693b3841 e adr-nx-020 existem."
---
> **Não é skill invocável.** Absorvida como `## MODO ALVO = SESSÃO DE AGENTE` de
> [diagnose](SKILL.md) em 2026-09-25 (adr-nx-020).

Estava em `status: quarantine` desde 0fe37fccc (2026-08-10), mas `hill` a chamava
em `calls:`; a ETAPA -1 do diagnose já a nomeava como terceiro alvo. O método
inteiro (tabela de 5 padrões, check discriminante, recovery reversível,
introspection report, lição) vive agora no modo, ao lado do MODO ALVO = OUTPUT
DE AGENTE ([trace](trace.md)). `hill` chama
`diagnose`.

Conteúdo anterior: `git show e693b3841:04-SYSTEM/automation/skills/reasoning/diagnose/agent-fault-debug.md`.
