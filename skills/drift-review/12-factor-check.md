---
type: reference
status: active
kind: reference
name: 12-factor-check
version: 1.0
tags: [audit, reliability, production, agents, 12-factor, architecture]
source: "12-factor-agents-humanlayer"
updated: 2026-08-09
description: "Spec do MODO ALVO = 12-FACTOR de [drift-review](SKILL.md). Não é skill invocável. @12-factor [slug] — Auditar um agente contra os 12 princípios de confiabilidade de produção (12-Factor Agents). Diferente de `guard` (segurança OWASP) e `governance-audit` (layers de governança): 12-factor-chec"
parent: "[drift-review](SKILL.md)"
mode: "ALVO = 12-FACTOR"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 10/10 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 10 secoes, 173 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Perfil de modelo](#perfil-de-modelo)
- [Os 12 Fatores (adaptados para vault)](#os-12-fatores-adaptados-para-vault)
- [Protocolo](#protocolo)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Restrições](#restrições)
- [Relacionado](#relacionado)

> **Não é skill invocável.** MODO ALVO = 12-FACTOR de [drift-review](SKILL.md) — carregado por ela, não resolvido pelo router.




# Skill: 12-Factor Check

## Propósito

Auditar um agente contra os 12 princípios de confiabilidade de produção (12-Factor Agents). Diferente de `guard` (segurança OWASP) e `governance-audit` (layers de governança): 12-factor-check avalia se o agente é *arquiteturalmente confiável* — escalável, debugável, testável.

**Princípio base:** As melhores aplicações LLM em produção são majoritariamente código determinístico com LLM nos pontos certos — não loops "bag-of-tools".

---

## Condições de Ativação

Ative quando:
- Novo agente criado (gate pré-deploy)
- Agente vai para uso em produção / alta frequência
- `rotina-audit-mensal` detecta score-drift em agente crítico
- Revisão arquitetural de agente existente

NÃO ative para: skills (não são agentes); rotinas (são workflows, não agentes LLM); análise de segurança (→ guard).

---

## Perfil de modelo

Herda o perfil de [drift-review](SKILL.md). Mode spec não declara perfil próprio:
é carregado por drift-review e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execução.

Resolução canônica em model-routing.

## Os 12 Fatores (adaptados para vault)

| # | Fator | O que verificar |
|---|-------|----------------|
| F1 | **Own your intent translation** | Agente converte linguagem natural em tool calls estruturados? Ou apenas "responde"? |
| F2 | **Own your prompts** | Prompts são literais no agent file (versionáveis)? Ou delegados a framework/template opaco? |
| F3 | **Own your context window** | Agente gerencia o que entra no contexto? Ou injeta tudo sem filtro? |
| F4 | **Tools are structured outputs** | Tools declaradas com schema claro? Execução é código determinístico, não LLM ad-hoc? |
| F5 | **Unify state** | Estado de execução = estado de negócio? Sem estados ocultos fora do agent file? |
| F6 | **Launch/Pause/Resume** | Agente pode ser pausado e retomado sem perda de contexto? |
| F7 | **Human in the loop** | Operações irreversíveis têm HITL gate explícito no agent file? |
| F8 | **Own your control flow** | Grafo de controle explícito no agent file? Ou LLM decide o fluxo livremente? |
| F9 | **Compact errors** | Erros são capturados e compactados no contexto? Sem loops infinitos de retry? |
| F10 | **Small, focused** | Agente faz UMA coisa? Ou tem >10 tools sobrepostas e múltiplos propósitos? |
| F11 | **Trigger from anywhere** | Pode ser ativado via CLI, hook, API e session? |
| F12 | **Stateless reducer** | `(state, event) → new_state + actions`? Estado vem do input, não de memória interna? |

---

## Protocolo

### 1. Ler Agent File

Ler `04-SYSTEM/automation/procedures/core/<slug>.md` completo.

### 2. Gate por Fator

Cada F1–F12 é um **gate binário: PASS | FAIL** (+ N/A quando não aplicável). Sem PARTIAL — "meio satisfeito" vira FAIL com nota do que falta (o meio-termo é a fuzz que o BinEval elimina; force a pergunta binária "o fator está satisfeito? sim/não").

```
Gate: PASS | FAIL | N/A
Evidência: [citação ou observação do agent file — obrigatória p/ FAIL]
```

**N/A válido para:** F6 (run longa — vault-agents raramente pausam), F11 (agentes de vault não precisam de API externa).

**Fatores críticos:** F7 (HITL), F8 (control flow), F10 (focused). FAIL num crítico é **blocking** → não production-ready. FAIL em não-crítico é **non-blocking** → nota, não bloqueia.

### 3. Veredito (sem número)

- **✅ PRODUCTION-READY** — 0 FAIL em fatores aplicáveis (non-blocking notes podem existir)
- **🔴 NOT PRODUCTION-READY** — ≥1 FAIL em fator crítico (F7/F8/F10)
- Se só há FAIL não-crítico: ship com notas → `@extend` oportunístico

### 4. Output

```
12-FACTOR CHECK: <slug> v<versão>

F1  Own intent translation:  PASS/FAIL
F2  Own prompts:             PASS/FAIL
F3  Own context:             PASS/FAIL
F4  Tools structured:        PASS/FAIL
F5  Unified state:           PASS/FAIL
F6  Launch/Pause/Resume:     PASS/FAIL/N/A
F7  Human in the loop ⚠️:    PASS/FAIL
F8  Own control flow ⚠️:     PASS/FAIL
F9  Compact errors:          PASS/FAIL
F10 Small & focused ⚠️:      PASS/FAIL
F11 Trigger from anywhere:   PASS/FAIL/N/A
F12 Stateless reducer:       PASS/FAIL

VEREDITO: ✅ PRODUCTION-READY | 🔴 NOT READY   (FAIL crítico: [N] / FAIL total: [N])

FAIL CRÍTICOS (F7/F8/F10 — blocking):
  [lista com localização no agent file]
FAIL não-crítico (notes):
  [lista]

RECOMENDAÇÃO:
  0 FAIL: OK — próxima revisão em 30d
  FAIL crítico: @spec novo design antes de @extend
  só FAIL não-crítico: @extend oportunístico
```

---

## Completion

- [ ] Todos os 12 fatores avaliados (F1-F12) como gate PASS/FAIL/N/A
- [ ] F7 (HITL) verificado: agente tem seção "Restrições" com confirmação para ops destrutivas
- [ ] F10 (focused) verificado: agente tem ≤10 tools e propósito único
- [ ] Cada FAIL tem evidência citada; FAIL crítico (F7/F8/F10) marcado blocking
- [ ] Veredito emitido: ✅ PRODUCTION-READY (0 FAIL) | 🔴 NOT READY (≥1 FAIL crítico)

## Failure modes

- **F7 false PASS**: dar PASS em F7 sem seção "Restrições" explícita → F7 FAIL = blocking
- **F10 ignore**: não flagar agente com >10 tools → F10 FAIL precisa ser flagado
- **PARTIAL/score numérico**: reintroduzir PARTIAL ou ratio composto → o modelo é gate binário PASS/FAIL; meio-termo vira FAIL com nota
- **FAIL sem classificação**: reportar FAIL sem marcar crítico/não-crítico → define o veredito

---

## Restrições

- F7 (HITL) FAIL = blocking imediato — agente sem HITL em op irreversível não é production-ready
- F10 (focused) FAIL = flag — agente com >10 tools ou múltiplos propósitos precisa ser dividido
- NUNCA reintroduzir PARTIAL ou score composto — cada fator é gate binário PASS/FAIL
- NUNCA dar PASS em F7 se o agent file não tiver seção "Restrições" com confirmação explícita para ops destrutivas

---

## Relacionado

- guard — F7 (HITL) intersecta com LLM08 (Excessive Agency); guard complementa mas não substitui
- [governance-audit](governance-audit.md) — governa *mandato e escopo*; 12-factor-check governa *arquitetura de confiabilidade*
- hill-mode — recebe failing factors como levers específicos para corrigir
- [score-drift](score-drift.md) — score-drift mede drift de comportamento; 12-factor-check mede qualidade arquitetural
