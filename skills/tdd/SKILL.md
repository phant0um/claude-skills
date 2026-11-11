---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: tdd
description: "Use when: pedido de escrever o teste antes do código, ou de feature/bugfix com teste, tipo 'escreve o teste primeiro', 'faz TDD/red-green disso', 'adiciona teste pra essa função', 'corrige esse bug e cria o teste que pegava ele'. Dispara mesmo com código ou diff colado, sem o usuário dizer 'TDD'. Poda de suíte existente é test-audit; bug sem causa é diagnose."
skill: tdd
version: 1.1
author: Nexus Agent System
source: mattpocock/skills (tdd + tests.md + mocking.md — merge R1 2026-08-09)
trigger: ['/tdd', '@tdd', 'red-green-refactor', 'test-first']
effort: low
tags: [testing, tdd, red-green-refactor, tracer-bullet, vertical-slices]
updated: 2026-09-28
reads: []
writes:
  - 06-GENERATED/tasks/lessons.md
triggers:
  positive:
    - "/tdd"
    - "@tdd"
    - "red-green-refactor"
    - "test-first"
    - "feature nova com interface definida"
    - "fix de bug que deveria ter teste"
    - "adicione testes a esta função: <def>"
  negative:
    - "config pura"
    - "migration sem lógica"
    - "protótipo throwaway"
    - "bug trivial sem comportamento observável"
consumes: ["seam-agreement", "test-framework"]
tools: []
references:
  - 04-SYSTEM/automation/skills/meta/spec-lifecycle/SKILL.md
  - 04-SYSTEM/automation/skills/dev/codebase-design/complexity-ratchet
  - 04-SYSTEM/automation/skills/meta/spec-lifecycle/spec-verify
verifier: ["Require red test escrito em seam pré-acordado antes do código e green após."]
human_gate: true
reviewed-scope: "checagem mecanica + semantica: 8/8 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 15 secoes, 280 linhas; drift R12: 3 achados resolvidos (A/B/F)"
reviewed-by: R13 (claude-sonnet; drift R12 corrigido)
reviewed: 2026-10-04
---


# Skill: TDD

## Propósito

Desenvolvimento test-first com vertical slices (tracer bullets). Cada teste é uma slice end-to-end que corta todas as camadas — não horizontal slices de uma camada só.

---

## Condições de Ativação

Ao explorar o codebase, ler `GLOSSARY.md` (se existir) para que nomes de teste e vocabulário
de interface batam com a linguagem de domínio do projeto, e respeitar ADRs da área tocada.

---

## Seams — onde o teste mora

**Seam** é o boundary público onde você observa behavior sem alcançar o interior. Teste mora
em seam, nunca contra internals.

**Só teste em seam pré-acordado.** Antes de escrever qualquer teste, escreva quais seams
entram no escopo e confirme com o user. Nenhum teste é escrito em seam não confirmado.

Não dá para testar tudo — acordar os seams na frente é o que faz o esforço cair em caminho
crítico e lógica complexa em vez de cada edge case.

Pergunta de abertura: "qual é a interface pública, e quais seams a gente testa?"

---

## Anti-Pattern: Horizontal Slices

**NÃO escreva todos testes primeiro, depois toda implementação.** Isso é "horizontal slicing" — tratar RED como "escrever todos testes" e GREEN como "escrever todo código."

Produz **crap tests**:
- Testes em bulk testam behavior imaginado, não atual
- Testam shape de coisas (data structures, signatures) não behavior user-facing
- Testes ficam insensíveis a mudanças reais — passam quando behavior quebra
- Você ultrapassa seus headlights, commitando estrutura de teste antes de entender a implementação

**Correto**: Vertical slices via tracer bullets. 1 teste → 1 implementação → repeat.

```
ERRADO (horizontal):
  RED: test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

CORRETO (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

---

## Protocolo

### 1. Planning

Antes de escrever código:
- [ ] Confirmar com user quais mudanças de interface são necessárias
- [ ] Confirmar quais behaviors testar (priorizar)
- [ ] Identificar oportunidades para deep modules (interface pequena, implementação profunda)
- [ ] Listar behaviors a testar (não steps de implementação)
- [ ] Aprovação do user no plano

### 2. Tracer Bullet

Escreva 1 teste que confirma 1 coisa:

```
RED: Escreve teste para primeiro behavior → teste falha
GREEN: Escreve código mínimo para passar → teste passa
```

Este é o tracer bullet — prova que o path funciona end-to-end.

### 3. Incremental Loop

Para cada behavior restante:

```
RED: Escreve próximo teste → falha
GREEN: Código mínimo para passar → passa
```

Regras:
- 1 teste por vez
- Apenas código suficiente para passar o teste atual
- Não antecipar testes futuros
- Testes focados em behavior observável

### 4. Refactor — **fora do loop** (Pocock v1.1)

Refactor estrutural **saiu do loop TDD** e vive depois da implementação (`code-optimize` para refactor 5E, `/code-review` para o diff), para não sobrecarregar a sessão de implementação com preocupações de refactoring. No loop, só **tidy verde** trivial (rename local, remover dead line) enquanto GREEN.

Refactor real — extrair duplicação, deepen modules, aplicar SOLID, code smells (Fowler) — é feito por [code-optimize](../code-optimize/SKILL.md) após a implementação, antes do commit.

---

## Checklist por ciclo

```
[ ] Teste descreve behavior, não implementação
[ ] Teste usa apenas interface pública
[ ] Teste sobreviveria a refactor interno
[ ] Código é mínimo para este teste
[ ] Sem features especulativas
```

---

## Authoring gate

Antes de adicionar ou mudar um teste, responda as 4 perguntas. Resposta
faltando = não adicione ainda.

1. Que comportamento observável, invariante ou contrato independente ele protege?
2. Que regressão crível faz ele falhar?
3. Por que a cobertura existente não pega essa falha? Cada contrato tem um
   único teste dono na fronteira mais forte; outra camada precisa de risco
   próprio (falha de transporte ou ciclo de vida que o dono não alcança).
   Prefira estender um caso de tabela ou fixture compartilhada a um teste
   quase duplicado.
4. Ele exige um seam de produção (export, flag, wrapper, hook de injeção) que
   nenhum caller de produção usa? Se sim, mova o teste para a fronteira real.

Fixture de formato externo é captura real da ferramenta: README com versão, comando de recaptura e digest; o teste nunca reescreve a golden. Gate ou lint novo leva tabela valid/invalid; o valid inclui caso de mesmo nome com outro tipo, alias ou sombreamento.

Depois confira contra os
[junk patterns](../test-audit/SKILL.md#junk-patterns).
Bater em um reprova, salvo se a retention bar da mesma skill nomear o contrato
que ele guarda sozinho.

Teste de regressão tem que falhar no código pré-fix pelo motivo certo e passar
depois do conserto no dono. Regressão que nunca falhou prova o mock, não o fix.
Uma regressão na fronteira do dono cobre o bug; não repita o cenário em cada
camada que ele atravessa.

Fonte: openclaw/openclaw `test-audit` (2026-09-28).

---

## Completion

- [ ] Plano aprovado pelo user (behaviors priorizados)
- [ ] Tracer bullet executado (1 teste → 1 impl → pass)
- [ ] Loop incremental completo (todos behaviors cobertos)
- [ ] Refactor estrutural deferido p/ /code-review (só tidy verde trivial no loop)
- [ ] Suite completa passa
- [ ] Zero features especulativas adicionadas

## Failure modes

- **Tautológico**: o valor esperado é recomputado do mesmo jeito que o código computa
  (`expect(add(a,b)).toBe(a+b)`, snapshot derivado à mão pelo mesmo caminho, constante
  comparada consigo mesma) → passa por construção, nunca discorda do código. Valor esperado
  vem de fonte independente: literal conhecido, exemplo trabalhado, a spec.
- **Seam não acordado**: teste escrito em boundary que o user não confirmou → esforço em
  edge case enquanto caminho crítico fica descoberto

---

## Good vs Bad Tests

**Good**: integration-style, exercita code paths reais via API pública. Lê como especificação: "user can checkout with valid cart".

**Bad**: coupled a implementação. Mocka internals, testa private methods, verifica via DB query em vez de interface. Sinal: teste quebra em refactor sem behavior change.

Exemplos de código bom vs ruim: se precisar calibrar um teste com exemplo concreto, leia [exemplos-bom-ruim](references/exemplos-bom-ruim.md).

Recurso com close ou rollback: injete falha no próprio cleanup; afirme erro primário mantido, mesmo dono retentado e trabalho novo recusado; registre o cleanup antes da ação.

Red flags: mockar collaborator interno · testar private method · asserir call count/ordem ·
teste quebra em refactor sem behavior change · nome descreve COMO, não O QUÊ · verificação
por fora da interface.

---

## Mocking

Mock apenas em **system boundaries**:
- APIs externas (payment, email)
- Databases (preferir test DB)
- Time/randomness
- Filesystem (às vezes)

NÃO mock:
- Suas próprias classes/módulos
- Collaborators internos
- Qualquer coisa que você controla

### Desenhar para mockabilidade

se precisar desenhar dependência injetável ou SDK mockável, leia [desenhar-mockabilidade](references/desenhar-mockabilidade.md).

---

## Self-Improvement

Após cada execução:
1. Se teste quebra em refactor sem behavior change → registrar padrão de implementation-detail test em `06-GENERATED/tasks/lessons.md`
2. Se horizontal slicing detectado → flag para @harden com contexto
3. Lições append: `- YYYY-MM-DD: [tdd] N tracer bullets, M refactors, behavior coverage=X%`

> Ver: [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop

---

## Restrições

- NUNCA escrever todos testes antes de toda implementação (horizontal slicing)
- NUNCA testar private methods ou internals
- NUNCA adicionar features especulativas sem teste que exija
- NUNCA refactor enquanto RED
- NUNCA remover, pular ou enfraquecer teste para ficar verde

---

## Quando NÃO usar

- **Config pura, docs, migrations de DB sem lógica, protótipos throwaway** — sem comportamento observável, teste-first não paga.
- **Bug com causa-raiz já confirmada e fix trivial (<10 linhas)** — escrever teste de regressão primeiro; não precisa do ciclo completo.
- **Exploração de código sem feature/fix definido** — TDD exige interface; usar `dev/codebase-design` ou `domain-modeling` antes.
- **Dívida de cobertura em código legado sem seams** — sem seam pré-acordado, vertical slices não encaixam; `complexity-ratchet` complementa depois, não junto.

Disambiguation: `dev/tdd` implementa test-first; `spec-verify` verifica spec contra implementação (depois do fato); `meta/spec-lifecycle` escreve a spec antes — TDD assume spec existente.

## Relacionado

- [complexity-ratchet](../codebase-design/complexity-ratchet.md) — coverage ratchet complementa TDD
- matt-pocock-skills-14-analysis — fonte original
