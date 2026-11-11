---
type: reference
status: active
kind: reference
name: meta-learn
version: 1.0
tags: [learning, principles, feedback, self-improvement, corrections, meta]
source: "agents-need-feedback-loops-not-perfect-prompts"
updated: 2026-08-09
description: "Spec do MODO META-LEARN de [evolve](SKILL.md). Não é skill invocável."
parent: "[evolve](SKILL.md)"
mode: "META-LEARN"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 8/8 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 10 secoes, 196 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Modelo por Etapa](#modelo-por-etapa)
- [Protocolo — 7 Steps (Petra Donka)](#protocolo-7-steps-petra-donka)
- [Output](#output)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Restrições](#restrições)
- [Relacionado](#relacionado)

> **Não é skill invocável.** MODO META-LEARN de [evolve](SKILL.md) — carregado por ela, não resolvido pelo router.





# Skill: Meta-Learn

## Propósito

Quando um agente sugere X e o humano faz Y (correção), extrair o **princípio** — não a regra. Regras são frágeis ("nunca mencione preço na primeira frase"); princípios são duráveis ("se alguém está expressando frustração, comece com empatia").

**Diferença de `/evolve`:** evolve captura padrões que *funcionaram* na sessão. meta-learn captura o *gap* entre sugestão do agente e ação humana — onde o agente estava errado ou incompleto.

**Diferença de `hill`:** hill melhora agente via eval iterativo. meta-learn extrai o princípio de uma correção específica para que hill tenha material de qualidade para trabalhar.

---

## Condições de Ativação

Ative quando:
- Usuário corrigiu output de agente e a correção revela um padrão (não um erro pontual)
- Agente sugeriu X, humano fez Y de forma diferente e isso aconteceu ≥2× com padrão similar
- Pós-sessão com múltiplas correções — extrair princípios antes de perder contexto
- `/meta-learn` explícito após qualquer sessão intensa de refinamento

NÃO ative para: erros pontuais sem padrão; preferências estéticas sem impacto de qualidade; correções de fato (→ ingest-verify ou guard).

---

## Modelo por Etapa

| Etapa | Modelo | Razão |
|-------|--------|-------|
| Coleta das correções da sessão | Haiku | Scan estruturado do histórico |
| 7-step extraction por correção | Sonnet | Abstração de regra → princípio |
| Decisão de destino | Sonnet | Julgar onde o princípio pertence |

---

## Protocolo — 7 Steps (Petra Donka)

Para cada correção identificada:

### Step 1 — Identificar o que deu errado (ou certo)
```
Sugestão do agente: [exato]
Ação real do humano: [exato]
Diferença: [o que o humano fez de diferente]
```

### Step 2 — Perguntar: por quê?
```
Por que o agente sugeriu X?
  → Qual parte do agent file ou contexto levou a X?
Por que o humano fez Y?
  → Qual contexto/valor/julgamento tornou Y melhor?
```

### Step 3 — Zoom out para o padrão
```
Isso é um caso específico de: [padrão mais geral]
Outros contextos onde esse padrão aparece: [lista]
```

### Step 4 — Verificar contra princípios existentes
```bash
grep -i "[palavra-chave do padrão]" 04-SYSTEM/automation/procedures/core/*.md 2>/dev/null | head -10
grep -i "[palavra-chave]" CLAUDE.md | head -5
```

Se princípio já existir: o agente violou um princípio existente → problema de enforcement, não de princípio novo. Encaminhar para `hill`.

### Step 5 — Escrever como princípio (não regra)

Regra (frágil): "Nunca faça X."
Princípio (durável): "Quando [contexto], priorize [valor] porque [razão]."

```
RASCUNHO DO PRINCÍPIO:
"Quando [condição que torna o princípio relevante],
[ação ou prioridade],
porque [mecanismo que explica por que isso funciona]."
```

### Step 6 — Decidir destino

| Destino | Quando |
|---------|--------|
| `04-SYSTEM/automation/procedures/core/<slug>.md` seção Restrições | Princípio específico de um agente |
| `CLAUDE.md` — seção Identity ou Preferences | Princípio de comportamento geral do vault |
| `04-SYSTEM/automation/skills/<categoria>/<skill>/SKILL.md` | Princípio de execução de uma skill |
| `04-SYSTEM/system/logs/errors.md` | Erro pontual sem princípio generalizável |

### Step 7 — Editar e commitar

```
PROPOSTA DE PRINCÍPIO:
  Arquivo: [destino]
  Seção: [onde inserir]
  Texto: "[princípio formatado]"
  
  Aplicar? [gate para agent files e CLAUDE.md — não aplicar automaticamente]
```

---

## Output

```
META-LEARN REPORT — [data]

Correções analisadas: N
Princípios extraídos: M
Erros pontuais (→ errors.md): K

PRINCÍPIOS:

[1] [título]
  Arquivo: [destino]
  Princípio: "[texto]"
  Origem: [descrição da correção que gerou isso]
  Gate: [PENDENTE APROVAÇÃO / APLICADO AUTONOMAMENTE se skill]

[2] ...

PRÓXIMO PASSO:
  Princípios para agent files: "@extend <slug>" com estes princípios
  Princípios para CLAUDE.md: apresentar ao usuário para confirmação
```

---

## Completion

- [ ] Correções analisadas e classificadas (padrão vs erro pontual)
- [ ] Padrões passaram Step 3 (zoom out para padrão geral, não caso isolado)
- [ ] Princípios escritos como princípio (condição + ação + razão), não regra ("nunca X")
- [ ] Verificação contra princípios existentes feita (grep em agents/core + CLAUDE.md)
- [ ] Destino decidido por princípio (agent file, CLAUDE.md, skill, ou errors.md)
- [ ] META-LEARN REPORT entregue com princípios + destino + gate status
- [ ] Princípios para agent files/CLAUDE.md: PENDENTE APROVAÇÃO (não auto-aplicado)

## Failure modes

- **Regra em vez de princípio**: "Nunca faça X" sem contexto → rewrite como "Quando [condição], priorize [valor] porque [razão]"
- **Padrão de correção única**: extrair princípio de 1 correção sem verificar recorrência → Step 3 obrigatório, mínimo 2 ocorrências
- **Princípio duplicado**: criar princípio que já existe em CLAUDE.md ou agent file → grep antes, se existe = enforcement problem → encaminhar para hill
- **Auto-aplicar em CLAUDE.md**: aplicar princípio sem confirmação → CLAUDE.md é INVARIANT, sempre gate humano

---

## Restrições

- NUNCA aplicar princípios em `04-SYSTEM/automation/agents/` ou `CLAUDE.md` sem confirmação — apenas em skills
- NUNCA escrever regras ("sempre X", "nunca Y" sem contexto) — princípios têm condição + razão
- NUNCA extrair princípio de correção única sem verificar se é padrão (Step 3 obrigatório)
- Se correção revelar violação de princípio existente: encaminhar para hill, não criar princípio duplicado

---

## Relacionado

- [evolve](SKILL.md) — captura padrões bem-sucedidos da sessão; meta-learn captura gaps de correção
- hill-mode — recebe princípios do meta-learn como levers para aplicar
- [codex-retrospective](codex-retrospective.md) — retrospective temporal; meta-learn é imediato (por correção)
- errors — erros pontuais sem padrão vão aqui, não viram princípios
