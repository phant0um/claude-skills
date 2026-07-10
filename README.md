# claude-skills

**Skills p/ agentes que precisam ser previsíveis.** Guardrails que o Claude Code carrega sob demanda p/ executar um workflow do mesmo jeito toda vez.

Extraídas de um vault Obsidian que opera como SO de agentes IA. Só as skills **genéricas** (servem fora do vault) vivem aqui.

## Setup em 30s

```
/plugin marketplace add phant0um/claude-skills
/plugin install claude-skills
```

Pronto. As skills carregam sozinhas quando o contexto casa — ou invoca manual com `/nome`.

---

## Os problemas que isto resolve

### O agente escreve muro de texto e enterra o ponto

Pediu um resumo, veio 4 parágrafos de aquecimento antes da conclusão. Toda leitura futura paga o custo de garimpar o ponto.

→ **`content-design`** aplica 5 regras antes de salvar: pirâmide invertida, veredito na linha 1, 1 ideia por frase, concreto sobre vago. Molda o artefato, não o conteúdo.

### O agente não tem taste — e não se autoavalia

Ele *acha* que front-loadeou. Não checou. Sem um segundo passo, o erro passa.

→ **`content-design-review`** é o par validador: audita o texto contra as 5 regras, devolve veredito por linha (localização + fix), não reescreve. Padrão _generate + review_ — uma skill produz, outra reprova.

### O agente decide sozinho e erra caro — sem segunda opinião

Decisão arquitetural, escolha de stack, plano de alto risco. Um só ângulo, blind spots passam.

→ **`council`**, **`debate`**, **`pre-mortem`**, **`office-hours`** forçam múltiplas perspectivas, confronto estruturado, ou hindsight prospectivo ("o plano já morreu — como?") antes de commitar.

### O bug resistiu a 1+ tentativas e o agente segue chutando fix

Sem hipótese confirmada, cada "fix" é aposta. O loop não fecha.

→ **`diagnose`** proíbe fix sem hipótese confirmada: reproduce → minimise → hypothesise → instrument → fix → regression. **`trace`** faz o mesmo p/ output inesperado de agente.

### Skills que não disparam, ou derrapam depois de disparar

→ **`writing-great-skills`** é a referência de vocabulário/princípios p/ escrever SKILL.md previsível. **`grill-me`** e **`doubt-driven-development`** pressionam premissas antes de construir.

---

## Referência

Skills têm dois modos de disparo:

- **Model-invoked** — o Claude aciona sozinho quando o contexto casa (ex: `content-design` ao salvar).
- **User-invoked** — tu chamas com `/nome` (ex: `/council`).

### writing/

| Skill | Modo | Função |
|-------|------|--------|
| [content-design](skills/content-design/SKILL.md) | model | 5 regras front-load p/ artefato persistido |
| [content-design-review](skills/content-design-review/SKILL.md) | user | Validador estrito pareado — veredito por linha |
| [writing-fragments](skills/writing-fragments/SKILL.md) | user | Minerar fragmentos crus, sem estrutura ainda |
| [writing-shape](skills/writing-shape/SKILL.md) | user | Moldar material em artigo, parágrafo a parágrafo |
| [writing-beats](skills/writing-beats/SKILL.md) | user | Montar material numa jornada de beats fundamentados |
| [writing-great-skills](skills/writing-great-skills/SKILL.md) | user | Referência p/ escrever/revisar SKILL.md previsível |

### reasoning/

| Skill | Modo | Função |
|-------|------|--------|
| [council](skills/council/SKILL.md) | user | 5 advisors debatem + revisão cega → veredicto |
| [debate](skills/debate/SKILL.md) | user | Confronto formal 2 perspectivas + arbitragem |
| [pre-mortem](skills/pre-mortem/SKILL.md) | user | Prospective hindsight — "o plano já falhou, como?" |
| [office-hours](skills/office-hours/SKILL.md) | user | 6 forcing-questions estilo YC p/ pressionar ideia |
| [grill-me](skills/grill-me/SKILL.md) | user | Perguntas duras, uma por vez, antes de codar |
| [doubt-driven-development](skills/doubt-driven-development/SKILL.md) | user | Enumera + classifica premissas por risco |
| [diagnose](skills/diagnose/SKILL.md) | user | Loop de debug disciplinado, fix só com hipótese |
| [trace](skills/trace/SKILL.md) | user | Reverse-engineer output inesperado de agente |

Regra de escopo → [CLAUDE.md](CLAUDE.md).

---

## Créditos

Estas skills adaptam padrões públicos. Crédito às fontes:

- **[mattpocock/skills](https://github.com/mattpocock/skills)** — `diagnose` (diagnosing-bugs), `grill-me`, `writing-great-skills`, `writing-fragments`, `writing-shape`, `writing-beats`.
- **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)** — `doubt-driven-development`.
- **Claude Council** (padrão 5-advisor) — `council`.
- **Gary Klein** (prospective hindsight, HBR) + endosso de Daniel Kahneman — `pre-mortem`.
- **Garry Tan / Y Combinator** (office hours) — `office-hours`.

`content-design`, `content-design-review`, `debate` e `trace` são originais deste pack.

---

## Escopo

Skill entra aqui só se **serve fora do vault de origem**. Teste: "outra pessoa, em outro projeto, ganharia?" Sim → entra. Acoplada a domínio (finança/concurso/agente específico) → fica privada.

## Licença

MIT — ver [LICENSE](LICENSE).
