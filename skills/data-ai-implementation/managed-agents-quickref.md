---
origin: native
type: reference
status: active
kind: reference
resolver-status: not-exposed  # cheat-sheet de API (referencia, nao procedimento); entry=0 — D3 consolidacao 2026-09-25
name: managed-agents-quickref
skill: managed-agents-quickref
version: 1.0
author: Nexus Agent System
tags: [managed-agents, claude-api, reference, cheat-sheet, agent-systems]
updated: 2026-09-25
description: "Spec do MODO QUICKREF MANAGED AGENTS API de [data-ai-implementation](SKILL.md). Não é skill invocável. Consulta da Managed Agents API (managed-agents-2026-04-01, beta) — cheat-sheet dos 4 conceitos centrais, padrão de segurança, limites e onde achar cada peça. Referência de API; não é orquestração."
reads: []

parent: 04-SYSTEM/automation/skills/dev/data-ai-implementation/SKILL.md
mode: "QUICKREF MANAGED AGENTS API"
consolidated-by: orphan-audit-2026-10-05 (rebaixada a reference, sem gatilho)
reviewed-scope: "checagem mecanica + semantica: 19/19 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 14 secoes, 128 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- Propósito
- Quando NÃO usar
- Condições de Ativação
- Modelo mental — a cadeia em 1 linha
- Cheat-sheet por componente
- Limites documentados (tabela rápida)
- Padrão de segurança transversal: "definição vs. credencial"
- 3 vias de injeção de conteúdo (todas "montagem imutável por ID")
- Armadilhas de nomenclatura — não confundir
- Índice — as 14 fontes do lote 2026-06-06
- Completion
- Failure modes
- Restrições## Restrições
- Related

 Skill: Managed Agents Quickref

## Propósito
Cheat-sheet consolidado da **Managed Agents API** (`managed-agents-2026-04-01`, beta) — referência rápida para os 4 conceitos centrais, o padrão de segurança transversal, limites documentados e onde achar cada peça entre as 14 fontes ingeridas em 2026-06-06 (consolidadas em managed-agents-harness).

## Quando NÃO usar

- **Operação não-Managed-Agents** — cheat-sheet é da API managed-agents; para agentes locais, `04-SYSTEM/automation/registry/agent-registry.md` (agent-registry é doc, não skill).
- **Detalhe profundo de implementação** — quickref é referência rápida; profundidade vai para a API doc.

Disambiguation: `managed-agents-quickref` é cheat-sheet da Managed Agents API; `agent-registry` mapeia agentes do vault; `harness-audit` audita autoridade — quickref consulta, não audita.


## Condições de Ativação
Ative quando precisar de resposta rápida sobre:
- Como desenhar/configurar um agent, environment ou session via Managed Agents API
- Limites documentados (skills, memory stores, MCP, reautenticação)
- O fluxo Agent → Environment → Session → Events e onde cada peça injeta o quê
- Comparar Managed Agents vs. Messages API direta vs. Claude Code para a mesma funcionalidade (skills, MCP, memória)

NÃO ative para: dúvidas conceituais profundas (→ ler managed-agents-harness direto) ou implementação passo-a-passo (→ ler a fonte específica linkada abaixo).

---

## Modelo mental — a cadeia em 1 linha

**Agent** (blueprint reutilizável, sem segredo) → **Environment** (como provisionar o sandbox) → **Session** (instância rodando; aqui é onde identidade/credenciais/recursos são injetados) → **Events** (stream assíncrono — todo o resto se comunica por aqui).

## Cheat-sheet por componente

| Componente | O que é | Ponto-chave | Fonte |
|---|---|---|---|
| **Agent** | Blueprint versionado (model, system prompt, tools, MCP, skills) — compartilhável, sem segredo | Reutilizável entre N sessions | define-your-agent |
| **Environment** | Config de *como* provisionar o sandbox (pacotes, rede) | Tipo `cloud` = hospedado Anthropic; cria 1×, referencia por ID em N sessions | cloud-environment-setup |
| **Session** | Instância do agent rodando num environment | Ciclo: criar (provisiona) → enviar evento (inicia trabalho). Identidade/credenciais/recursos injetados SÓ AQUI — não pode anexar depois | start-a-session, session-operations |
| **Events** | Comunicação assíncrona via stream | Enviar/interromper/redirecionar/confirmar tool call/retomar/rastrear tokens | session-event-stream |
| **Outcomes** | "O que é pronto" — rubrica de qualidade + auto-avaliação + grader | Eleva session de "conversa" → "trabalho mensurável" | define-outcomes |
| **Multiagent** | Coordenador/roster, threads isolados, sandbox/credenciais compartilhados | Limite de skills é coletivo (ver tabela de limites) | multiagent-sessions |

## Limites documentados (tabela rápida)

| Limite | Valor | Nota |
|---|---|---|
| Skills por sessão | **20 total** | Contado coletivamente entre TODOS os agentes da sessão — não por agente |
| Memory stores por sessão | **8** | Controle `read_write` (default) ou `read_only` (filesystem-level) |
| Tamanho de memória / store | **100kB / memória, 2.000 memórias / store** | Reforça "many small focused files" |
| Reautenticação (AWS) | **6 horas** | Único delta operacional vs. pilha nativa em sessões autônomas |
| `instructions` por memory store | **4096 caracteres** | Orientação contextual mostrada ao agente junto de `name`/`description` |

## Padrão de segurança transversal: "definição vs. credencial"

Repetido em quase todas as 14 fontes — princípio único:
- Agent definitions NUNCA carregam segredo (portáveis, auditáveis).
- Sessions injetam identidade/tokens/recursos SÓ na criação — não depois.
- Recursos montados como **leitura imutável, referenciados por ID**, nunca ecoados de volta. Campos de segredo são *write-only*.
- Least-privilege como padrão: tokens com escopo mínimo, redes limitadas, vaults com refresh automático.

Mesmo princípio do Zero-Trust Framework em agent-security — aqui é a versão de produção em escala.

## 3 vias de injeção de conteúdo (todas "montagem imutável por ID")

1. **GitHub** — mount de repo + PRs via GitHub MCP → accessing-github
2. **Files API** — storage "create-once, use-many-times", referenciável por `file_id` → files-api
3. **Adding files** — monta arquivos da Files API no sandbox da session → adding-files

## Armadilhas de nomenclatura — não confundir

- `mcp-connector` (Messages API, beta `mcp-client`) **≠** `mcp-connector-1` (Managed Agents) — mesma funcionalidade, superfícies diferentes. Ver mcp-connector / mcp-connector-1.
- Limite de skills: Messages API = 8/requisição · Managed Agents = 20/sessão (coletivo) · Claude Code = sem hard limit documentado.
- "Skill" tem 3 mecanismos de anexação distintos por superfície: array `skills` (Managed Agents) / `container.skills` (Messages API) / `SKILL.md` em diretório (Claude Code).

## Índice — as 14 fontes do lote 2026-06-06

`claude-managed-agents-overview` (overview) · `define-your-agent` (Agent) · `define-outcomes` (Outcomes) · `start-a-session` + `session-operations` (Session) · `session-event-stream` (Events) · `multiagent-sessions` (coordenação) · `cloud-environment-setup` + `cloud-sandbox-reference` (Environment/sandbox) · `claude-platform-on-aws` (deploy) · `accessing-github` + `adding-files` + `files-api` (injeção de conteúdo) · `authenticate-with-vaults` (credenciais) · `skills` (Skills nesta superfície)

## Completion

- [ ] Resposta usa a tabela de componente correta (Agent/Environment/Session/Events)
- [ ] Limites citados correspondem à tabela documentada (20 skills, 8 memory stores, etc.)
- [ ] Distinção mcp-connector vs mcp-connector-1 respeitada (superfícies diferentes)
- [ ] Link para fonte específica fornecido para detalhe de implementação

## Failure modes

- **Surface confusion**: citar limite de Messages API (8 skills) em contexto de Managed Agents (20) → sempre confirmar superfície
- **Attach-after-creation**: sugerir anexar memory/vault a session em execução → só na criação
- **mcp-connector conflation**: tratar mcp-connector e mcp-connector-1 como sinônimos → são docs de superfícies diferentes

---

## Restrições## Restrições

- NUNCA tratar `mcp-connector` e `mcp-connector-1` como sinônimos — são docs de superfícies diferentes (risco de citar limite errado).
- NUNCA assumir que memory stores/vaults/arquivos podem ser anexados a uma session já em execução — só na criação.
- Para detalhe de implementação, sempre seguir o link da fonte específica — este cheat-sheet é ponto de entrada, não substitui a leitura completa.

## Related
- managed-agents-harness
- agent-security
- multi-agent-orchestration
