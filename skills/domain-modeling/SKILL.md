---
origin: native
kind: skill-proc
resolver-status: exposed
skill: domain-modeling
version: 1.0
trigger: "/domain-modeling · @domain · 'fixar glossário' · 'registrar ADR' · 'ubiquitous language'"
source: mattpocock/skills (domain-modeling)

id: "domain-modeling"
name: "domain-modeling"
title: "Skill: Domain Modeling"
type: "skill"
created: "2026-07-02"
status: "active"
updated: "2026-07-29"
tags: ["domain", "ubiquitous-language", "glossary", "adr", "context-md", "ddd"]
owner: "nexus"
description: "Use when: corrigir terminologia · resolver linguagem/terms de domínio ambígua · modelar conceitos antes do código. NÃO é destino primário de decisões arquiteturais — isso é core/decisions."
invocation: "both"
triggers:
  positive:
    - "fix domain terminology"
    - "record a justified architectural decision"
    - "resolve fuzzy domain language"
    - "write or edit a GLOSSARY.md directly"
  negative:
    - "consume an existing glossary"
    - "implementation-only task"
    - "mechanical rename"
route:
  profile: "deep"
  risk: "medium"
consumes: []
reads: ["domain-terms", "code-context", "architectural-decision"]
writes: []
tools: []
references: []
verifier: ["Require each fuzzy term to resolve to one canonical term and each ADR to satisfy its three-criteria gate."]
human_gate: false
reviewed-scope: "checagem mecanica + semantica: 4/4 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 8 secoes, 160 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---


# Skill: Domain Modeling

Construir e afiar **ativamente** o modelo de domínio enquanto se desenha. Disciplina *ativa* — desafiar termos, inventar cenários de borda, escrever glossário e decisões no instante em que cristalizam.

> Apenas *ler* `GLOSSARY.md` para vocabulário **não é** esta skill — isso é hábito de uma linha que qualquer skill faz. Esta skill é p/ quando você **muda** o modelo, não só consome.

---

## Quando NÃO usar

- **Registrar decisão arquitetural (ADR/ledger)** → `meta/decisions` — modelar termos não publica decisão; este não é o destino primário.
- **Vocabulário já estável no GLOSSARY.md** — remodelar sem mudança de requisito é dívida.
- **Projeto sem lógica de domínio** (CRUD puro, scripts) — modelar CRUD é cerimônia.
- **Sessão de implementação direta** — modelar antes de entender o problema real; não durante.
- **Protótipo throwaway** — sem persistência do domínio, modelagem não paga.

Disambiguation: `domain-modeling` afia o modelo de domínio (ubiquitous language); `codebase-design` desenha interfaces; `ubiquitous-language` extrai glossário DDD — modeling é o processo, glossary é o artefato.


## Condições de Ativação
Ative quando:
- Fixar terminologia de domínio / ubiquitous language
- Registrar decisão arquitetural (ADR)
- Grilling/design revela termo fuzzy ou decisão que precisa persistir
- Outra skill (`grill-me`, `codebase-design`, `to-spec`) precisa manter o modelo

NÃO ative para: só consumir vocabulário existente (hábito de 1 linha); implementação; edição mecânica.

---

## Estrutura de Arquivos
Maioria dos repos = contexto único:
```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Se existe `GLOSSARY-MAP.md` na raiz → repo tem **múltiplos contextos**. O mapa aponta onde cada um vive:
```
/
├── GLOSSARY-MAP.md
├── docs/adr/                    ← decisões system-wide
├── src/ordering/
│   ├── GLOSSARY.md
│   └── docs/adr/                ← decisões do contexto
└── src/billing/
    ├── GLOSSARY.md
    └── docs/adr/
```

Repo com `CONTEXT.md`/`CONTEXT-MAP.md` (convenção anterior ao upstream v1.3.1): proponha `git mv` para `GLOSSARY.md`/`GLOSSARY-MAP.md` — as skills só procuram o nome novo.

Criar arquivos **lazy** — só quando há algo p/ escrever. Sem `GLOSSARY.md`? Crie ao resolver o 1º termo. Sem `docs/adr/`? Crie ao precisar do 1º ADR.

---

## Durante a Sessão

### Desafiar contra o glossário
Termo do usuário conflita com a linguagem em `GLOSSARY.md` → aponte na hora. "Teu glossário define 'cancelamento' como X, mas parece que você quer dizer Y — qual é?"

### Afiar linguagem fuzzy
Termo vago/sobrecarregado → proponha termo canônico preciso. "Você diz 'account' — é Customer ou User? São coisas diferentes."

### Discutir cenários concretos
Relação de domínio em discussão → estresse com cenário específico que sonda bordas e força precisão sobre os limites entre conceitos.

### Cruzar com o código
Usuário afirma como algo funciona → cheque se o código concorda. Contradição → exponha. "Teu código cancela Orders inteiras, mas você disse que cancelamento parcial é possível — qual é o certo?"

### Atualizar GLOSSARY.md inline
Termo resolvido → atualize `GLOSSARY.md` ali mesmo. Não batche — capture na hora.

> **`GLOSSARY.md` é glossário e NADA MAIS.** Totalmente livre de detalhe de implementação. Não é spec, não é scratch pad, não é repositório de decisão de implementação.

### Oferecer ADR com parcimônia
Só ofereça ADR quando os **três** forem verdade:
1. **Difícil de reverter** — mudar de ideia depois custa caro
2. **Surpreendente sem contexto** — leitor futuro vai perguntar "por que fizeram assim?"
3. **Resultado de trade-off real** — havia alternativas genuínas e escolheu uma por razões específicas

Falta qualquer um dos três → pule o ADR.

Formato ADR (via `/decisions`):
```
## ADR-<n>: [título]
**Contexto:** [problema]
**Decisão:** [o que foi decidido]
**Consequências:** [trade-offs aceitos]
```

---

## Completion
- [ ] Termos fuzzy desafiados e canonizados
- [ ] `GLOSSARY.md` atualizado inline (não batchado), só glossário
- [ ] Contradições código-vs-fala expostas
- [ ] ADR só quando passa nos 3 critérios
- [ ] Multi-contexto: `GLOSSARY-MAP.md` aponta cada `GLOSSARY.md`

## Failure modes
- **GLOSSARY.md poluído**: detalhe de implementação/spec no glossário → só termos
- **Batch de termos**: acumular termos p/ escrever depois → capturar inline, evaporam
- **ADR barato**: registrar decisão trivial/reversível → gasta 3-critérios
- **Termo fuzzy aceito**: "account" não desafiado → propor canônico na hora

---

## Relacionado
- [grill-me](../grill-me/SKILL.md) — grilling alimenta doc capture aqui
- [codebase-design](../codebase-design/SKILL.md) — design usa o vocabulário de domínio
- [decisions](../decisions/SKILL.md) — formato/registro de ADR
- [prd-grade](../spec-lifecycle/prd-grade.md) — PRD usa o glossário de domínio
