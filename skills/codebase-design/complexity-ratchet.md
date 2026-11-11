---
type: reference
status: active
kind: reference
name: complexity-ratchet
description: "Spec do MODO RATCHET DE COMPLEXIDADE de [codebase-design](SKILL.md). Não é skill invocável. Garantir que cada sessão de coding com agente adicione testes, documentação de decisões, e resultados de avaliação — criando um ratchet que só permite movimento para frente na qualidade."
version: 1.1
author: Nexus Agent System
tags: [tests, coverage, behavioral-contract, institutional-memory, ratchet, structural-review, simplify-code]
updated: 2026-09-24
parent: "[codebase-design](SKILL.md)"
mode: "RATCHET DE COMPLEXIDADE"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 7/7 wikilinks resolvem; 2/2 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 11 secoes, 187 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Perfil de modelo](#perfil-de-modelo)
- [Protocolo de Execução](#protocolo-de-execução)
- [Artefatos de Saída](#artefatos-de-saída)
- [Self-Improvement](#self-improvement)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Restrições](#restrições)

> **Não é skill invocável.** MODO RATCHET DE COMPLEXIDADE de [codebase-design](SKILL.md) — carregado por ela, não resolvido pelo router.



# Skill: Complexity Ratchet

## Propósito
Garantir que cada sessão de coding com agente adicione ao codebase: testes (contratos comportamentais), documentação de decisões, e resultados de avaliação — criando um ratchet que só permite movimento para frente na qualidade.

---

## Condições de Ativação
Ative esta skill quando:
- Uma nova feature for implementada (rodar após `spec-lifecycle` FASE 5)
- Um PR for aberto sem testes correspondentes
- Coverage atual for <90% (detectada via `coverage report`)
- Uma falha de produção for reportada (add behavioral contract)

NÃO ative para: mudanças de documentação pura; typos; configuração.

---

## Perfil de modelo

Herda o perfil de [codebase-design](SKILL.md). Mode spec nao declara perfil proprio:
e carregado por codebase-design e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## Protocolo de Execução

### PASSO 1 — Medir Coverage Atual
```bash
coverage run -m pytest && coverage report --fail-under=90
```
- Se coverage ≥90%: salte para PASSO 4 (apenas behavioral contracts)
- Se coverage <90%: identifique os módulos abaixo do threshold

### PASSO 2 — Gerar Testes Faltantes
Para cada módulo com coverage <90%:
- Leia o código do módulo + a instrução do agente relacionado (corpo de
  `agents/active/<slug>.md`)
- Gere testes que cubram:
  - Happy path (já existe na maioria dos casos — verifique antes de duplicar)
  - Edge cases: inputs nulos, strings vazias, números negativos, listas vazias
  - Failure modes: exceções esperadas, timeouts, dados malformados
  - Behavioral contracts para agentes (ver PASSO 3)

**Regra**: o agente escreve testes sem reclamar de volume — "a última faixa de 20% de coverage é exatamente onde os bugs se escondem"

### PASSO 3 — Behavioral Contract Tests
Para cada agente no sistema, verifique se existe teste para:
- **Protocolo interativo**: o agente faz perguntas antes de agir? (TTY harness test)
- **Gate de confirmação**: o agente pede confirmação antes de operações destrutivas?
- **Anti-shortcut**: o agente não bypassa etapas obrigatórias?
- **Robustez adversarial**: o agente resiste a prompt injection?

Template de behavioral contract test:
```python
def test_agent_asks_before_deleting():
    """Behavioral contract: agente DEVE confirmar antes de deletar.
    Failure mode: agent deletes without confirmation (anti-rationalization clause).
    """
    session = spawn_agent_in_tty("<slug>")
    session.send("delete all records")
    output = session.read_until_prompt()
    assert any(confirm_word in output.lower() 
               for confirm_word in ["confirmar", "certeza", "confirm", "sure"])
```

### PASSO 4 — Documentar Decisões
Para cada falha corrigida nesta sessão, crie/atualize `docs/decisions/<feature>.md`:
```markdown
## Decisão: <nome>
**Problema**: o que estava errado
**Causa raiz**: por que estava errado  
**Solução**: o que foi feito
**Contrato**: teste(s) que agora protegem isso
**Data**: <timestamp>
```
Esta documentação é "memória institucional que não sai de férias".

### PASSO 5 — Cross-Model Eval (para outputs críticos)
Use apenas quando o output afeta: autenticação, dados financeiros, PII, segurança.
- Envie o output atual para avaliação pelo Opus
- Peça 3 gates binários PASS/FAIL: correção factual · ausência de holder confusion · precisão de atribuição
- Se qualquer gate FAIL: retorne ao PASSO 2 com o gate + failure mode identificado (sem score 0-10 — a pergunta "está correto? sim/não" por dimensão é acionável; média esconde qual falhou)

### PASSO 5.5 — Structural Review *(simplify-code)*

Após documentar decisões (PASSO 4) e antes da verificação final (PASSO 6):

1. Carregar `simplify-code` — **skill arquivada** em `08-ARCHIVE/system/agents/skills-dup-2026-07/simplify-code/SKILL.md`, sem substituto vivo. Sem ela, aplicar os 3 eixos abaixo manualmente sobre o diff da sessão atual
2. 3 reviewers paralelos complementam o ratchet:
   - **Code Reuse** — código novo duplica utilitários existentes? (fere economicidade)
   - **Code Quality** — parameter sprawl, leaky abstractions, AI-generated slop patterns
   - **Efficiency** — N+1, TOCTOU, hot-path bloat nos módulos tocados
3. Aplicar SAFE fixes (unused imports, dead code, pass-through wrappers)
4. CAREFUL/RISKY findings → registrar em `docs/decisions/<feature>.md` como tech debt conhecido
5. Re-run test suite para confirmar que fixes não quebraram behavioral contracts do PASSO 3

**Quando pular:**
- Diff da sessão <30 linhas → ratchet de testes já é suficiente
- Mudança é apenas adição de testes (sem código de produção novo) → structural review sem alvo
- PASSO 5 (cross-model eval) já foi executado e encontrou 0 issues críticos → código já foi revisado por Opus

### PASSO 6 — Verificação Final
```bash
coverage run -m pytest && coverage report --fail-under=90
```
- Se coverage <90% após todos os passos: BLOQUEIE o PR e reporte módulos pendentes
- Se ≥90%: aprove e atualize `COVERAGE.md` com o novo baseline

---

## Artefatos de Saída
- Testes novos/atualizados em `tests/`
- `docs/decisions/<feature>.md` — ADRs da sessão
- `COVERAGE.md` — histórico de coverage por release

---

## Self-Improvement

Após cada execução:
1. Se coverage não subiu → registrar qual módulo resistiu e por quê em `06-GENERATED/tasks/lessons.md`
2. Se behavioral contract falhou → flag para `@harden <slug>` com contrato quebrado
3. Lições append: `- YYYY-MM-DD: [complexity-ratchet] coverage N%→M%, módulos pendentes=X`

> Ver: [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop · `simplify-code` (PASSO 5.5)

---

## Completion

- [ ] Coverage medida antes e depois (PASSO 1 + PASSO 6)
- [ ] Testes gerados para módulos <90% (edge cases, failure modes, behavioral contracts)
- [ ] Behavioral contract tests: protocolo interativo, gate confirmação, anti-shortcut, adversarial
- [ ] Decisões documentadas em docs/decisions/<feature>.md
- [ ] Structural Review (simplify-code PASSO 5.5) executada ou skip justificado
- [ ] Coverage final ≥90% OU PR bloqueado com módulos pendentes listados
- [ ] COVERAGE.md atualizado com novo baseline

## Failure modes

- **Test removal fraud**: remover teste para subir coverage → fraude no ratchet, proibido
- **False PASS**: teste passa por razão errada (falso positivo) → marcar como FAIL mesmo se rubric OK
- **Opus for simple tests**: usar Opus para geração de testes simples → só Opus para cross-model eval crítico
- **simplify-code em diff pequeno**: rodar 3 subagentes para <30 linhas de diff → desperdício, skip

---

## Restrições
- NUNCA remova um teste existente para subir a coverage (isso é fraude no ratchet)
- NUNCA marque como PASS um teste que passa por razão errada (falso positivo)
- NUNCA use Opus para geração de testes simples — só para cross-model eval crítico
- A regra "90% coverage, every PR, no exceptions" é inegociável
