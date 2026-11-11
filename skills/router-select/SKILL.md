---
origin: native
kind: skill-proc
resolver-status: exposed
name: router-select
skill: router-select
version: 1.1
author: Nexus Agent System
source: Model Routing v3 (Fase 4)

id: "router-select"
title: "Skill: Router Select — pergunta de modo interativa"
type: "skill"
created: "2026-07-16"
status: "active"
updated: "2026-07-29"
tags: ["routing", "model-selection", "interactive", "grilling-pattern"]
owner: "nexus"
description: "Use when: @router-select · escolher modo de execução antes de tarefa roteada · resolver effort de deep work ambíguo. Interactive routing preflight; ask for execution mode and, when needed, effort before starting a routed task."
invocation: "user"
triggers:
  positive:
    - "@router-select"
    - "choose execution mode before routed work"
    - "resolve effort for ambiguous deep work"
  negative:
    - "mode fixed by caller"
    - "noninteractive deterministic run"
    - "task with no routing choice"
route:
  profile: "standard"
  risk: "low"
consumes: []
reads: ["task", "mode-options", "effort-signal"]
writes: []
tools: []
references: []
verifier: ["Require the mode question first, an effort question only when ambiguity is material, and a recorded selection or documented default."]
human_gate: false
reviewed-scope: "checagem mecanica + semantica: 6/6 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 11 secoes, 112 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---


# Skill: Router Select — pergunta de modo interativa

## Propósito
Confirmar **modo** (Claude é o único runtime interativo desde 2026-09-26; Codex/OpenAI removido) — e, se a tarefa for deep/ambígua, **effort** — antes de rodar uma tarefa roteada em sessão interativa. Padrão `grill-me` refinado: convergir nível a nível, opções concretas com dado, nunca abstração solta.

## Trigger nítido
- Início de tarefa roteada em sessão interativa: rotina manual, batch ingest, pipeline.

**NÃO dispara:** cron/background/subagente; tarefa <5 min; modo já escolhido nesta sessão.

## Pergunta hierárquica

1. Confirmar que o trigger dispara (não em cron, subagente, tarefa de menos de 5 min ou modo já escolhido).
2. Perguntar o modo se ainda não foi escolhido na sessão; não há alternativa Codex/OpenAI.
3. Perguntar o effort só se a tarefa for deep, ambígua ou com confidence abaixo de 0,60.
4. Sem resposta ou em cron, usar `claude` como default e registrar a assumption no log.
5. Devolver a seleção antes de agir.

**1. Modo** (sempre, se ainda não escolhido na sessão):
> "Claude (Opus 5.5·medium default e deep; effort high só advisor/security-gate)." Não há alternativa Codex/OpenAI; não perguntar, só declarar.

**2. Effort** (só se a tarefa for deep/ambígua — perfil `deep`/`critical`/`advisor` ou confidence <0.60):
> "Effort low/medium/high? Cada degrau ≈ +10% qualidade por custo multiplicativo de tokens (1 linha de custo relativo antes de perguntar)."

Não perguntar effort em tarefa `economy`/`standard`/`deterministic` sem sinal de ambiguidade — resolve pelo default do perfil (job-routing-map).

## Persistência
- Resposta de modo vale a sessão inteira (não reperguntar).
- Se o usuário expressar padrão ("sempre Claude p/ ingest") → gravar em auto-memory (`user`/`feedback`).
- Recall de memória é probabilístico → sem preferência recuperada, **perguntar ou usar default — nunca assumir silenciosamente**.

## Default sem resposta / cron
- `claude`.
- Registrar assumption + runtime escolhido no log da run (telemetria: `06-GENERATED/observability/routing-telemetry.jsonl`, campo `runtime`).

## Wiring
- Referenciado por model-routing §Ordem de decisão (passo 0: modo).
- 1 linha no firmware: AGENTS.

## Relations
- Padrão de pergunta: `grill-me`
- Política: model-routing
- IDs/perfis: model-catalog
- Mapa rotina→effort: job-routing-map

**Critério de sucesso:** modo confirmado (ou default declarado no log) e seleção devolvida antes de executar a tarefa.

## Completion

- [ ] Skill alvo consultada via ponteiro antes da execução.
- [ ] Trigger da skill combinado com o uso lido no frontmatter.
- [ ] Resultado da seleção devolvido antes de agir.

## Failure modes

- **Perguntar fora de sessão interativa**: cron, background ou subagente → ninguém responde; use o modo do contrato do job.
- **Reperguntar o modo**: pergunta repetida na mesma sessão → reuse a escolha registrada.
- **Default silencioso**: sem preferência recuperada, assumir sem declarar → pergunte ou use o default e registre a assumption.
- **Effort em tarefa simples**: perguntar effort em perfil economy/standard sem ambiguidade → resolva pelo default do perfil.

## Quando NÃO usar

- **Cron/background/subagente** — sem sessão interativa, não há quem responder a pergunta; modo vem do contrato do job.
- **Tarefa <5 min** — overhead da pergunta > tarefa; executar com default.
- **Modo já escolhido nesta sessão** — repetir a pergunta é ruído; reusar a escolha registrada.
- **Tarefa sem escolha de roteamento** — se só existe um modo válido, não perguntar.

Disambiguation: o preflight pergunta o modo ANTES de tarefa roteada — é curto, não é planejamento. Os modos ASK-MATT (qual skill, não qual modelo) e WAYFINDER (mapear bloco grande) vivem aqui dentro, não em skills separadas. WAYFINDER mapeia o bloco; fatiar o bloco em ondas para outro modelo executar é `plan-handoff`.

## Modos absorvidos (R3)

Modos inline desta skill. Os arquivos separados foram absorvidos aqui (`link-redirects.json`, 2026-08-31); nao ha o que carregar.

- **MODO ASK-MATT** — roteia trabalho de dev para a skill certa
- **MODO WAYFINDER** — mapeia bloco grande de trabalho antes de fatiar
