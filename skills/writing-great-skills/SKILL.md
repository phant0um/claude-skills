---
name: writing-great-skills
description: "Referência p/ escrever e editar skills bem — o vocabulário e princípios que tornam uma skill previsível. Chame ao criar/revisar SKILL.md, decidir invocação model vs user, ou diagnosticar skill que não dispara/derrapa."
trigger: "/writing-great-skills · 'como escrever skill' · 'revisar skill' · 'write a skill' · 'review this skill'"
version: 1.0
effort: low
tags: [skills, meta, writing, predictability, leading-words]
---

# Skill: Writing Great Skills

Skill existe p/ arrancar **determinismo** de sistema estocástico. **Previsibilidade** — o agente tomar o mesmo _processo_ toda run, não produzir o mesmo output — é a virtude-raiz; toda alavanca abaixo serve a ela.

> É a **referência de qualidade** da forma-skill. Complementa a skill `content-design` (front-load de artefato).

---

## Invocação — 2 escolhas, custos diferentes
- **Model-invoked**: mantém **description** → agente dispara autônomo E outras skills alcançam. Custa **context load** (description no contexto todo turno). Mecânica: omitir `disable-model-invocation`, description rica em triggers ("Use quando o user…, menciona…").
- **User-invoked**: tira description do alcance do agente — só você, digitando o nome, invoca. Zero context load, mas gasta **cognitive load** (_você_ é o índice que lembra que existe). Mecânica: `disable-model-invocation: true`; description vira humana (resumo 1 linha, triggers removidos).

Escolha model só quando o agente precisa alcançar sozinho, ou outra skill precisa. Se só dispara à mão → user-invoked, zero context load.
Quando user-invoked multiplicam além do que você lembra, essa cognitive load acumulada cura-se com **router skill** (uma user-invoked que nomeia as outras).

## Escrevendo a description
Faz 2 jobs — dizer o que a skill é, e listar os **branches** que a disparam. Cada palavra aumenta context load → poda mais dura que o corpo:
- **Front-load a leading word** — a description é onde ela faz o trabalho de invocação.
- **Um trigger por branch.** Sinônimos que renomeiam um branch = **duplicação**. Colapse; só branches genuinamente distintos.
- **Corte identidade que já está no corpo.** Só triggers + cláusula "quando outra skill precisa…".

## Trigger metadata (OpenHands)
Description é prosa; o *dispatch* fica mais confiável quando os triggers são **explícitos e escopados**, como microagent OpenHands. Três campos no frontmatter, além da description:
- **`trigger` (keywords, não frase)** — lista de palavras-gatilho literais que o agente casa, não parágrafo em prosa. Prosa infla context load e dispara fuzzy; keyword casa determinística. Um keyword por branch (mesma regra da description).
- **Escopo — global vs project** — microagent OpenHands é *knowledge* (sempre no alcance) ou *repo* (só naquele repo). Espelhe: skill de domínio declara escopo via `tags:` → não polui context fora do domínio. Sem escopo = global = paga context load toda sessão. Declare escopo estreito por padrão.
- **Anti-trigger (`negative`)** — diga *quando NÃO disparar*. Sem isso, keyword genérico ("revisar") canibaliza turnos vizinhos. Um anti-trigger corta o falso-positivo mais provável (ex: negative "single technical question").

## Hierarquia de informação
Skill = **steps** + **reference**, misturam livre. Escada por urgência:
1. **In-skill step** — ação ordenada no SKILL.md, tier primário. Cada step fecha num **completion criterion** _checável_ (dá p/ saber done de não-done?) e, onde importa, _exaustivo_ ("todo model modificado contabilizado", não "produza lista"). Critério vago convida **premature completion**.
2. **In-skill reference** — definição/regra/fato consultado sob demanda. Muitas vezes peer-set legitimamente flat (toda regra numa mesma rung).
3. **External reference** — reference empurrado p/ arquivo separado, alcançado por **context pointer**, carregado só quando o pointer dispara.

Empurra pouco → topo incha; empurra demais → esconde o que o agente precisa. Essa tensão é a decisão inteira. **Progressive disclosure** = o movimento escada abaixo (p/ arquivo linkado) p/ o topo ficar legível. **Branch** é o teste mais limpo: inline o que todo branch precisa, esconde atrás de pointer o que só alguns alcançam. A _redação_ do pointer, não o alvo, decide quando/quão confiável o agente alcança.
**Co-location**: mantenha definição, regras e caveats de um conceito sob um heading, não espalhados.

## Quando dividir (granularity)
Cada corte gasta uma das 2 loads → divida só quando compensa.
- **Por invocação** — separe skill model-invoked quando há **leading word** distinta que deve dispará-la, ou outra skill precisa alcançar. Paga context load da description sempre-carregada.
- **Por sequência** — divida run de steps quando os steps à frente tentam o agente a apressar o da frente (premature completion). Escondê-los força mais **legwork** na tarefa atual.

## Poda
- **Single source of truth**: cada significado num lugar autoritativo — mudar comportamento = edit de um lugar.
- **Relevance**: cada linha ainda pesa no que a skill faz?
- **No-ops** frase a frase: rode o no-op test em cada frase isolada; falhou → delete a frase inteira, não apare palavras. Seja agressivo.

## Leading words
Conceito compacto já vivo no pretraining que o agente pensa-com ao rodar a skill (ex: _lesson_, _fog of war_, _tracer bullets_, _tight_, _red_). Repetido, acumula definição distribuída e ancora uma região de comportamento em pouquíssimos tokens, recrutando priors que o modelo já tem.
Serve previsibilidade 2×: no **corpo** ancora _execução_ (mesmo comportamento toda vez que a palavra aparece); na **description** ancora _invocação_ (linguagem compartilhada em prompts/docs/código → dispara mais confiável).
Cace refactor: "fast, deterministic, low-overhead" → _tight_; "loop em que você acredita" → _red_ (gate fuzzy vira estado binário observável). Ganha 2×: menos tokens E hook mais afiado.

## Failure modes (diagnóstico)
- **Premature completion** — fecha step antes de done, atenção escorrega p/ _estar done_. Defesa em ordem: afiar completion criterion (barato); só se irredutivelmente fuzzy E você observa a pressa, esconda post-completion steps dividindo.
- **Duplication** — mesmo significado em >1 lugar. Custa manutenção, tokens, e infla a proeminência do significado na escada.
- **Sediment** — camadas velhas que assentam porque adicionar parece seguro e remover parece arriscado. Destino default sem disciplina de poda.
- **Sprawl** — skill longa demais mesmo com toda linha viva. Cura = a escada (disclose reference atrás de pointer, divida por branch/sequência).
- **No-op** — linha que o modelo já obedece por default. Teste: muda comportamento vs default? Leading word fraca (_seja thorough_ quando já é) é no-op; conserto = palavra mais forte (_relentless_), não outra técnica.

---

## Exemplo

**Input** (description crua, submetida a review):
```
description: "Esta skill ajuda o usuário a escrever testes. Ela é muito útil e
thorough. Use quando precisar de testes, criar testes, gerar testes unitários,
escrever testes, ou testar código."
```

**Diagnóstico** aplicando os princípios:
- "Esta skill ajuda o usuário a escrever testes" → identidade que repete no corpo → cortar.
- "muito útil e thorough" → no-op (o modelo já tenta ser útil) → deletar.
- "criar testes / gerar testes / escrever testes / testar código" → sinônimos do mesmo branch → **duplication**, colapsar em um.
- Falta leading word front-loaded.

**Output** (podado, um trigger por branch, leading word na frente):
```
description: "Write fast, isolated unit tests. Use quando o user pede testes de
uma função nova, ou pede cobertura para código sem testes."
```

---

## Completion
- [ ] Invocação escolhida (model vs user) pelo custo certo (context vs cognitive load)
- [ ] Description front-load leading word, um trigger por branch, sem identidade duplicada do corpo
- [ ] Steps com completion criterion checável; reference disclosed onde incha
- [ ] Podado: single source of truth, relevance, no-ops deletados frase a frase
- [ ] Leading words caçadas onde restatements colapsam

## Relacionado
- Skill `content-design` — front-load de artefato persistido

---

Adaptado de mattpocock/skills (writing-great-skills).
