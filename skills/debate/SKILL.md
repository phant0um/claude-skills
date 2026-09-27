---
name: debate
description: "Spec do MODO DEBATE (2 lados) de `council`. Não é skill invocável. @debate [questão] — Deliberação formal entre duas perspectivas opostas para decisões arquiteturais ou de design onde a resposta certa não é óbvia. Produz confronto estruturado + arbitragem — não síntese suave."
trigger: "@debate [questão]" | "/debate [questão]" | "debate this" | "A vs B?" | "faz um debate sobre"
---
> **Não é skill invocável.** MODO DEBATE (2 lados) de `council` — carregado por ela, não resolvido pelo router.




# Skill: Debate

## Propósito

Deliberação formal entre duas perspectivas opostas para decisões arquiteturais ou de design onde a resposta certa não é óbvia. Produz confronto estruturado + arbitragem — não síntese suave.

**Diferença de heavy-think:**
- `heavy-think` = múltiplas trajetórias paralelas sobre *como* resolver um problema bem definido
- `debate` = duas posições opostas sobre *qual* escolha tomar quando há trade-off real

Usar `debate` quando a questão for "A vs B?" — usar `heavy-think` quando for "como resolver X?".

---

## Condições de Ativação

Ative quando:
- Decisão arquitetural com trade-off real (não preferência óbvia)
- Usuário indeciso entre dois designs/abordagens
- Agente propõe mudança significativa e você quer confronto antes de aceitar
- `@debate [questão com vs / ou]`

NÃO ative para: questões factuais verificáveis; tarefas de implementação; decisões já tomadas e irreversíveis; preferências estéticas sem impacto arquitetural.

---

## Perfil de modelo

Herda o perfil de `council`. Mode spec nao declara perfil proprio:
e carregado por council e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## Protocolo

### 1. Extrair Questão

Da input do usuário, extrair:
- **Questão central:** "A vs B?" em uma frase
- **Contexto:** o que motivou essa decisão agora
- **Restrições ativas:** princípios do projeto, recursos, prazo
- **Critério de sucesso:** o que "melhor escolha" significa aqui

Se a questão for ambígua: reformular como "Perspectiva A: [posição] / Perspectiva B: [posição oposta]" e confirmar com usuário antes de continuar.

### 2. Perspectiva A

Instrução:
```
Você defende a Perspectiva A: [posição].
Contexto: [contexto extraído]
Restrições: [restrições ativas]

Sua tarefa:
1. Argumento principal (1 parágrafo — por que A é superior a B nesse contexto)
2. Evidência concreta (exemplos, dados, precedentes no próprio projeto)
3. Fraqueza reconhecida de A (1 frase — onde B tem vantagem real)
4. Por que essa fraqueza não é decisiva (1 frase)

NÃO seja suave. NÃO conceda além do mínimo. Ganhe o argumento.
```

### 3. Perspectiva B

Mesma estrutura, posição oposta. Executar em paralelo com Perspectiva A.

### 4. Arbitragem

Instrução:
```
Você recebe dois argumentos opostos sobre a mesma decisão.
Contexto: [contexto]
Restrições: [restrições]

Perspectiva A: [output do Passo 2]
Perspectiva B: [output do Passo 3]

Sua tarefa:
1. Identifique o argumento mais forte de cada perspectiva
2. Identifique o ponto cego de cada perspectiva
3. Verifique: há premissas falsas em alguma das perspectivas?
4. Emita veredicto: qual perspectiva vence neste contexto específico?
5. Condição de revisão: em que circunstância o veredicto mudaria?

PROIBIDO: veredicto "depende" sem especificar o que depende.
PROIBIDO: recomendar "um meio-termo" sem justificar que é superior a ambas.
```

### 5. Output

Formato final para o usuário:

```
DEBATE: [Questão]

─── PERSPECTIVA A: [posição] ───
[argumento, evidência, fraqueza reconhecida]

─── PERSPECTIVA B: [posição] ───
[argumento, evidência, fraqueza reconhecida]

─── ÁRBITRO ───
Argumento mais forte de A: [...]
Argumento mais forte de B: [...]
Ponto cego de A: [...]
Ponto cego de B: [...]

VEREDICTO: [A/B] — porque [razão específica ao contexto]
Condição de revisão: [quando mudar de ideia]
```

---

## Completion

- [ ] Perspectivas A e B executadas em paralelo (não sequência)
- [ ] Árbitro emite veredito com vencedor (não "depende" sem condição)
- [ ] Se ambas concordam: reportado como não-debate, encaminhar para heavy-think
- [ ] Output: decisão + razão + condição de reversão

## Failure modes

- **Sequential execution**: rodar A depois B → paralelo obrigatório, sequencial contamina
- **"Depende" sem condição**: árbitro emite "depende" sem especificar quando A vs B → deve especificar condição
- **Default middle-ground**: recomendar meio-termo como saída padrão → debate tem vencedor
- **Non-debate**: ambas perspectivas concordam → não há debate real, usar heavy-think

---

## Restrições## Restrições

- NUNCA executar Perspectivas A e B em sequência — paralelo obrigatório (sequencial contamina)
- NUNCA deixar o árbitro emitir "depende" sem especificar a condição
- NUNCA recomendar meio-termo como saída padrão — debate tem vencedor
- Se ambas as perspectivas concordarem no fundo: não há debate real — reportar e usar heavy-think

---

## Relacionado

- heavy-think — multi-trajetória para resolver um problema (não escolher entre opções)
- `pre-mortem` — analisa riscos de falha de um plano já escolhido
- guard — usa adversarial mode similar (attacker + defender + auditor)

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
