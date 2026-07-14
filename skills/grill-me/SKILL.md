---
name: grill-me
description: Asks sharp clarifying questions before acting on any plan, decision, or task — not just code. Walks a decision tree one question at a time, recommends answers, explores the environment (codebase, notes, sources) for evidence. Use when the user says "grill me", "me questiona", "clarifica isso", "antes de codar", "antes de decidir", "vamos pensar nisso", "design this", "me ajuda a decidir", or when the user describes a feature/task/decision that has ambiguity, multiple valid approaches, or hidden assumptions. Also trigger when the user jumps straight to acting on a non-trivial task without specifying requirements.
---

# Grill Me

Clarificacao implacavel antes de agir — codigo, plano, decisao, ou qualquer tarefa. Uma pergunta por vez. Sem pular pra acao.

## Regras

1. **Uma pergunta por vez.** Nao bombardear com lista. Esperar resposta. Mecanismo, nao estilo: resposta N molda pergunta N+1; lista quebra o encadeamento e gera respostas rasas.
2. **Recomendar resposta.** Sempre sugerir o que voce faria e por que. Usuario pode aceitar ou divergir. Nunca largar pergunta crua.
3. **Explorar o ambiente.** Quando possivel, ler o contexto relevante antes de perguntar — codigo, notas do vault, fontes, docs. Perguntas fundamentadas > perguntas genericas.
4. **Facts vs Decisions (anti-self-grilling).** **Facts** = o que voce descobre explorando o ambiente (padroes, o que ja existe) → resolva sozinho, NAO pergunte. **Decisions** = o que so o usuario decide (escopo, arquitetura, trade-off) → e o que voce grilla. Nunca grille a si mesmo.
5. **Caminhar a decision tree.** Cada resposta abre galho novo ou fecha. Seguir ate folhas.
6. **Confirmation gate.** NAO agir ate o usuario confirmar entendimento compartilhado. Sessao nao termina pulando pra acao — parar e esperar "ok, pode agir".

## Decision Tree — Ordem de Exploracao

```
1. PROBLEMA — O que exatamente nao funciona / falta / precisa decidir?
2. USUARIO/STAKEHOLDER — Quem e afetado? Qual o fluxo?
3. SCOPE — O que esta dentro? O que esta FORA? (scope negativo)
4. ABORDAGEM — Quais opcoes? Trade-offs?
5. DADOS/EVIDENCIA — Que informacao precisa? De onde vem?
6. EDGE CASES — O que pode dar errado?
7. SUCESSO — Como saber que funciona? Criterio de sucesso?
8. DEPENDENCIAS — O que precisa existir antes?
```

Aplica a codigo E a decisoes nao-tecnicas (estudo, plano de carreira, escolha de ferramenta, estrategia).

## Matriz de Unknowns (Fable — finding your unknowns)

Antes de formular, mapeie o plano nos 4 quadrantes. Alvo do grilling = mover coisas p/ cima e p/ esquerda:

| | **Knowns** | **Unknowns** |
|---|---|---|
| **Known** | fatos assumidos → confirmar que ainda valem | perguntas ja abertas → priorize |
| **Unknown** | falso-consenso ("todo mundo sabe", nao-testado) → challenge | **unknown-unknowns** → o mais perigoso; cave com "e se seu modelo mental estiver errado?" |

Os **unknown-unknowns** (canto inferior-direito) sao o valor real. Gaste as perguntas duras ali, nao no que ja e known-unknown.

Nao seguir ordem rigida — adaptar ao contexto. Mas cobrir todos antes de declarar pronto.

## Formato de Cada Pergunta

```
**[CATEGORIA]:** [Pergunta clara e especifica]

> Recomendo: [sua sugestao]. [1 frase de justificativa].
```

## Constraints

- NAO agir durante grill. Zero codigo, zero execucao do plano.
- NAO fazer multiplas perguntas por turno.
- NAO aceitar respostas vagas — repergunta com opcoes concretas.
- NAO pular pra solucao antes de entender o problema.
- Se usuario pedir pra parar e agir → respeitar, mas listar decisoes pendentes.

## Quando Parar

Todas verdadeiras:
- [ ] Problema claro e especifico
- [ ] Scope definido (incluindo o que esta FORA)
- [ ] Abordagem escolhida com trade-offs aceitos
- [ ] Edge cases identificados
- [ ] Criterio de sucesso definido

Entao: "Pronto. Quer que eu aja direto ou gera doc (PRD/plano) primeiro?"

## Modo questionário (resposta não existe na sessão)

Nem toda pergunta resolve na hora. Resposta que é unknown-unknown dependente de terceiro (stakeholder, dado externo, teste ainda não feito) → NÃO travar o confirmation gate. Emitir questionário e seguir grillando o resolvível.

- **Trigger:** usuário responde "não sei", "preciso perguntar pra X", "depende de dado que não tenho" — ou pergunta cai em unknown-unknown sem base pra recomendar.
- **Ação:** registrar a pergunta num artefato questionário (markdown), NÃO inventar resposta. Continuar a sessão com as perguntas que dão pra resolver agora.
- **Loop:** respostas preenchidas offline/colaborativo voltam como input → nova rodada de grilling sobre elas. Questionário fecha o gap sem bloquear a sessão.

```
## Questionário — <tópico>
### Q1 [CATEGORIA]
Pergunta: <clara e específica>
Contexto: <por que importa / o que trava sem isso>
Opções conhecidas: A / B / (outra)
Resposta: _____
```

## Linhagem

- **Upstream:** Matt Pocock (grilling v1.1, generalizado no PR #532; grilling → questionnaire loop) + Fable (matriz de unknowns) + Karpathy P1 (think before acting).
- **Original (vault):** scope negativo, decision tree 8-cat, Facts vs Decisions (anti-self-grilling), confirmation gate.
- **Critério:** mecanismo > autor. Fonte rastreável, não privilegiada.

**Fonte canonica executavel:** este arquivo (michel-skills:grill-me) — versao portavel invocavel globalmente.
Wiring vault-interno (delegacao a `domain-modeling`, captura CONTEXT.md/ADR, model-per-etapa) vive em `04-SYSTEM/skills/foundational/grill-me.md`, que aponta pra ca. NAO duplicar o motor nos dois — mecanismo aqui, integracao vault la.
