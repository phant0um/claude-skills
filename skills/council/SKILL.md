---
name: council
description: 5 advisors com perspectivas hard-wired debatem uma questão, revisam uns aos outros de forma cega, e entregam veredicto estruturado num único contexto. Use para decisões estratégicas multi-dimensionais onde blind spots são esperados.
trigger: "council this" | "@council [questão]" | "/council [questão]" | "convoca o council" | "run a council on this"
version: 1.0
model: claude-opus-4-8
effort: high
tags: [reasoning, decision-making, multi-perspective, peer-review, deliberation]
---

# Skill: Council

## Propósito

5 advisors com perspectivas hard-wired debatem uma questão, revisam uns aos outros de forma cega, e entregam veredicto estruturado. Substitui coordenação de múltiplos modelos por prompt engineering sofisticado em um único contexto.

**Diferença de `debate`:** debate = 2 posições opostas (A vs B), árbitro decide (ver skill `debate`). Council = 5 lentes distintas cobrindo sistematicamente risco + problema real + upside oculto + praticidade + ação concreta — sem posições predefinidas.

**Council vs. exploração de trajetórias:** explorar múltiplas trajetórias de raciocínio resolve *como*. Council usa 5 perspectivas humanas para decidir *o quê/se*.

---

## Condições de Ativação

Ative quando:
- Decisão estratégica com múltiplas dimensões (não apenas A vs B)
- Usuário diz "council this" antes de qualquer questão
- Spec arquitetural complexa antes de comprometer recursos
- Decisão onde blind spots são esperados

NÃO ative para: implementações concretas; questões técnicas verificáveis; A vs B claro (→ ver skill `debate`).

---

## Modelo por Etapa

Para reduzir custo, use um modelo mais barato para as etapas divergentes (extração e advisors) e reserve o modelo mais forte para a síntese final.

| Etapa | Modelo | Razão |
|-------|--------|-------|
| Extração de contexto | barato/rápido | Parsing estruturado |
| 5 advisors (em paralelo) | intermediário × 5 | Perspectiva + evidência por advisor |
| Blind peer review | intermediário | Revisão cruzada sem viés de posição |
| Veredicto final | mais forte | Síntese de alta complexidade |

---

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

---

## Exemplo

**Input:** "council this — devo largar meu emprego CLT para tocar meu SaaS solo em tempo integral? Tenho 8 meses de reserva e ~R$2k MRR."

**Output (resumido):**
```
COUNCIL: Largar CLT para SaaS solo full-time agora?

━━━ ADVISORS ━━━
Risk:      8 meses de runway some rápido se o MRR estagnar; sem colchão de renda.
Problem:   O gargalo não é tempo, é canal de aquisição — mais horas não resolvem distribuição.
Upside:    Full-time pode destravar parcerias e vendas outbound impossíveis no part-time.
Pragmatics:Testar 3 meses reduzindo para 20h CLT antes do salto de tudo-ou-nada.
Action:    Não largaria ainda; validaria 1 canal repetível de aquisição primeiro.

━━━ PEER REVIEW ━━━
Resposta mais forte: Problem — todos assumiram que tempo é a restrição; é distribuição.
Maior blind spot individual: Upside ignorou que outbound exige skill que você ainda não tem.
O que todos perderam: nenhum quantificou qual MRR tornaria o salto reversível-seguro.

━━━ VEREDICTO ━━━
Recomendação: Não largar agora. Definir gatilho: largar quando MRR cobrir 60% do custo de vida por 2 meses seguidos.
Blind spot coletivo: ninguém definiu o número que transforma a aposta em decisão racional.
Tensão central: foco total acelera aprendizado vs. runway curto pune erros de distribuição.
Próximo passo: esta semana, escolher e rodar 1 canal de aquisição medível.
Condição de revisão: reavaliar quando MRR dobrar ou a reserva cair abaixo de 5 meses.
```

---

## Completion

- [ ] 5 advisors executados em paralelo (não sequência)
- [ ] Shuffle + anonimização aplicados no peer review
- [ ] Veredito sintetizado com contribuição de cada lente
- [ ] Se questão tem resposta técnica verificável: não usado

## Failure modes

- **Sequential advisors**: rodar 5 advisors em sequência → paralelo obrigatório, sequencial contamina
- **Skip anonymization**: pular shuffle + anonimização → viés de posição invalida peer review
- **Weak model for advisors**: usar modelo fraco para perspectivas → perspectivas requerem raciocínio real
- **Verifiable answer**: usar council para questão com resposta técnica → não é o caso de uso

---

## Restrições

- NUNCA executar advisors em sequência — paralelo obrigatório (sequencial contamina perspectivas)
- NUNCA pular o shuffle + anonimização no peer review — viés de posição invalida a revisão cruzada
- NUNCA usar um modelo fraco demais para advisors — perspectivas requerem raciocínio real
- Se a questão tiver resposta técnica verificável: não usar council

---

## Relacionado

- Skill `debate` — 2 perspectivas opostas; council = 5 lentes não-opostas
- Skill `pre-mortem` — analisa riscos de um plano já escolhido; council escolhe qual plano adotar

---

## Mecanismos anti-groupthink

Endurecem a deliberação contra groupthink e perguntas mal-formuladas:

- **Problem-Restate Gate:** antes de qualquer análise, cada perspectiva reformula a pergunta. Se as reformulações divergem, a pergunta É o problema — resolver isso primeiro.
- **Dissent quota / novelty gate:** se >70% concordam cedo, forçar 2 perspectivas a fazer steelman da posição oposta. Sem dissenso genuíno, sem veredito.
- **Verdict lidera com incerteza:** veredito abre com "Perguntas Não-Resolvidas" + "Próximos Passos", não com consenso confiante. O que não se sabe importa mais que onde concordam.
- **Multi-modelo (opcional):** rodar os advisors num modelo mais barato e reservar o modelo mais forte para a síntese reduz custo e diversifica o raciocínio.

---

*Adaptado do padrão Claude Council (5-advisor).*
