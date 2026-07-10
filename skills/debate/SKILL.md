---
name: debate
description: Deliberação formal entre duas perspectivas opostas para decisões arquiteturais ou de design com trade-off real. Produz confronto estruturado + arbitragem com veredicto, não síntese suave.
trigger: "@debate [questão]" | "/debate [questão]" | "debate this" | "A vs B?" | "faz um debate sobre"
version: 1.0
model: claude-opus-4-8
effort: high
tags: [reasoning, deliberation, architecture, decisions, two-perspective]
---

# Skill: Debate

## Propósito

Deliberação formal entre duas perspectivas opostas para decisões arquiteturais ou de design onde a resposta certa não é óbvia. Produz confronto estruturado + arbitragem — não síntese suave.

**Quando usar debate vs. explorar trajetórias:**
- Explorar múltiplas trajetórias paralelas serve para descobrir *como* resolver um problema bem definido.
- `debate` = duas posições opostas sobre *qual* escolha tomar quando há trade-off real.

Usar `debate` quando a questão for "A vs B?". Para "como resolver X?", prefira uma exploração de múltiplas abordagens.

---

## Condições de Ativação

Ative quando:
- Decisão arquitetural com trade-off real (não preferência óbvia)
- Usuário indeciso entre dois designs/abordagens
- Uma mudança significativa foi proposta e você quer confronto antes de aceitar
- `@debate [questão com vs / ou]`

NÃO ative para: questões factuais verificáveis; tarefas de implementação; decisões já tomadas e irreversíveis; preferências estéticas sem impacto arquitetural.

---

## Modelo por Etapa

Para reduzir custo, use um modelo mais barato nas etapas divergentes (extração e as duas perspectivas) e reserve o modelo mais forte para a arbitragem.

| Etapa | Modelo | Razão |
|-------|--------|-------|
| Extração da questão e contexto | barato/rápido | Parsing estruturado |
| Perspectiva A | intermediário | Argumentação com evidência |
| Perspectiva B | intermediário | Argumentação com evidência |
| Arbitragem | mais forte | Julgamento integrado de trade-offs |

---

## Protocolo

### 1. Extrair Questão

Da input do usuário, extrair:
- **Questão central:** "A vs B?" em uma frase
- **Contexto:** o que motivou essa decisão agora
- **Restrições ativas:** princípios do projeto, recursos, prazo
- **Critério de sucesso:** o que "melhor escolha" significa aqui

Se a questão for ambígua: reformular como "Perspectiva A: [posição] / Perspectiva B: [posição oposta]" e confirmar com usuário antes de continuar.

### 2. Perspectiva A *(sem ver Perspectiva B)*

Instrução:
```
Você defende a Perspectiva A: [posição].
Contexto: [contexto extraído]
Restrições: [restrições ativas]

Sua tarefa:
1. Argumento principal (1 parágrafo — por que A é superior a B nesse contexto)
2. Evidência concreta (exemplos, dados, precedentes relevantes)
3. Fraqueza reconhecida de A (1 frase — onde B tem vantagem real)
4. Por que essa fraqueza não é decisiva (1 frase)

NÃO seja suave. NÃO conceda além do mínimo. Ganhe o argumento.
```

### 3. Perspectiva B *(sem ver Perspectiva A)*

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

## Exemplo

**Input:** "@debate REST vs GraphQL para a API do nosso app mobile — time pequeno, backend Node, mudanças frequentes de tela."

**Output (resumido):**
```
DEBATE: REST vs GraphQL para a API mobile

─── PERSPECTIVA A: REST ───
Simplicidade operacional: cache HTTP nativo, menos tooling, curva rasa para time pequeno.
Fraqueza: over/under-fetching força versões de endpoint por tela.

─── PERSPECTIVA B: GraphQL ───
Cliente pede exatamente os campos que a tela precisa; telas mudam sem tocar o backend.
Fraqueza: complexidade de cache e risco de queries N+1 sem dataloader.

─── ÁRBITRO ───
Argumento mais forte de A: menor custo operacional para 1-2 devs.
Argumento mais forte de B: desacopla evolução de UI da API — casa com "mudanças frequentes de tela".
Ponto cego de A: subestima o custo recorrente de versionar endpoints por tela.
Ponto cego de B: ignora que caching e monitoring de GraphQL pesam num time pequeno.

VEREDICTO: GraphQL — porque a restrição dominante declarada é churn de telas, e é aí que REST cobra imposto contínuo.
Condição de revisão: mudar para REST se as telas estabilizarem ou se o time não absorver o tooling de cache em 1 sprint.
```

---

## Completion

- [ ] Perspectivas A e B executadas em paralelo (não sequência)
- [ ] Árbitro emite veredito com vencedor (não "depende" sem condição)
- [ ] Se ambas concordam: reportado como não-debate
- [ ] Output: decisão + razão + condição de reversão

## Failure modes

- **Sequential execution**: rodar A depois B → paralelo obrigatório, sequencial contamina
- **"Depende" sem condição**: árbitro emite "depende" sem especificar quando A vs B → deve especificar condição
- **Default middle-ground**: recomendar meio-termo como saída padrão → debate tem vencedor
- **Non-debate**: ambas perspectivas concordam → não há debate real

---

## Restrições

- NUNCA executar Perspectivas A e B em sequência — paralelo obrigatório (sequencial contamina)
- NUNCA deixar o árbitro emitir "depende" sem especificar a condição
- NUNCA recomendar meio-termo como saída padrão — debate tem vencedor
- Se ambas as perspectivas concordarem no fundo: não há debate real — reportar

---

## Relacionado

- Skill `council` — 5 lentes não-opostas; debate = 2 perspectivas opostas
- Skill `pre-mortem` — analisa riscos de falha de um plano já escolhido

---

## Mecanismos anti-groupthink

Endurecem a deliberação contra groupthink e perguntas mal-formuladas:

- **Problem-Restate Gate:** antes de qualquer análise, cada perspectiva reformula a pergunta. Se as reformulações divergem, a pergunta É o problema — resolver isso primeiro.
- **Dissent quota / novelty gate:** se as perspectivas convergem cedo, forçar cada uma a fazer steelman da posição oposta. Sem dissenso genuíno, sem veredito.
- **Verdict lidera com incerteza:** veredito abre com "Perguntas Não-Resolvidas" + "Próximos Passos", não com consenso confiante.
- **Multi-modelo (opcional):** rodar as duas perspectivas num modelo mais barato e reservar o modelo mais forte para a arbitragem reduz custo e diversifica o raciocínio.
