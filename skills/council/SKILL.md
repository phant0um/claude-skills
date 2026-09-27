---
name: council
trigger: ['council this', '@council [questão]', '/council [questão]']
description: "Use when: council this — 5 advisors com perspectivas hard-wired debatem uma questão, revisam uns aos outros de forma cega, e entregam veredicto estruturado. Substitui coordenação de múltiplos modelos por prompt engineering sofisticado em um único contexto."
---
# Skill: Council

## Propósito

5 advisors com perspectivas hard-wired debatem uma questão, revisam uns aos outros de forma cega, e entregam veredicto estruturado. Substitui coordenação de múltiplos modelos por prompt engineering sofisticado em um único contexto.

**Diferença de `/debate`:** debate = 2 posições opostas (A vs B), árbitro decide. Council = 5 lentes distintas cobrindo sistematicamente risco + problema real + upside oculto + praticidade + ação concreta — sem posições predefinidas.

**Diferença de `heavy-think`:** heavy-think = múltiplas trajetórias de raciocínio para resolver *como*. Council = 5 perspectivas humanas para decidir *o quê/se*.

---

## Quando NÃO usar

- **Decisão binária simples** (A vs B com critério objetivo) — `debate` (2 posições) ou decisão direta custam menos.
- **Questão de execução (*como*)** — `heavy-think` resolve trajetórias de raciocínio; council decide o quê/se.
- **Pressa com custo alto** — 5 advisors custam tokens; para decisão reversível de baixo risco, decidir direto.
- **Fato verificável** — council não resolve fato; buscar a fonte.

Disambiguation: `debate` = 2 posições opostas, árbitro decide; `council` = 5 lentes cobrindo risco/problema/upside/praticidade/ação; `heavy-think` = múltiplas trajetórias para resolver como; `reason-judge` pontua output por rubrica, não delibera decisão.


## Condições de Ativação

Ative quando:
- Decisão estratégica com múltiplas dimensões (não apenas A vs B)
- Usuário diz "council this" antes de qualquer questão
- Spec arquitetural complexa antes de escalar para Opus
- Decisão de produto/arquitetura onde blind spots são esperados

NÃO ative para: implementações concretas (→ spec/extend); questões técnicas verificáveis (→ heavy-think); segurança (→ guard); A vs B claro (→ debate).

---

## Perfil de modelo

Perfil `deep` — 5 perspectivas hard-wired em contradicao deliberada, com peer review cego:
sintese de desacordo e auditoria semantica
(model-routing §Padrao custo-efetivo; model-catalog §Perfis).
Esta skill nao mantem pins locais por etapa.

## Protocolo

### Fase 1 — Contexto

Extrair da input:
- **Questão central** (1 frase)
- **Contexto relevante** (o que motivou, restrições ativas, histórico)
- **O que "boa decisão" significa** (critério de sucesso)

### Fase 2 — 5 Advisors em paralelo

Cada advisor responde com sua perspectiva exclusiva. **Executar em paralelo — sequencial contamina.**

| Advisor | Lente | Pergunta guia |
|---------|-------|--------------|
| **A — Risk** | O que pode falhar? | Quais os 3 modos de falha mais prováveis? O que não estamos vendo? |
| **B — Problem** | Qual o problema real? | Estamos resolvendo o problema certo? Qual problema subjacente estamos ignorando? |
| **C — Upside** | Qual upside estamos perdendo? | Qual oportunidade não óbvia está aqui? O que a decisão conservadora sacrifica? |
| **D — Pragmatics** | O que faz sentido segunda de manhã? | Que constrangimentos reais (tempo, energia, complexidade) este plano ignora? |
| **E — Action** | O que você realmente faria? | Se fosse sua decisão pessoal, com suas consequências: o que faria agora? |

Instrução para cada advisor:
```
Você é o Advisor [X] do Council.
Questão: [questão]
Contexto: [contexto]

Responda exclusivamente da sua perspectiva ([lente]).
Formato:
1. Resposta principal (2-4 parágrafos)
2. Blind spot mais importante da questão (1 parágrafo)
3. Recomendação concreta (1 frase de ação)

NÃO seja diplomático. Diga o que você vê.
```

### Fase 3 — Blind Peer Review

1. Coletar todas as 5 respostas
2. **Anonimizar + shuffle** (chamar de "Advisor Alpha/Beta/Gamma/Delta/Epsilon" em ordem aleatória)
3. Cada advisor recebe as 5 respostas anonimizadas e responde:
   - "Qual resposta é mais forte e por quê?"
   - "Qual tem o maior blind spot?"
   - "O que todos os 5 perderam?"

Executar os 5 peer reviews em paralelo.

### Fase 4 — Veredicto Final

Instrução:
```
Você recebe 5 perspectivas sobre uma questão + 5 peer reviews cruzados.
Questão: [questão]
Critério de sucesso: [critério]

SUA TAREFA:
1. Melhor recomendação — qual ação tomar e por quê
2. Maior blind spot coletivo — o que todos os 5 perderam
3. Tensão central — qual é o trade-off irresolvível nessa decisão
4. Próximo passo concreto — 1 ação específica para amanhã
5. Condição de revisão — quando reconsiderar este veredicto

PROIBIDO: veredicto vago. Cada item deve ser específico ao contexto dado.
```

### Fase 5 — Output

```
COUNCIL: [Questão]

━━━ ADVISORS ━━━
Risk:      [resumo 1 linha]
Problem:   [resumo 1 linha]
Upside:    [resumo 1 linha]
Pragmatics:[resumo 1 linha]
Action:    [resumo 1 linha]

━━━ PEER REVIEW ━━━
Resposta mais forte: [qual e por quê — 1 linha]
Maior blind spot individual: [qual e por quê — 1 linha]
O que todos perderam: [1-2 linhas]

━━━ VEREDICTO ━━━
Recomendação: [ação concreta]
Blind spot coletivo: [o que ninguém viu]
Tensão central: [trade-off irresolvível]
Próximo passo: [1 ação específica]
Condição de revisão: [quando mudar de ideia]
```

**Veredito que é decisão arquitetural** (escolhe estrutura, contrato, stack ou
política do sistema): o `Próximo passo` é registrar a decisão →
decisions, com a recomendação, a tensão
central como trade-off e a condição de revisão como gatilho de reabertura. Fora
disso, o veredito fecha no próprio output.

---

## Completion

- [ ] 5 advisors executados em paralelo (não sequência)
- [ ] Shuffle + anonimização aplicados no peer review
- [ ] Veredito sintetizado com contribuição de cada lente
- [ ] Veredito arquitetural: `Próximo passo` aponta para `decisions`
- [ ] Se questão tem resposta técnica verificável: não usado (usar heavy-think)

## Failure modes

- **Sequential advisors**: rodar 5 advisors em sequência → paralelo obrigatório, sequencial contamina
- **Skip anonymization**: pular shuffle + anonimização → viés de posição invalida peer review
- **Haiku for advisors**: usar Haiku para perspectivas → perspectivas requerem raciocínio real (Sonnet+)
- **Verifiable answer**: usar council para questão com resposta técnica → usar heavy-think

---

## Restrições

- NUNCA executar advisors em sequência — paralelo obrigatório (sequencial contamina perspectivas)
- NUNCA pular o shuffle + anonimização no peer review — viés de posição invalida a revisão cruzada
- NUNCA usar Haiku para advisors — perspectivas requerem raciocínio real
- Se a questão tiver resposta técnica verificável: não usar council, usar heavy-think

---

## Relacionado

- `debate` — 2 perspectivas opostas; council = 5 lentes não-opostas
- heavy-think — múltiplas trajetórias de solução; council = perspectivas humanas de decisão
- `pre-mortem` — analisa riscos de plano já escolhido; council escolhe qual plano adotar

---

## Mecanismos importados (council-of-high-intelligence)

Endurecem a deliberação contra groupthink e perguntas mal-formuladas:

- **Problem-Restate Gate:** antes de qualquer análise, cada perspectiva reformula
  a pergunta. Se as reformulações divergem, a pergunta É o problema — resolver isso primeiro.
- **Dissent quota / novelty gate:** se >70% concordam cedo, forçar 2 perspectivas a
  fazer steelman da posição oposta. Sem dissenso genuíno, sem veredito.
- **Verdict lidera com incerteza:** veredito abre com "Perguntas Não-Resolvidas" +
  "Próximos Passos", não com consenso confiante. O que não se sabe importa mais que onde concordam.
- **Multi-provider (opcional):** membros baratos via Ollama (model-router), síntese via Claude.
  Reduz custo e diversifica raciocínio. Ref: model-router.


## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO DEBATE (2 lados)** — `debate`
- **MODO HEAVY-THINK (1 perspectiva, profundidade)** — heavy-think
