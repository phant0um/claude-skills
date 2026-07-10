---
name: grill-me
description: Desafia um plano ou ideia com perguntas duras, uma por vez, antes de qualquer implementação — expõe pressupostos falsos, ambiguidades e riscos ocultos enquanto o custo de mudança ainda é zero.
trigger: "@grill [plano]" | "me questione sobre X" | "testa esse plano" | "quero ser desafiado" | "grill me" | "stress-test this plan" | "challenge this before I build"
---

# Skill: Grill Me

## Propósito
Desafiar um plano ou ideia com perguntas duras antes de qualquer implementação. Expõe pressupostos falsos, ambiguidades e riscos ocultos enquanto o custo de mudança ainda é zero.

Adaptado das skills de Matt Pocock (github.com/mattpocock/skills). Funciona com ou sem codebase existente.

---

## Condições de Ativação
Ative esta skill quando:
- `@grill [plano | feature | ideia]` for chamado
- O usuário disser "me questione sobre X", "testa esse plano", "quero ser desafiado"
- Uma feature não-trivial for iniciada sem grilling prévio
- A complexidade estimada for >2h de implementação

NÃO ative para: bugs pontuais já bem definidos; tarefas mecânicas sem decisão de design; quando o usuário explicitamente pular ("skip grill").

---

## Modelo por Etapa

| Etapa | Modelo | Justificativa |
|-------|--------|---------------|
| Leitura de contexto + formulação de perguntas | Sonnet | Requer compreensão semântica e julgamento |
| Síntese de respostas + identificação de gaps | Sonnet | Raciocínio sobre coerência e completude |
| Atualização de notas de contexto (se existir) | Haiku | Edição mecânica estruturada |

---

## Protocolo de Execução

### ETAPA 1 — Leitura de Contexto *(Sonnet)*
Antes de grillar, colete:

```
- Qual é o objetivo final? (não a feature — o resultado de negócio)
- Quem usa isso e em qual situação?
- O que já existe que resolve parte disso?
- Há docs de contexto, ADRs ou specs relevantes? Leia-os.
```

Se não houver contexto suficiente: faça 1-2 perguntas de bootstrap antes de avançar.

### ETAPA 2 — Formulação de Perguntas Duras *(Sonnet)*
Gere 5-8 perguntas nas categorias abaixo. Priorize as que o usuário provavelmente NÃO pensou.

**Categorias obrigatórias:**

| Categoria | Exemplo de pergunta |
|-----------|-------------------|
| Pressupostos | "Você assumiu X — o que acontece se X for falso?" |
| Casos extremos | "Como se comporta quando Y = zero / vazio / máximo?" |
| Conflito com existente | "Isso contradiz [decisão anterior Z] — é intencional?" |
| Critério de sucesso | "Como você saberá que funcionou? Qual métrica?" |
| Custo oculto | "Quem mantém isso daqui a 6 meses?" |
| Alternativa mais simples | "Por que não [solução mais simples]?" |
| Reversibilidade | "Se der errado, como desfaz?" |

**Tom:** direto, sem suavização. Não é sessão de brainstorm — é teste de pressão.

**Regras do motor:**
- **Uma pergunta por vez** — espere feedback antes da próxima. Múltiplas de uma vez desnorteiam: o usuário não sabe qual atacar, responde raso, e o encadeamento (resposta N molda pergunta N+1) quebra. Uma por vez é o mecanismo, não estilo.
- **Dê tua resposta recomendada** em cada pergunta — não largue a pergunta crua.
- **Facts vs Decisions** (anti-self-grilling): distingue os dois. **Facts** = o que você acha explorando o codebase (padrões, implementações existentes) — resolva sozinho, NÃO pergunte. **Decisions** = o que só o usuário decide (arquitetura, escopo de feature) — é o que você grilla. Nunca grille a si mesmo explorando código sem input humano.

Output (uma por vez):
```
GRILLING SESSION — [título do plano]

Q1: [pergunta]
   Recomendação: [tua resposta sugerida + porquê]
   → aguarda feedback
```

### ETAPA 3 — Ciclo de Resposta *(iterativo)*
```
- Usuário responde cada pergunta
- Para cada resposta: identifique se resolve o ponto ou expõe novo gap
- Se novo gap: adicione 1-2 perguntas de follow-up
- Repita até: todas as perguntas respondidas satisfatoriamente OU usuário encerrar
```

### ETAPA 4 — Síntese *(Sonnet)*
Após ciclo completo, produza:

```markdown
## Síntese do Grilling — [título]

### Pressupostos confirmados
- [lista]

### Riscos identificados
- [risco]: [mitigação acordada | ABERTO]

### Decisões tomadas
- [decisão]

### Próximo passo recomendado
[spec | implementação | pesquisa adicional | descartar]
```

> **Confirmation gate:** NÃO execute o plano até o usuário confirmar que chegamos a entendimento compartilhado. Sessão de grilling não termina pulando direto p/ implementação — pare e espere o "ok, pode implementar".

### ETAPA 5 — Registrar Contexto *(Haiku, opcional)*
Se existir um doc de contexto no projeto:
- Adicione termos de domínio que emergiram no grilling
- Registre decisões como ADR inline:
  ```
  ## ADR-<n>: [título]
  **Contexto:** [problema]
  **Decisão:** [o que foi decidido]
  **Consequências:** [trade-offs]
  ```

Se não existir doc de contexto e >3 termos de domínio emergiram: proponha criação.

---

## Exemplo

**Plano:** "Vou adicionar um cache Redis para acelerar o endpoint de perfil."

```
GRILLING SESSION — cache Redis no endpoint de perfil

Q1: Qual é a latência atual do endpoint e qual é a meta?
   Recomendação: medir antes — se a lentidão vem de uma query N+1,
   um índice resolve sem introduzir Redis (custo oculto de manter
   um serviço a mais). Só cachear se a query já estiver otimizada.
   → aguarda feedback
```

Usuário: "Nunca medi, achei que estava lento."

```
Q2: Como o cache é invalidado quando o perfil muda?
   Recomendação: sem estratégia de invalidação, você serve dados
   velhos. Se o perfil muda raramente, TTL curto basta; se muda com
   frequência, o cache mal ajuda. Defina isto antes de escrever código.
   → aguarda feedback
```

**Síntese:** premissa "está lento" era não-verificada (risco: otimização prematura). Decisão: medir primeiro; provavelmente só falta um índice. Próximo passo: profiling, não Redis.

---

## Completion

- [ ] Perguntas não suavizadas ("Você considerou que X pode falhar?" não vira "Talvez valha pensar em X?")
- [ ] Plano não aceita "vai funcionar" sem raciocínio específico
- [ ] Máximo 8 perguntas por rodada
- [ ] Se plano não sobreviveu: reportado como sucesso (encontrou problema barato)
- [ ] Síntese com riscos e decisões entregue

## Failure modes

- **Softened questions**: suavizar perguntas críticas → mecanismo da skill é a tensão, não cortesia
- **Accept vague assurance**: aceitar "vai funcionar" → exigir raciocínio específico de por que
- **Over-asking**: 10+ perguntas por rodada → qualidade > quantidade, máx 8
- **No docs captured**: grilling revela decisão arquitetural mas não registra ADR → capturar inline
- **Fuzzy term unsharpened**: user usa termo vago ("account") e skill não challenge → propor termo canônico
- **Self-grilling**: agente explora código e grilla a si mesmo sem input humano → Facts resolve sozinho, só Decisions viram pergunta
- **Jump to implementation**: sessão encerra e agente parte pra codar sem confirmação → confirmation gate obrigatório

---

## Captura de Domínio

Durante o grilling, quando uma decisão ou termo cristalizar, registre-o na hora — grilling sem captura é perguntas desperdiçadas, porque as decisões evaporam:

1. **Termo resolvido** → atualiza o glossário do doc de contexto inline (glossário SÓ, zero implementação; não batchar)
2. **Decisão arquitetural** → registre um ADR se os 3 critérios valerem (difícil de reverter + surpreendente + trade-off real). Falta um → skip.
3. **Termo fuzzy** → challenge: "Você disse 'account' — Customer ou User? São coisas diferentes."

---

## Regras de Ouro

- **Não suavize perguntas** — "Você considerou que X pode falhar completamente?" não vira "Talvez valha pensar em X?"
- **Não aceite "vai funcionar"** — exija raciocínio específico
- **Máximo 8 perguntas por rodada** — qualidade > quantidade
- **Se o plano não sobreviver ao grilling**: é um sucesso, não falha — encontrou o problema barato

---

## Artefatos de Saída
- Síntese estruturada com riscos e decisões
- Doc de contexto atualizado (se existente)
- Recomendação de próximo passo
