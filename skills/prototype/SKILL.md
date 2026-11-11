---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: prototype
description: "Build a throwaway prototype to flesh out a design — terminal app for state/logic questions, or UI variants for look questions. Use when answering a design question cheaply."
skill: prototype
version: 1.0
author: Nexus Agent System
source: mattpocock/skills (prototype)
trigger: ['/prototype', '@prototype']
effort: low
tags: [prototype, throwaway, design, logic, ui, terminal, variants]
updated: 2026-07-06
reads: []
writes:
  - 06-GENERATED/tasks/lessons.md
triggers:
  positive:
    - "protótipo throwaway para validar design"
    - "app terminal para state/logic"
    - "variantes de UI para look"
  negative:
    - "código de produção"
    - "spike com spec definida (implement)"

reviewed-scope: "checagem mecanica + semantica: 6/6 wikilinks resolvem; 2/2 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 10 secoes, 160 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
# Skill: Prototype

## Propósito

Protótipo é **throwaway code que responde uma pergunta**. A pergunta decide a forma.

> **Leading word: throwaway.** Protótipo não é produção. É código que responde uma pergunta e depois é deletado ou absorvido.

---

## Quando NÃO usar

- **Solução com requisito claro e caminho conhecido** — implementar; protótipo é para dúvida de design.
- **Protótipo que vira produção sem rewrite** — protótipo é throwaway; promovê-lo acumula dívida.
- **Falta de pergunta a responder** — sem questão de design, protótipo é trabalho desperdiçado.
- **Tempo real de usuário envolvido** (piloto externo) — protótipo interno; piloto é produto mínimo.

Disambiguation: `prototype` responde pergunta de design (throwaway); `spike` valida abordagem técnica (experimento) — `spike` não existe, use `prototype` para throwaway; `implement` constrói com PRD — protótipo destrói depois.


## Condições de Ativação

Ative quando:
- User precisa responder uma pergunta de design barato antes de commit
- "Does this logic/state model feel right?" → LOGIC branch
- "What should this look like?" → UI branch
- Antes de implementar feature complexa sem clareza

NÃO ative para: features já especificadas (→ /implement); hotfixes; refactors.

---

## Pick a Branch

Identificar a pergunta. Se ambíguo e user indisponível: defaultar para a branch
que melhor matcha o código adjacente (backend → LOGIC; page/component → UI), e
declarar a suposição no topo.

### Branch LOGIC — *"Does this logic / state model feel right?"*

**Forma:** terminal app, não UI — o modelo de estado é o objeto de estudo.
Entrada JSON/CLI mínima, saída em prints ou JSON. Sem framework: stdlib ou lib
mínima de estado.

**Validar:** (1) o modelo comporta os casos que o design promete? (2) as
transições são exaustivas — todo input tem handler? (3) os invariantes se mantêm
sob sequências adversas de eventos? (4) a complexidade do modelo justifica o ganho?

**Done:** a pergunta de design tem resposta (sim/não/condicional); o protótipo
roda de ponta a ponta no cenário mínimo; decisão registrada — adotar, descartar,
ou iterar (com o que mudaria).

### Branch UI — *"What should this look like?"*

**Forma:** 2–3 variantes de interface (HTML/mockup leve), nunca uma tela só.
Mesmo conteúdo, layouts/tons diferentes para comparação honesta. Zero backend:
dados fixos inline.

**Validar:** (1) a hierarquia visual comunica a prioridade do conteúdo? (2) o
fluxo principal cabe em uma tela sem scroll crítico? (3) as variantes resolvem o
mesmo problema de formas genuinamente diferentes? (4) qual variante o usuário
prefere **e por quê** — não "qual é mais bonita"?

**Done:** comparação feita com o usuário, preferência registrada com motivo;
variante vencedora identificada (ou decisão de iterar); protótipo descartado ou
absorvido — nunca vira produção por inércia.

Em qualquer das duas: se o experimento revelou padrão reutilizável, registrar a
lição em `06-GENERATED/tasks/lessons.md`.

---

## Rules que aplicam a ambos

1. **Throwaway from day one.** Código próximo de onde será usado, mas nomeado como prototype.
2. **One command to run.** Task runner existente (pnpm, python, bun, etc).
3. **No persistence by default.** State em memória. DB só se a pergunta envolve DB (scratch DB com nome "PROTOTYPE — wipe me").
4. **Skip the polish.** Sem testes, sem error handling além do runnable, sem abstrações.
5. **Surface the state.** Após cada action (logic) ou variant switch (UI), print/render full relevant state.
6. **Delete or absorb when done.** Resposta capturada → delete prototype ou fold na real code.

---

## Completion

- [ ] Branch identificada (LOGIC ou UI)
- [ ] Pergunta explicitamente escrita no topo do prototype
- [ ] 1 comando para rodar
- [ ] State surfaced após cada action/switch
- [ ] Resposta capturada (commit message, ADR, NOTES.md, ou conversa)
- [ ] Prototype deletado ou absorvido na real code

## Failure modes

- **Production prototype**: adicionar testes, error handling, abstrações → prototype não é produção
- **DB wiring**: conectar DB real sem ser scratch → persistence é o que se está testando, não depender disso
- **Generalise**: "what if we wanted X later" → prototype responde 1 pergunta, não é genérico
- **Logic/TUI blur**: logic referencing console.log para control flow → logic deve ser pure, TUI imports logic
- **No answer captured**: protótipo respondeu mas resposta não foi registrada → capturar antes de deletar

---

## Self-Improvement

Após cada execução:
1. Se protótipo não respondeu a pergunta → registrar por quê em `06-GENERATED/tasks/lessons.md`
2. Se protótipo virou produção (não foi deletado) → flag para revisão
3. Lições append: `- YYYY-MM-DD: [prototype] branch=X, pergunta=Y, resposta=Z`

> Ver: [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop

---

## Restrições

- NUNCA adicione testes ao protótipo
- NUNCA wire DB real (use in-memory ou scratch)
- NUNCA generalize além da pergunta
- NUNCA deixe protótipo rotting no repo — delete ou absorva

---

## Relacionado

- [spec-lifecycle](../spec-lifecycle/SKILL.md) — spec antes de implementar; prototype antes de spec
- [tdd](../tdd/SKILL.md) — TDD durante implementação, não protótipo
- [implement](../implement/SKILL.md) — implementação após prototype validar design
- matt-pocock-skills-14-analysis — fonte original