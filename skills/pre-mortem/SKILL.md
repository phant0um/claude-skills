---
name: pre-mortem
description: Avalia planos de alto risco usando prospective hindsight — "este plano já falhou, explique como morreu." O framing quebra o viés otimista e produz razões de falha específicas e acionáveis.
trigger: "@premortem [plano]" | "/premortem [plano]" | "que poderia matar isso?" | "pre-mortem this" | "how could this fail?"
version: 1.0
source: Gary Klein (Harvard Business Review) + endosso de Kahneman
tags: [reasoning, risk, decision-making, parallel-agents, pre-mortem]
---

# Skill: Pre-Mortem

## Propósito
Avaliar planos de alto risco usando prospective hindsight: "este plano já falhou — explique como morreu." O framing "já falhou" quebra o viés otimista e produz razões mais específicas e honestas que "o que poderia dar errado?".

---

## Condições de Ativação
Ative esta skill quando:
- Decisão irreversível ou de alto custo de erro (investimento, lançamento de MVP, mudança de carreira)
- Usuário solicitar `@premortem [plano]` ou "que poderia matar isso?"
- Antes de comprometer recursos significativos (tempo, dinheiro, reputação)

NÃO ative para: feedback simples; perguntas factuais; decisões já tomadas e irreversíveis; tarefas operacionais de rotina.

---

## Modelo por Etapa

Para reduzir custo, use um modelo mais barato nas etapas mecânicas e divergentes e reserve o modelo mais forte para a síntese de risco.

| Etapa | Modelo | Justificativa |
|-------|--------|---------------|
| Coleta de contexto | barato/rápido | Busca em arquivos e memória do projeto |
| Avalia suficiência de contexto | barato/rápido | Checklist mecânico |
| Premortem bruto (lista de falhas) | intermediário | Requer criatividade + especificidade |
| Sub-agentes por modo de falha | intermediário | Paralelo, independente |
| Síntese final | mais forte | Julgamento de risco integrado |

---

## Protocolo de Execução

### PASSO 1 — Coleta de Contexto
Buscar em documentos e notas relevantes do projeto. Extrair: o que é, para quem, como é sucesso.

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
Número de falhas = o que o plano merece (3 a 8).
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
3. 2-3 sinais de alerta precoce (o que teria sido visível antes da falha)
```

### PASSO 5 — Síntese
Integrar todos os modos de falha e produzir:
1. **Falha mais provável** — maior probabilidade
2. **Falha mais perigosa** — maior impacto se ocorrer
3. **Suposto oculto** — o que o planejador assumiu sem perceber
4. **Plano revisado** — 3-5 ajustes concretos ao plano original
5. **Checklist pré-lançamento** — 3-5 verificações antes de comprometer

---

## Exemplo

**Input:** "@premortem vou lançar um curso online de Python em 6 semanas, gravando à noite depois do trabalho, e vender para minha lista de 500 emails."

**Output (resumido):**
```
PRE-MORTEM: Curso de Python em 6 semanas

Falha mais provável: burnout de gravação — 6 semanas noturnas colidem com semanas
de trabalho pesado; gravação para, prazo estoura, momentum morre.

Falha mais perigosa: lista de 500 emails converte a 1% → 5 vendas; receita não paga
o esforço e desmotiva o próximo lançamento.

Suposto oculto: que a lista está "quente" e quer justamente este curso — nunca foi
validado com uma enquete ou pré-venda.

Plano revisado:
1. Pré-vender antes de gravar (validar demanda + criar compromisso).
2. Gravar módulo 1 completo antes de anunciar data — reduz risco de prazo.
3. Reservar 2 semanas de buffer no cronograma noturno.
4. Segmentar a lista e medir interesse antes de comprometer 6 semanas.

Checklist pré-lançamento:
[ ] Enquete de interesse enviada e >30 respostas positivas
[ ] Pré-venda com ao menos 10 compradores antes de gravar tudo
[ ] Módulo 1 gravado e revisado
[ ] Buffer de cronograma definido
```

---

## Artefatos de Saída
- Resumo no chat: máx 3 frases (falha mais provável + suposto oculto + revisão mais importante)
- Relatório completo em arquivo, se solicitado

---

## Completion

- [ ] Sub-agentes executaram em paralelo (cada um com framing "já falhou")
- [ ] 4 outputs entregues: falha mais provável, mais perigosa, suposto oculto, plano revisado (3-5 ajustes)
- [ ] Checklist pré-lançamento com 3-5 verificações concretas
- [ ] Resumo no chat: máx 3 frases
- [ ] Riscos específicos ao plano (não genéricos)

## Failure modes

- **Cortês com o plano**: sugestões suavizadas → framing "já falhou" é o mecanismo crítico
- **Sequential sub-agents**: lançar sub-agentes em sequência → paralelo obrigatório, sequencial contamina
- **Generic risks**: "pode falhar por falta de mercado" → sempre específico ao plano concreto
- **Force-count**: forçar 7 falhas quando há 3 reais → quantidade segue qualidade, não quota

---

## Restrições
- NUNCA ser cortês com o plano — o framing "já falhou" é o mecanismo psicológico crítico
- NUNCA lançar sub-agentes em sequência — paralelo obrigatório (sequencial contamina)
- NUNCA forçar 7 falhas se há 3, nem parar em 3 se há 7
- NUNCA usar riscos genéricos ("pode falhar por falta de mercado") — sempre específico ao plano
- Diferente de risk assessment: premortem vai ao futuro onde falhou, não avalia probabilidades no presente

---

## Relacionado

- Skill `debate` — escolhe entre duas opções antes de haver um plano
- Skill `council` — decide qual plano adotar; pre-mortem estressa o plano já escolhido

---

*Fonte do método: Gary Klein (Harvard Business Review), com endosso de Daniel Kahneman.*
