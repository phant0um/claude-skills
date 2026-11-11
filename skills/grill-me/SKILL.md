---
kind: skill-proc
resolver-status: exposed
name: grill-me
skill: grill-me
type: skill
version: "2.1.0"
author: Nexus Agent System
source: mattpocock/skills (grilling v1.1) + Fable "finding your unknowns" (matriz de unknowns)
source_version: 1.2.3
id: "grill-me"
title: "Skill: Grill Me"
created: "2026-06-19"
updated: 2026-10-11
status: active
owner: nexus
tags: ["pre-implementation", "grilling", "alignment", "challenge", "planning"]
description: "Use when: desafiar plano, feature ou decisão ANTES de implementar — entrevista adversarial que expõe pressuposto falso, ambiguidade e risco oculto enquanto mudar custa zero. Fecha com gate de confirmação. MODO PREMISSAS: enumerar e classificar as premissas do plano sozinho, sem entrevista. Ideia sem plano ainda: office-hours; deliberação multi-perspectiva: council; antecipar falha de plano pronto: pre-mortem."
triggers:
  positive:
    - "me questione sobre"
    - "testa esse plano"
    - "quero ser desafiado"
    - "grill"
    - "desafia essa ideia antes de implementar"
    - "enumerar o que poderia estar errado nas premissas"
  negative:
    - "decisão barata e reversível (grilling custa mais que o erro)"
    - "fato verificável — buscar a fonte, não interrogar"
    - "plano já aprovado e em execução"
    - "bug pontual já bem definido, sem decisão de design"
route:
  profile: "deep"
  risk: "medium"
consumes: []
reads: ["plan", "feature", "assumptions", "decisions"]
writes: []
tools: []
references:
  - "04-SYSTEM/automation/skills/meta/domain-modeling/SKILL.md"
  - "04-SYSTEM/automation/skills/reasoning/office-hours/SKILL.md"
verifier:
  - "No máximo 8 perguntas por rodada."
  - "Cada pergunta recebeu resposta explícita antes da síntese."
  - "Síntese registra pressupostos confirmados, riscos, decisões e próximo passo."
  - "Gate de confirmação alcançado — grilling não termina por cansaço."
human_gate: false
upstream: "~/.agents/skills/grill-me/SKILL.md"
restored-from: "defac13fc^ (04-SYSTEM/automation/skills/foundational/grill-me/SKILL.md)"
restored: 2026-09-02
restored-reason: "defac13fc deletou o arquivo como 'morto'. Nao estava: 9 docs vivos apontavam para ele (workflows/vault-maintenance/revisao-semanal, procedures/core spec+extend, 6 SKILL.md, moc-skills) e o passo 3 do nexus.md exige 'invocar a skill grill-me'. O upstream ~/.agents/skills/grill-me e' shim de 147 B ('Run a /grilling session') e ~/.agents/skills/grilling tem 12 linhas, 843 B, zero headings — nao substitui as 220 linhas daqui. O que se perdeu era conteudo proprio do vault: ETAPA 5 (atualizar CONTEXT.md), Doc Capture delegando a domain-modeling, Failure modes, Completion e a matriz de unknowns do Fable. Promovido de kind:reference/not-exposed para skill-proc/exposed por decisao do usuario 2026-09-02: o vault vira canonico do nome grill-me."
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Skills citadas existem (domain-modeling, office-hours, to-questionnaire em ~/.agents/skills, wait-what). doubt-driven-development resolve em grill-me/. Campos upstream e restored-from nao reverificados."
---


# Skill: Grill Me

## Propósito
Desafiar um plano ou ideia com perguntas duras antes de qualquer implementação. Expõe pressupostos falsos, ambiguidades e riscos ocultos enquanto o custo de mudança ainda é zero.

---

## Quando NÃO usar

- **Decisão de baixo risco reversível** — grilling custa mais que o erro.
- **Fato verificável** — grill não resolve fato; buscar a fonte.
- **Plano já aprovado e em execução** — grill é pré-implementação; interromper execução para re-grillar é ruído.
- **Interlocutor sem tempo/disposição para o ciclo completo** — grilling é exaustivo por design; meia entrevista não afia nada.

Disambiguation: `grill-me` é entrevista adversarial para afiar plano/decisão; `office-hours` interroga ideia com forcing-questions; `council` delibera com 5 perspectivas; `pre-mortem` antecipa falhas — grill é o mais agressivo e o mais cedo no ciclo. Plano aprovado no gate que vai para outro modelo executar segue para `plan-handoff`.


## Condições de Ativação
Ative esta skill quando:
- `@grill [plano | feature | ideia]` for chamado
- O usuário disser "me questione sobre X", "testa esse plano", "quero ser desafiado"
- `spec` ou `forge` forem acionados sem grilling prévio em feature não-trivial
- A complexidade estimada for >2h de implementação

NÃO ative para: bugs pontuais já bem definidos; tarefas mecânicas sem decisão de design; quando o usuário explicitamente pular ("skip grill").

MODO PREMISSAS (abaixo) quando: `@doubt [feature/spec/ideia]`; antes de `spec` ou
`forge` em feature com >3 premissas implícitas; o usuário diz "tenho dúvidas sobre
X"; ou não há interlocutor disponível para a entrevista.

---

## Perfil de modelo

Perfil `deep` — interrogatorio pre-implementacao: a pergunta que nao foi feita vira retrabalho estrutural (model-routing §Padrao custo-efetivo; model-catalog §Perfis). Esta skill nao mantem pins locais por etapa.

## Protocolo de Execução

### ETAPA 1 — Leitura de Contexto
Antes de grillar, colete:

```
- Qual é o objetivo final? (não a feature — o resultado de negócio)
- Quem usa isso e em qual situação?
- O que já existe que resolve parte disso?
- Há GLOSSARY.md, ADRs ou docs relevantes? Leia-os.
```

Antes da primeira pergunta dura: reformule em 2-3 frases, com tuas palavras, o objetivo e o problema do usuário, e peça "sim / não / ajuste"; só então pergunte.

Se não houver contexto suficiente: faça 1-2 perguntas de bootstrap antes de avançar.

### ETAPA 2 — Formulação de Perguntas Duras
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

**Matriz de unknowns** (Fable "finding your unknowns") — antes de formular, mapeie o plano nos 4 quadrantes; o alvo do grilling é mover coisas p/ cima e p/ a esquerda:

| | **Knowns** | **Unknowns** |
|---|---|---|
| **Known** | fatos assumidos → confirmar que ainda valem | perguntas já abertas → priorize estas |
| **Unknown** | falso-consenso: "todo mundo sabe" não-testado → challenge | **unknown-unknowns**: o mais perigoso → cave com "o que aconteceria se seu modelo mental estivesse errado?" |

Os **unknown-unknowns** (canto inferior-direito) são o valor real do grilling — perguntas que expõem riscos que o autor nem sabe que tem. Gaste as perguntas duras aqui, não no que já é known-unknown.

**Tom:** direto, sem suavização. Não é sessão de brainstorm — é teste de pressão.

**Regras do motor (upstream `grilling` v1.1 + frontier, portada de `michel-skills` 681b926):**
- **Uma rodada de frontier por vez.** A **frontier** é toda decisão cujos pré-requisitos já estão resolvidos: as perguntas que dá para fazer AGORA sem chutar uma resposta que você ainda não ouviu. Pergunte a frontier inteira numa rodada, numerada, cada pergunta com sua recomendação, e espere as respostas antes da próxima. Pergunta cuja resposta depende de outra ainda aberta NESTA rodada pertence à rodada seguinte. Isso preserva o encadeamento (resposta N molda a pergunta N+1) sem gastar um turno por pergunta. Lista bruta de tudo que você quer saber não é frontier: é o anti-padrão. Frontier com mais de 8 itens: priorize os unknown-unknowns e deixe o resto para a rodada seguinte.
- **Dê tua resposta recomendada** em cada pergunta — não largue a pergunta crua.
- **Facts vs Decisions** (anti-self-grilling): distingue os dois. **Facts** = o que você acha explorando o codebase (padrões, implementações existentes) — resolva sozinho, NÃO pergunte. **Decisions** = o que só o usuário decide (arquitetura, escopo de feature) — é o que você grilla. Nunca grille a si mesmo explorando código sem input humano.

Output (uma rodada por vez):
```
GRILLING SESSION — [título do plano]

Rodada N — frontier: [o que já está resolvido e destravou estas perguntas]

Q1 · [CATEGORIA]: [pergunta]
   Recomendação: [tua resposta sugerida + porquê]

---

Q2 · [CATEGORIA]: [pergunta]
   Recomendação: [tua resposta sugerida + porquê]
   → aguarda as respostas da rodada
```

Rodada de uma pergunta só é legítima: é o que acontece quando a frontier tem um item.

### ETAPA 3 — Ciclo de Resposta *(iterativo)*
```
- Usuário responde a rodada
- Para cada resposta: identifique se resolve o ponto ou expõe novo gap
- Decisão resolvida empurra a frontier para fora e destrava o que dependia dela
- Recompute a frontier (inclui follow-ups de gaps novos) e faça a próxima rodada
- Repita até: frontier vazia (todo galho visitado, nada assumido em silêncio) OU usuário encerrar
```

### ETAPA 4 — Síntese
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
[spec | forge | pesquisa adicional | descartar]
```

> **Confirmation gate (upstream v1.1):** NÃO execute o plano até o usuário confirmar que chegamos a entendimento compartilhado. Sessão de grilling não termina pulando direto p/ implementação — pare e espere o "ok, pode implementar".

### ETAPA 5 — Atualizar GLOSSARY.md
Se existir `GLOSSARY.md` no projeto:
- Adicione termos de domínio que emergiram no grilling
- Registre decisões como ADR inline:
  ```
  ## ADR-<n>: [título]
  **Contexto:** [problema]
  **Decisão:** [o que foi decidido]
  **Consequências:** [trade-offs]
  ```

Se não existir `GLOSSARY.md` e >3 termos de domínio emergiram: proponha criação.

## MODO PREMISSAS — solo, sem entrevista

Absorvido de [doubt-driven-development](doubt-driven-development.md) (adr-nx-018). A entrevista
desafia o **plano**; este modo desafia as **premissas** que o plano assume, em
batch, sem perguntar nada ao usuário. Roda antes da entrevista (as premissas
`frágil` viram perguntas da ETAPA 2) ou depois dela, como segunda camada.
Premissa que só o usuário decide não é resolvida aqui: vira pergunta, pela regra
Facts vs Decisions.

**P1 — Enumerar premissas.** Toda afirmação que precisa ser verdade para o design
funcionar, com a fonte: `explícita | inferida | assumida`. Tipos: domínio (regra
de negócio), técnica (constraint externa), comportamental (expectativa de uso),
temporal (deadline implícito). Mínimo 5, mesmo que pareçam óbvias.

**P2 — Aplicar as 5 dúvidas.** Uma ou mais por premissa, priorizando as
`assumida` e as que aparecem em mais de uma cascata:

| # | Dúvida | Pergunta |
|---|--------|----------|
| D1 | Falsabilidade | Como provaríamos que esta premissa é falsa? |
| D2 | Condicional | Sob qual condição ela deixa de valer? |
| D3 | Cascade | Se for falsa, quais outras caem junto? |
| D4 | Temporal | É verdade hoje. Será em 6 meses? |
| D5 | Proxy | É o que queremos saber, ou um proxy para outra coisa? |

**P3 — Veredito por premissa.** `confirmada` (prosseguir) · `frágil` (validar antes
de build, com método) · `condicional` (a condição vira requisito explícito) ·
`falsa` (redesign) · `proxy` (reescrever em termos da premissa real).

**Output:**

```markdown
## Análise de premissas — [título]

| Premissa | Fonte | Dúvida | Veredito | Ação |
|----------|-------|--------|----------|------|
| P1 | assumida | D3 — derruba P5, P6 | frágil | [como validar antes de build] |

Próximo passo: [entrevista (ETAPA 2) | spec | validação externa | redesign | descartar]
```

Completion do modo: toda premissa `assumida` recebeu ≥1 dúvida; D3 rodou nas
`frágil`; toda `frágil` tem método de validação; toda `condicional` gerou
requisito. Failure modes: duvidar só das explícitas (o valor está nas
assumidas); `frágil` sem método de validação; ignorar D3, que é onde se separa
redesign de ajuste pontual.

---

## Completion

- [ ] Perguntas não suavizadas ("Você considerou que X pode falhar?" não vira "Talvez valha pensar em X?")
- [ ] Plano não aceita "vai funcionar" sem raciocínio específico
- [ ] Máximo 8 perguntas por rodada
- [ ] Se plano não sobreviveu: reportado como sucesso (encontrou problema barato)
- [ ] Síntese com riscos e decisões entregue

---

## Doc Capture → delega a `domain-modeling`

Durante o grilling, quando uma decisão ou termo cristalizar, aplique a skill [domain-modeling](../domain-modeling/SKILL.md) (disciplina ativa de modelo de domínio). Resumo do que ela faz:

1. **Termo resolvido** → atualiza GLOSSARY.md inline (glossário SÓ, zero implementação; não batchar)
2. **Decisão arquitetural** → oferece ADR via `/decisions` se os 3 critérios (hard to reverse + surprising + real trade-off). Falta um → skip.
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
- GLOSSARY.md atualizado (se existente)
- Recomendação de próximo passo
- Stakeholder ausente: exporte a rodada com a skill `to-questionnaire`
  (perguntas + contexto num arquivo que ele responde sem a sessão). Não
  invente a resposta dele.
- Explicação confusa no meio da rodada: aplique `wait-what` antes de seguir.
