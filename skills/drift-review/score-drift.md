---
type: reference
status: active
kind: reference
name: score-drift
description: "Spec do MODO ALVO = IDENTIDADE/SCORE de [drift-review](SKILL.md). Não é skill invocável. Measures drift as binary gate flips (OK/DRIFTED) across 5 dimensions — no "
version: 2.0
tags: [quality, drift, agents, monitoring, binary]
updated: 2026-08-09
parent: "[drift-review](SKILL.md)"
mode: "ALVO = IDENTIDADE/SCORE"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 9/9 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 11 secoes, 194 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Perfil de modelo](#perfil-de-modelo)
- [Dimensões de Avaliação](#dimensões-de-avaliação)
- [Protocolo](#protocolo)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Restrições](#restrições)
- [Relacionado](#relacionado)

> **Não é skill invocável.** MODO ALVO = IDENTIDADE/SCORE de [drift-review](SKILL.md) — carregado por ela, não resolvido pelo router.



# Skill: Score-Drift

## Propósito

Medir o drift semântico de um agente entre sua identidade declarada e seu comportamento observado via **gates binários** (OK/DRIFTED por dimensão — sem score 0-10, que é opaco e cria falsa precisão). Alimenta `hill` com diagnóstico mais preciso do que "parece ter drifted": nomeia qual gate flipou. Modelo herdado do gate-flip binário de `audit-agentes-mensal` (sim→não = degradação), agente retirado em 2026-08-09 — a mecânica sobreviveu, o agente não. Ver binary-eval-statistics.

**Diferença de `drift-review`:** drift-review varre todo o repo para drift de docs/config (binário: drifted/not). `score-drift` mede um agente específico em profundidade — 5 gates por dimensão + histórico de flips.

**Diferença de `hill`:** hill melhora. score-drift mede antes de melhorar (input para hill, não substituto).

---

## Condições de Ativação

Ative quando:
- Comportamento de agente parece inconsistente mas não claramente errado
- Antes de `@harden <agente>` para quantificar o problema
- Após série de sessões com agente crítico (guard, nexus, verify) — manutenção preventiva
- `@review` reportou drift mas não quantificou

NÃO ative para: agente recém-criado sem histórico de sessões; drift de docs/config do vault (→ drift-review).

---

## Perfil de modelo

Herda o perfil de [drift-review](SKILL.md). Mode spec nao declara perfil proprio:
e carregado por drift-review e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## Dimensões de Avaliação

Cada dimensão é um **gate binário: OK** (comportamento bate com o declarado) ou **DRIFTED** (≥1 desvio observado com evidência). Sem meio-termo — a pergunta "houve desvio?" é sim/não. D1 e D4 são **gates críticos** (identidade e restrições).

| Dimensão | Gate (pergunta binária) | Evidência a coletar |
|----------|-------------------------|---------------------|
| **D1 — Identidade** ⚠️ | Agente agiu FORA da identidade declarada? | Comparar seção "Identidade" com comportamento nos últimos outputs observados |
| **D2 — Escopo** | Agente saiu do "Fora do Escopo"? | Casos onde agente saiu do escopo declarado |
| **D3 — Modelo** | Agente usou modelo errado por fase? | Comparar `model_tier` declarado vs comportamento real |
| **D4 — Restrições** ⚠️ | Agente violou alguma "Restrição" explícita? | Cada restrição da seção → foi violada alguma vez? |
| **D5 — Formato** | Output divergiu do formato declarado? | Comparar formato esperado vs outputs reais |

> ⚠️ = gate crítico: se DRIFTED, escalar direto para `@trace` antes de `@harden`.

---

## Protocolo

### 1. Ler Agent File

Ler `04-SYSTEM/automation/procedures/core/<slug>.md`. Extrair:
- Identidade declarada (seção "Identidade")
- Restrições explícitas
- Fora do escopo
- Model tier
- Formato de relatório/output

### 2. Coletar Evidência de Comportamento

Fontes de evidência (usar o que estiver disponível):
```bash
# Commits relacionados ao agente
git log --oneline --all --grep="<slug>" -- 04-SYSTEM/automation/agents/

# Outputs gerados pelo agente
ls -t 06-GENERATED/ | head -20

# Errors log
grep -i "<slug>" 04-SYSTEM/system/logs/errors.md 2>/dev/null | tail -10

# Hot cache (sessões recentes)
grep -A3 "<slug>" 04-SYSTEM/system/state/context/hot.md 2>/dev/null
```

Se não houver evidência suficiente: score com base apenas na análise estática do agent file (consistência interna).

### 3. Gate Check por Dimensão

Para cada dimensão D1–D5:

```
Gate: [OK | DRIFTED]
Evidência: [citação ou observação concreta — obrigatória p/ DRIFTED]
```

Sem evidência concreta → não pode marcar DRIFTED (evita falso positivo). Análise estática do agent file conta como evidência de consistência interna.

### 4. Comparar com histórico (flips)

Se houver medição anterior no hot.md, comparar gate a gate:
```
Flip OK→DRIFTED  = degradação nova (a que mais importa)
Flip DRIFTED→OK  = recuperação
Sem flip         = estável
```
Sem número composto — o sinal é *quais* gates fliparam, não uma média. (Média esconde flip: 4 OK + 1 DRIFTED "parece bom" mas o 1 pode ser D4=Restrições.)

### 5. Output

```
SCORE-DRIFT: <slug> v<versão> | <data>

D1 — Identidade ⚠️:  [OK | DRIFTED]
D2 — Escopo:         [OK | DRIFTED]
D3 — Modelo:         [OK | DRIFTED]
D4 — Restrições ⚠️:  [OK | DRIFTED]
D5 — Formato:        [OK | DRIFTED]

GATES DRIFTED: [N/5]  | Flips vs anterior: [lista OK→DRIFTED / "primeira medição"]

DIMENSÕES DRIFTED:
  [lista com evidência e localização no agent file]

RECOMENDAÇÃO (por gate, não por média):
  0 gates DRIFTED:        agente estável — próxima medição em 30 dias
  D1 ou D4 DRIFTED:       DRIFT CRÍTICO — acionar "@trace <slug>" antes de hill
  ≥1 gate (não-crítico):  acionar "@harden <slug>" com este relatório

PRÓXIMO PASSO: [ação específica baseada nos gates flipados]
```

### 6. Atualizar hot.md *(só se ≥1 gate DRIFTED)*

```markdown
## Score-Drift <slug> | <data> | [N]/5 gates DRIFTED
Gates DRIFTED: [D* list] (flips: [OK→DRIFTED list]) → "@harden <slug>" ou "@trace" se D1/D4
```

---

## Completion

- [ ] Gate OK/DRIFTED emitido por dimensão (todas as 5)
- [ ] Todo DRIFTED tem evidência concreta citada
- [ ] Se D1 ou D4 DRIFTED: escalado para Sonnet/trace
- [ ] Se não houver histórico: declarado "análise estática apenas"
- [ ] Output: gate card + dimensões DRIFTED + flips vs anterior + recomendação hill/trace

## Failure modes

- **Invented evidence**: marcar DRIFTED sem evidência → sem evidência concreta, gate fica OK (ou "análise estática apenas")
- **Reintroduzir score numérico**: emitir 0-10 ou média composta → o modelo é gate binário OK/DRIFTED; média esconde flip crítico
- **D4 underestimate**: tratar D4 (Restrições) DRIFTED como não-crítico → D1/D4 DRIFTED sempre escalam para trace

---

## Restrições

- NUNCA inventar evidência — se não houver histórico, declarar "análise estática apenas"
- NUNCA reintroduzir score 0-10 ou composto — cada dimensão é gate binário OK/DRIFTED
- NUNCA marcar DRIFTED sem evidência concreta citada
- Se D1 (Identidade) ou D4 (Restrições) DRIFTED: escalar para Sonnet/trace mesmo que os outros estejam OK

---

## Relacionado

- hill-mode — consome este score como input inicial
- [trace](../diagnose/trace.md) — investiga causas específicas quando score-drift identifica dimensão crítica
- [drift-review](SKILL.md) — drift de docs/repo (diferente de drift de comportamento de agente)
