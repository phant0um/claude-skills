---
origin: native
kind: skill-proc
resolver-status: exposed
name: pre-mortem
skill: pre-mortem
version: 1.0
author: Nexus Agent System
source: Gary Klein (Harvard Business Review) + Kahneman endorsement

id: "pre-mortem"
title: "Skill: Pre-Mortem"
type: "skill"
created: "2026-06-19"
status: "active"
updated: "2026-07-29"
tags: ["reasoning", "risk", "decision-making", "parallel-agents", "pre-mortem"]
owner: "nexus"
description: "Use when: @premortem <plan> — prospective-hindsight APÓS o compromisso assumido: como o plano vai falhar? (não se deve fazer). Diferente de [office-hours](../office-hours/SKILL.md) (que questiona se a ideia merece investimento, fase de decisão); pre-mortem assume o compromisso e busca o modo de falha."
invocation: "both"
triggers:
  positive:
    - "@premortem <plan>"
    - "prospective-hindsight review for a costly commitment"
  negative:
    - "simple feedback"
    - "factual lookup"
    - "routine operational task"
route:
  profile: "deep"
  risk: "medium"
consumes: []
reads: ["plan", "assumptions", "constraints", "resource-commitment"]
writes: ["06-GENERATED/audits/*.md"]
tools: []
references: []
verifier: ["Require parallel failure analyses, plan-specific risks, concrete mitigations, and a concise summary."]
human_gate: false
reviewed-scope: "checagem mecanica + semantica: 3/3 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 9 secoes, 153 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---


# Skill: Pre-Mortem

## Propósito
Avaliar planos de alto risco usando prospective hindsight: "este plano já falhou — explique como morreu." O framing "já falhou" quebra o viés otimista do Claude e produz razões mais específicas e honestas que "o que poderia dar errado?".

---

## Quando NÃO usar

- **Decisão trivial reversível** — pre-mortem custa mais que o risco.
- **Plano já em execução sem checkpoint** — pre-mortem é prospective (antes), não retrospectivo.
- **Sem plano escrito** — pre-mortem sobre ideia vaga vira brainstorm; escrever o plano antes.

Disambiguation: `pre-mortem` antecipa falhas de um plano (prospective hindsight); `drift-review` detecta desvio entre docs e código; `contradiction-sweep` varre contradições no vault — pre-mortem é sobre o futuro, não o presente.


## Condições de Ativação
Ative esta skill quando:
- Decisão irreversível ou de alto custo de erro (investimento, concurso strategy, MVP launch)
- Usuário solicitar `@premortem [plano]` ou "que poderia matar isso?"
- Antes de comprometer recursos significativos (tempo >1 semana, dinheiro >R$1000)

NÃO ative para: feedback simples; perguntas factuais; decisões já tomadas e irreversíveis; tarefas operacionais de rotina.

---

## Perfil de modelo

Perfil `deep` — prospective hindsight: gerar modos de falha especificos e criativos e o produto,
e `route.profile: deep` ja estava declarado no frontmatter
(model-routing §Padrao custo-efetivo; model-catalog §Perfis).
Esta skill nao mantem pins locais por etapa.

## Protocolo de Execução

### PASSO 1 — Coleta de Contexto
Buscar em CLAUDE.md, memory/, arquivos do projeto. Extrair: o que é, para quem, como é sucesso.

### PASSO 2 — Avalia Suficiência
Precisa de 3 elementos mínimos:
- O que é o plano (ação concreta)
- Para quem é (audiência/mercado)
- Como é sucesso (métrica ou resultado)

Se faltar: máx 1 pergunta por vez. Não fazer entrevista.

### PASSO 3 — Premortem Bruto
Instrução para o modelo:
```
Estamos 6 meses no futuro. Este plano falhou completamente.
Sua tarefa: liste TODAS as razões plausíveis de falha.
Seja específico ao plano — sem riscos genéricos.
Número de falhas = o que o plano merece (quantas houver; tipicamente 3 a 8).
Para cada: nome curto + 1 frase descritiva.
```

### PASSO 4 — Sub-Agentes Paralelos
Spawnar 1 sub-agente por razão de falha. **Todos em paralelo — sequencial contamina.**

Cada sub-agente recebe:
```
Você é analista de risco. Um plano falhou por esta razão: [RAZÃO].
Produza:
1. História da falha (3-5 frases narrativas — como aconteceu, passo a passo)
2. Suposto subjacente que o planejador não questionou
3. 2-3 sinais de alerta precoce (o que teria sido visível antes da falha), cada um com: como acompanhar e a ação preventiva
```

### PASSO 5 — Síntese
Integrar todos os modos de falha e produzir:
1. **Falha mais provável** — maior probabilidade (só com base declarada; sem base, diga "não estimável")
2. **Falha mais perigosa** — maior impacto se ocorrer
3. **Suposto oculto** — o que o planejador assumiu sem perceber
4. **Plano revisado** — 3-5 ajustes concretos ao plano original
5. **Checklist pré-lançamento** — 3-5 verificações antes de comprometer
6. **Gatilhos** — por falha: sinal observável · como acompanhar · condição para revisar, parar ou reverter · ação

---

## Artefatos de Saída
- Resumo no chat: máx 3 frases (falha mais provável + suposto oculto + revisão mais importante)
- `premortem-report-[timestamp].md` — relatório completo (se solicitado)

---

## Completion

- [ ] 1 sub-agente por falha do PASSO 3, todos em paralelo (cada um com framing "já falhou")
- [ ] 4 outputs entregues: falha mais provável (ou "não estimável", sem base), mais perigosa, suposto oculto, plano revisado (3-5 ajustes)
- [ ] Checklist pré-lançamento com 3-5 verificações concretas
- [ ] Gatilhos por falha: sinal observável, como acompanhar, condição para revisar/parar/reverter, ação
- [ ] Resumo no chat: máx 3 frases (falha provável + suposto oculto + revisão principal)
- [ ] Riscos específicos ao plano (não genéricos)

## Failure modes

- **Cortês com o plano**: suggestions suavizadas → framing "já falhou" é o mecanismo crítico
- **Sequential sub-agents**: lançar os sub-agentes em sequência → paralelo obrigatório, sequencial contamina
- **Generic risks**: "pode falhar por falta de mercado" → sempre específico ao plano concreto
- **Force-count**: forçar 7 falhas quando há 3 reais → quantidade segue qualidade, não quota

---

## Restrições
- NUNCA ser cortês com o plano — o framing "já falhou" é o mecanismo psicológico crítico
- NUNCA lançar sub-agentes em sequência — paralelo obrigatório (sequencial contamina)
- NUNCA forçar 7 falhas se há 3, nem parar em 3 se há 7
- NUNCA usar riscos genéricos ("pode falhar por falta de mercado") — sempre específico ao plano
- Diferente de risk assessment: premortem vai ao futuro onde falhou, não avalia probabilidades no presente
