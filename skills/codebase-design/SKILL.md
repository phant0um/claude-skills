---
origin: native
kind: skill-proc
resolver-status: exposed
skill: codebase-design
version: 1.0
trigger: "/codebase-design · @design [módulo] · 'onde colocar o seam' · 'deixar testável'"
source: mattpocock/skills (codebase-design)

id: "codebase-design"
name: "codebase-design"
title: "Skill: Codebase Design"
type: "skill"
created: "2026-07-02"
status: "active"
updated: 2026-08-09
tags: ["design", "deep-modules", "seam", "interface", "testability", "ousterhout", "feathers"]
owner: "nexus"
description: "Use when: desenhar interface de módulo profundo · escolher seam de módulo · melhorar testabilidade pela interface pública. Deep-module design card; shrink interfaces, place seams only where variation exists, and preserve testability through the public interface."
invocation: "both"
triggers:
  positive:
    - "design a deep module interface"
    - "choose a module seam"
    - "improve interface-level testability"
  negative:
    - "formatting-only change"
    - "rename-only change"
    - "mechanical edit"
route:
  profile: "deep"
  risk: "medium"
consumes: []
reads: ["module", "interface", "adapters", "tests"]
writes: []
tools: []
references: []
verifier: ["Apply the deletion and depth tests; require seam justification, at least two adapters for variation, and interface-level tests."]
human_gate: false
consolidated-by: R3 (absorveu improve-codebase-architecture, complexity-ratchet como modos)
reviewed-scope: "checagem mecanica + semantica: 7/7 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 12 secoes, 181 linhas; drift R13/R14: 1 achados resolvidos (decisoes D1-D4 A / SKILL_REF)"
reviewed-by: R15 (claude-sonnet; decisoes D1-D4 A)
reviewed: 2026-10-04
---


# Skill: Codebase Design

Desenhar **deep modules**: muito comportamento atrás de interface pequena, num seam limpo, testável pela interface. Usar esta linguagem onde código for desenhado ou reestruturado. Alvo: leverage para callers, locality para maintainers, testability para todos.

---

## Quando NÃO usar

- **Formatting-only / rename-only / edição mecânica** — sem variação de design, skill não aplica.
- **Módulo já estável com interface testada** — redesign é dívida; só com necessidade real.
- **Bug fix pontual** — corrigir; design é para desenho novo ou refactor deliberado.
- **Sessão de spike/protótipo** — protótipo é throwaway; não desenhar módulo profundo.

Disambiguation: `codebase-design` desenha interfaces de módulos profundos; `domain-modeling` constrói o vocabulário de domínio (GLOSSARY.md); `complexity-ratchet` impede aumento de complexidade — design precede código, ratchet acompanha.


## Condições de Ativação
Ative quando:
- Desenhar ou melhorar a interface de um módulo
- Decidir onde colocar um seam
- Tornar código mais testável ou navegável por IA
- Outra skill (`grill-me`) precisar do vocabulário deep-module

NÃO ative para: edições mecânicas sem decisão de design; renomear; formatação.

---

## Glossário
Usar estes termos **exatamente** — não substituir por "component", "service", "API", "boundary". Linguagem consistente é o ponto inteiro.

- **Module** — qualquer coisa com interface + implementação. Escala-agnóstico de propósito: função, classe, pacote, ou slice que atravessa camadas. *Evitar:* unit, component, service.
- **Interface** — tudo que um caller precisa saber p/ usar o módulo corretamente: assinatura de tipo, mas também invariantes, ordem, modos de erro, config exigida, características de performance. *Evitar:* API, signature (estreito demais — só a superfície de tipo).
- **Implementation** — o que está dentro do módulo. Distinta de **Adapter**: pode-se ter adapter pequeno com implementação grande (repo Postgres) ou adapter grande com implementação pequena (fake in-memory).
- **Depth** — leverage na interface: quanto comportamento um caller (ou teste) exercita por unidade de interface que precisa aprender. **Deep** = muito comportamento atrás de interface pequena. **Shallow** = interface quase tão complexa quanto a implementação.
- **Seam** *(Michael Feathers)* — lugar onde se altera comportamento sem editar naquele lugar; a *localização* da interface. Onde pôr o seam é decisão de design própria, distinta do que vai atrás dele. *Evitar:* boundary (colide com bounded context do DDD).
- **Adapter** — coisa concreta que satisfaz uma interface num seam. Descreve *papel* (que slot preenche), não substância.
- **Leverage** — o que callers ganham da depth: mais capacidade por unidade de interface aprendida. Uma implementação paga em N call sites e M testes.
- **Locality** — o que maintainers ganham da depth: mudança, bugs, conhecimento e verificação concentram num lugar. Conserta uma vez, consertado em todo lugar.

---

## Deep vs Shallow

**Deep** = interface pequena + muita implementação (buscar):
```
┌─────────────────────┐
│  Interface Pequena  │  ← poucos métodos, params simples
├─────────────────────┤
│ Implementação Deep  │  ← lógica complexa escondida
└─────────────────────┘
```

**Shallow** = interface grande + pouca implementação (evitar):
```
┌─────────────────────────────────┐
│      Interface Grande           │  ← muitos métodos, params complexos
├─────────────────────────────────┤
│  Implementação Fina (pass-through)
└─────────────────────────────────┘
```

Ao desenhar interface, perguntar:
- Dá p/ reduzir número de métodos?
- Dá p/ simplificar os params?
- Dá p/ esconder mais complexidade dentro?

---

## Princípios
- **Depth é propriedade da interface, não da implementação.** Módulo deep pode ser internamente composto de partes pequenas, mockáveis — elas só não fazem parte da interface. Módulo pode ter **seams internos** (privados, usados pelos próprios testes) além do **seam externo** na interface.
- **Deletion test.** Imagine deletar o módulo. Se a complexidade some, era pass-through. Se reaparece espalhada por N callers, estava ganhando o pão.
- **A interface é a superfície de teste.** Callers e testes cruzam o mesmo seam. Se quer testar *além* da interface, o módulo tem forma errada.
- **Um adapter = seam hipotético. Dois adapters = seam real.** Não introduza seam a menos que algo de fato varie através dele.

---

## Desenhar para Testabilidade
1. **Aceite dependências, não crie-as.**
   ```typescript
   function processOrder(order, paymentGateway) {}   // testável
   function processOrder(order) { const g = new StripeGateway(); }  // difícil
   ```
2. **Retorne resultados, não efeitos colaterais.**
   ```typescript
   function calculateDiscount(cart): Discount {}       // testável
   function applyDiscount(cart): void { cart.total -= d; }  // difícil
   ```
3. **Superfície pequena.** Menos métodos = menos testes. Menos params = setup mais simples.

---

## Relações
- Um **Module** tem exatamente uma **Interface**.
- **Depth** é propriedade do **Module**, medida contra a **Interface**.
- Um **Seam** é onde a **Interface** do **Module** vive.
- Um **Adapter** senta num **Seam** e satisfaz a **Interface**.
- **Depth** produz **Leverage** (callers) + **Locality** (maintainers).

---

## Framings Rejeitados
- **Depth como razão linhas-impl / linhas-interface** (Ousterhout): premia inchar a implementação. Usamos depth-as-leverage.
- **"Interface" como keyword `interface` do TS / métodos públicos**: estreito demais — interface aqui inclui todo fato que o caller precisa saber.
- **"Boundary"**: colide com bounded context do DDD. Diga **seam** ou **interface**.

---

## Completion
- [ ] Termos usados exatamente (Module/Interface/Depth/Seam/Adapter/Leverage/Locality)
- [ ] Interface avaliada por depth (deletion test aplicado)
- [ ] Seam só introduzido onde algo varia (≥2 adapters)
- [ ] Testabilidade: dependências injetadas, resultados retornados, superfície pequena

## Failure modes
- **Shallow module**: interface quase tão complexa quanto impl → esconder mais dentro
- **Seam especulativo**: seam com 1 adapter só → adiar até 2º adapter existir
- **Vocabulário substituído**: dizer "service/component/boundary" → quebra a linguagem compartilhada
- **Testar além da interface**: precisa furar a interface p/ testar → módulo tem forma errada

---

## Relacionado
- [domain-modeling](../domain-modeling/SKILL.md) — vocabulário de domínio (glossário/ADR); design usa a mesma linguagem
- [prd-grade](../spec-lifecycle/prd-grade.md) — esboça seams de teste antes de fatiar PRD
- [spec-lifecycle](../spec-lifecycle/SKILL.md) — vertical slice corta seams
- [tdd](../tdd/SKILL.md) — testa pela interface, no seam
- [grill-me](../grill-me/SKILL.md) — grilling usa deep-module para desafiar design


## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO MELHORAR ARQUITETURA EXISTENTE** — [improve-codebase-architecture](improve-codebase-architecture.md)
- **MODO RATCHET DE COMPLEXIDADE** — [complexity-ratchet](complexity-ratchet.md)
