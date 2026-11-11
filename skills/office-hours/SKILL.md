---
origin: native
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: office-hours
description: "Use when: /office-hours — interrogatório de DECISÃO: a ideia merece investimento? 6 forcing-questions estilo YC. Fase de avaliação pré-compromisso. Diferente de [pre-mortem](../pre-mortem/SKILL.md) (que assume o compromisso e busca como vai falhar via prospective hindsight); office-hours é 'vale a pena fazer?', pre-mortem é 'como isso dá errado?'."
type: skill
created: 2026-06-27
updated: 2026-11-10
reads: []
writes: []
triggers:
  positive:
    - "/office-hours"
    - "interrogar produto ou ideia antes de investir"
    - "6 forcing-questions de produto"
  negative:
    - "produto já validado no mercado"
    - "decisão de implementação já tomada"
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7: corpo completo lido pelo shield (opus, somente leitura); W3: Completion alinhado as 6 perguntas e ao fecho go/pivot/drop; checks frontmatter/lint/evals verdes; 64 linhas, 4 secoes"
---
# office-hours — interroga a ideia antes de construir

Aplica quando: nova ideia de produto/projeto/empreendimento, antes de planejar.
Inspiração: gstack /office-hours (Garry Tan, YC).

## Quando NÃO usar

- **Pergunta de fato** — office-hours é para debate/julgamento; fato vai para busca dirigida.
- **Decisão com deadline imediato** — a skill assume disponibilidade para conversar; se urgente, decidir com o que há.
- **Questão já resolvida na sessão** — reabrir decisão fechada é ruído; respeitar o veredito anterior.
- **Ideia sem autor disposto a iterar** — sem interlocutor, as 6 perguntas não têm resposta; adiar.

Disambiguation: `office-hours` interroga a ideia antes de construir; `grill-me` é entrevista adversarial para afiar plano; `council` delibera com 5 perspectivas — office-hours assume um interlocutor e sai com decisão go/pivot/drop.

## 6 forcing-questions
1. Qual o problema real, e de quem? (1 frase, sem jargão)
2. Por que agora? O que mudou?
3. Qual a menor coisa que prova/refuta isto em 1 semana?
4. Quem já tenta resolver, e por que falham/bastam?
5. Se desse 10×, como seria? Se falhasse, por quê (pré-mortem)?
6. Próximo passo concreto, mensurável, esta semana?

Saída: respostas curtas + 1 decisão (go / pivot / drop). Liga a empreendedorismo.
Sem sycophancy — desafiar a premissa (cf council/debate/grill-me).

> [grill-me](../grill-me/SKILL.md) **não é modo de office-hours**: é skill própria, exposta e canônica desde 2026-09-02 (antes era stub `not-exposed` do shim externo). Editar comportamento de grilling se faz lá, no vault. Distinção: office-hours interroga uma ideia com forcing-questions; grill-me faz entrevista adversarial de um plano.

## Completion

- [ ] As 6 forcing-questions respondidas de forma curta; sem dado, a resposta diz "sem dado" e o que falta.
- [ ] Ao menos uma premissa foi desafiada (sem sycophancy).
- [ ] Saída fecha com 1 decisão: go / pivot / drop.

## Failure modes

- **Sycophancy**: aceitar a premissa da ideia sem desafiar → questione cada forcing-question.
- **Sair sem decisão**: respostas sem go / pivot / drop no fim → feche com uma decisão.
- **Reabrir decisão fechada**: reinterrogar ideia já resolvida na sessão → respeite o veredito anterior.
- **Confundir com grill-me**: entrevistar um plano em vez de uma ideia → plano vai para `grill-me`.
