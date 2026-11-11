---
type: reference
status: active
kind: reference
name: improve-codebase-architecture
description: "Spec do MODO MELHORAR ARQUITETURA EXISTENTE de [codebase-design](SKILL.md). Não é skill invocável. Escaneia um codebase por deepening opportunities (refactors que tornam módulos shallow em deep), apresenta como relatório, depois grilla o candidato escolhido. Informado pelo modelo de domínio + vocabulário de design com"
version: 1.0
tags: [architecture, deepening, refactor, deep-modules, testability, review]
source: mattpocock/skills (improve-codebase-architecture)
updated: 2026-08-09
parent: "[codebase-design](SKILL.md)"
mode: "MELHORAR ARQUITETURA EXISTENTE"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 10/10 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 7 secoes, 121 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Condições de Ativação](#condições-de-ativação)
- [Perfil de modelo](#perfil-de-modelo)
- [Processo](#processo)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Relacionado](#relacionado)

> **Não é skill invocável.** MODO MELHORAR ARQUITETURA EXISTENTE de [codebase-design](SKILL.md) — carregado por ela, não resolvido pelo router.



# Skill: Improve Codebase Architecture

Aflorar fricção arquitetural e propor **deepening opportunities** — refactors que transformam módulos shallow em deep. Alvo: testabilidade e navegabilidade por IA.

Construído sobre vocabulário compartilhado:
- Aplique [codebase-design](SKILL.md) p/ o vocabulário (**module, interface, depth, seam, adapter, leverage, locality**) + princípios (deletion test, "interface é a superfície de teste", "1 adapter = seam hipotético, 2 = real"). Use os termos **exatamente** — não derive p/ "component/service/API/boundary".
- A linguagem de domínio em `GLOSSARY.md` dá nome aos bons seams; ADRs em `docs/adr/` registram decisões que este comando **não** deve re-litigar.

---

## Condições de Ativação
Ative quando:
- User quer auditar arquitetura de projeto-dev existente
- Procurar onde deixar código mais testável/navegável
- `/improve-arch` chamado

NÃO ative para: código novo (→ `codebase-design` no design); bug (→ `diagnose`); micro-refactor óbvio.

---

## Perfil de modelo

Herda o perfil de [codebase-design](SKILL.md). Mode spec nao declara perfil proprio:
e carregado por codebase-design e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## Processo

### 1. Explore
Leia `GLOSSARY.md` (glossário) + ADRs da área primeiro. Depois use a **Agent tool `subagent_type=Explore`** p/ caminhar o codebase. Sem heurística rígida — explore organicamente e anote fricção:
- Onde entender um conceito exige pular entre muitos módulos pequenos?
- Onde módulos são **shallow** — interface quase tão complexa quanto a implementação?
- Onde funções puras foram extraídas só p/ testabilidade, mas os bugs reais moram em COMO são chamadas (sem **locality**)?
- Onde módulos acoplados vazam pelos seams?
- Que partes são não-testadas, ou difíceis de testar pela interface atual?

Aplique o **deletion test** ao que suspeita ser shallow: deletar concentraria complexidade, ou só a moveria? "Concentra" = o sinal que você quer.

### 2. Apresentar candidatos — relatório Markdown
> Adaptação vault: **relatório Markdown**, não HTML (HTML = ~3× tokens; ver decisão de formato). Escreva em `06-GENERATED/arch-review-<timestamp>.md`. Nada entra no repo do projeto.

Para cada candidato, um card:
- **Arquivos** — quais módulos envolvidos
- **Problema** — por que a arquitetura atual causa fricção
- **Solução** — inglês/PT simples do que mudaria
- **Benefícios** — em termos de **locality** e **leverage**, e como os testes melhoram
- **Before / After** — diagrama ASCII/mermaid lado a lado (shallow → deepened)
- **Força da recomendação** — badge: `Forte` · `Vale explorar` · `Especulativo`

Termine com **Top recommendation**: qual atacar primeiro e por quê.

Use vocabulário de `GLOSSARY.md` p/ domínio + `codebase-design` p/ arquitetura. Se `GLOSSARY.md` define "Order", fale "módulo de intake de Order" — não "FooBarHandler", nem "Order service".

**Conflito com ADR:** se candidato contradiz ADR existente, só aflore quando a fricção é real o bastante p/ reabrir o ADR. Marque claro (callout: _"contradiz ADR-0007 — mas vale reabrir porque…"_). Não liste todo refactor teórico que um ADR proíbe.

**NÃO proponha interfaces ainda.** Após escrever o arquivo, pergunte: "Qual desses quer explorar?"

### 3. Grilling loop
User escolhe candidato → rode `/grill-me` (grilling) p/ caminhar a árvore de design: constraints, dependências, forma do módulo deepened, o que fica atrás do seam, quais testes sobrevivem.

Side effects inline conforme decisões cristalizam — rode `/domain-modeling` p/ manter o modelo atual:
- **Nomear módulo deepened com conceito fora do `GLOSSARY.md`?** Adicione o termo (lazy-create se não existe).
- **Afiar termo fuzzy na conversa?** Atualize `GLOSSARY.md` ali.
- **User rejeita candidato com razão load-bearing?** Ofereça ADR: _"Registro como ADR p/ futuras reviews não re-sugerirem?"_ Só quando a razão seria necessária a um explorador futuro — pule razões efêmeras/óbvias.
- **Explorar interfaces alternativas?** Use o padrão design-it-twice (sub-agentes paralelos) do `codebase-design`.

---

## Completion
- [ ] `GLOSSARY.md` + ADRs lidos antes de explorar
- [ ] Codebase varrido via subagente Explore; fricção anotada
- [ ] Deletion test aplicado aos suspeitos shallow
- [ ] Relatório MD em 06-GENERATED com cards + top recommendation
- [ ] Interfaces NÃO propostas até user escolher
- [ ] Grilling loop no candidato escolhido; domain-modeling inline

## Failure modes
- **Vocabulário derivado**: "service/component" em vez de module/seam → quebra linguagem
- **Propor interface cedo**: desenhar antes do user escolher → só apresentar candidatos
- **Relatório no repo**: arquivo no projeto → sempre 06-GENERATED
- **Re-litigar ADR**: sugerir o que ADR já decidiu → só se fricção justifica reabrir

---

## Relacionado
- [codebase-design](SKILL.md) — vocabulário deep-module (dependência dura)
- [domain-modeling](../domain-modeling/SKILL.md) — mantém GLOSSARY.md/ADR durante o loop
- [grill-me](../grill-me/SKILL.md) — grilling do candidato escolhido
- [code-optimize](../code-optimize/SKILL.md) — review de código pós-refactor
