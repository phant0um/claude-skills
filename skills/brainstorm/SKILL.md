---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: brainstorm
skill: brainstorm
version: 1.0.0
trigger: ['/brainstorm [questão]', '@brainstorm [questão]', 'que opções existem']
effort: medium
tags: [reasoning, divergence, ideation, option-generation]
created: 2026-08-18
updated: 2026-10-25
owner: nexus
description: "Use when: /brainstorm [questão] · que opções existem · o espaço de solução parece ter só uma saída — gera opções deliberadamente divergentes antes de qualquer avaliação, com operadores de variação forçada e proibição de convergir. Entrega um leque; quem decide é council/debate."
consumes: []
reads: []
writes: []
tools: []
references:
  - "[council](../council/SKILL.md)"
  - "[council MODO DEBATE](../council/debate.md)"
  - "[prototype](../prototype/SKILL.md)"
verifier: ["≥8 opções geradas; ≥3 sobrevivem ao teste de distinção (premissa diferente, não redação diferente); nenhuma avaliação emitida antes da Fase 4; handoff nomeado."]
human_gate: false
triggers:
  positive:
    - "/brainstorm [questão]"
    - "que opções existem"
    - "só vejo uma saída, que alternativas existem?"
  negative:
    - "opções já definidas e prontas para avaliar"
    - "escolher entre opções já listadas"
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisao 2026-10-25: debate e heavy-think corrigidos para modos de council (nao sao skills); triggers alinhados (leading word, negativo sem auto-disparo); excecao de espaco estreito explicita; restricoes ausentes viram suposicao declarada (casa com evals.json caso 2). NAO conferido: skill-trigger-eval nao re-rodado apos a mudanca; reciprocidade council/office-hours -> brainstorm nao adicionada."
---
# Skill: Brainstorm

## Propósito

Gerar opções deliberadamente divergentes para uma questão aberta, **antes** de
qualquer avaliação. O produto é um leque de caminhos genuinamente distintos —
não uma recomendação.

O modo de falha que esta skill existe para impedir: gerar 3 variações da mesma
ideia, chamar de leque e escolher a do meio. Convergência precoce disfarçada de
opções.

---

## Quando NÃO usar

- **Brainstorm de escrita (fragmentos de artigo)** — `writing-fragments`.
- **Decidir entre opções que já existem** — `council` (5 lentes → veredicto) ou
  council MODO DEBATE (2 posições, árbitro). Brainstorm produz insumo pra eles, não substitui.
- **Pergunta com resposta verificável** — buscar a fonte. Divergir sobre fato é
  inventar.
- **Questão de execução (*como* fazer o que já está decidido)** — council MODO HEAVY-THINK
  resolve trajetórias; `prototype` responde pergunta de design construindo.
- **Espaço de solução genuinamente estreito** (uma API, um formato obrigatório) —
  forçar 8 opções ali produz ruído. Diga que é estreito e pare: este é o único resultado que dispensa o verifier (≥8 geradas, ≥3 sobreviventes).

Disambiguation: `brainstorm` **abre** o espaço · `council` **decide** dentro dele ·
council MODO DEBATE decide entre 2 · `pre-mortem` ataca um plano já escolhido ·
`connection-finder` minera links já existentes no vault, não gera novos caminhos ·
`prototype` constrói descartável pra responder uma pergunta de design específica.

---

## Entradas

- **Questão** (obrigatória) — reformulada na Fase 0, não aceita como veio.
- **Restrições duras** — o que é inegociável (orçamento, prazo, invariante).
- **Restrições assumidas** — o que *parece* fixo. A Fase 2 vai quebrar estas.

Sem restrições declaradas, assuma as mais prováveis, declare-as no topo do leque e siga. Brainstorm sem restrição gera
fantasia; brainstorm com restrição falsa gera timidez.

---

## Protocolo

### Fase 0 — Reformular a pergunta

Escreva a questão de 3 formas: mais estreita, mais ampla, e invertida
("como garantir que isso falhe?"). Se as três apontam para problemas diferentes,
**a pergunta é o problema** — resolva isso antes de gerar qualquer opção.

### Fase 1 — Descarga bruta

Gere **≥8 opções** rápidas, sem filtro, sem justificativa. Uma linha cada.
Inclua deliberadamente a opção óbvia e a opção "não fazer nada" — as duas são
baseline, não candidatas de honra.

Regra: nenhuma avaliação nesta fase. Nem "essa é boa". Avaliar cedo mata a cauda.

### Fase 2 — Variação forçada

A descarga bruta puxa do óbvio. Estes operadores puxam do resto. Aplique **pelo
menos 4**, gerando ≥1 opção nova por operador:

| Operador | Provocação |
|---|---|
| **Inverter** | E se fizéssemos o oposto exato? |
| **Remover** | Qual peça parece essencial? Tire ela. O que resta funciona? |
| **Extremar** | 10× maior. 10× menor. Grátis. Caro demais. |
| **Transplantar** | Como outro domínio resolve isso? (biologia, logística, jogos) |
| **Quebrar premissa** | Liste as restrições *assumidas*. Negue cada uma. |
| **Mudar de ator** | E se quem resolve não fosse você? Um novato? Um adversário? |
| **Deslocar no tempo** | Solução de 1990. Solução de 2040. |

### Fase 3 — Teste de distinção

Para cada par de opções: **elas diferem em premissa ou só em redação?**
Mesma premissa = uma opção só. Funda e siga.

Critério de done desta fase: **≥3 opções sobreviventes com premissas
incompatíveis entre si.** Se todas são compatíveis, você não divergiu — volte
à Fase 2 com operadores diferentes.

### Fase 4 — Mapear, não ranquear

Primeira fase em que avaliação é permitida — e ainda assim **não é escolha**.
Para cada sobrevivente, uma linha:

- **Aposta** — no que essa opção precisa acreditar pra funcionar
- **Custo de estar errado** — reversível ou não
- **Teste mais barato** — o que decidiria isso em menos tempo

### Fase 5 — Handoff

Nomeie explicitamente o próximo passo: `council` (múltiplas dimensões),
council MODO DEBATE (afunilou em 2), `prototype` (a dúvida é de design e um descartável
resolve), ou decisão direta (reversível e barata).

---

## Output

```
BRAINSTORM: [questão reformulada]

━━━ PERGUNTA ━━━
Como veio:    [original]
Reformulada:  [a que vamos usar]
Deslocamento: [o que mudou, ou "nenhum"]

━━━ LEQUE (n sobreviventes de N gerados) ━━━
1. [opção]  — premissa: [em que acredita]
2. [opção]  — premissa: [...]
3. [opção]  — premissa: [...]

━━━ FUNDIDAS ━━━
[par] → mesma premissa, redação diferente

━━━ MAPA ━━━
| Opção | Aposta | Custo se errado | Teste mais barato |

━━━ HANDOFF ━━━
→ [council | council-debate | prototype | decidir direto] porque [1 linha]
```

---

## Restrições

- **Nunca avaliar antes da Fase 4.** Julgamento precoce colapsa o leque; é o
  único jeito conhecido de esta skill falhar em silêncio.
- **Nunca entregar recomendação.** Brainstorm que recomenda virou council ruim.
- **Nunca contar variações de redação como opções** — Fase 3 existe pra isso.
- **Espaço estreito é resultado válido.** Dizer "só há 2 caminhos reais e aqui
  está por quê" vale mais que 8 opções infladas.
- Opção que viola restrição **dura** sai; que viola restrição **assumida** fica
  e é marcada — a premissa quebrada costuma ser o achado.

---

## Failure modes

| Sintoma | Causa | Correção |
|---|---|---|
| 8 opções, todas parecidas | pulou Fase 2 | aplicar 4 operadores de verdade |
| leque bom, mas nada acionável | pulou Fase 4 | mapear aposta e teste |
| virou recomendação | convergiu na Fase 1 | reiniciar da Fase 0 |
| tudo violou restrição dura | restrição não foi declarada | pedir restrições e refazer |

## Completion

- [ ] ≥8 geradas, ≥3 sobreviventes com premissas incompatíveis.
- [ ] Nenhuma avaliação antes da Fase 4.
- [ ] Handoff nomeado com razão.
