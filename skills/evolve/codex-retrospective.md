---
type: reference
status: active
kind: reference
name: codex-retrospective
version: 1.0
created: 2026-05-29
tags: [retrospective, self-improvement, session-review, behavior, vault-improvement]
updated: 2026-08-09
description: "Spec do MODO RETROSPECTIVA DE SESSÃO de [evolve](SKILL.md). Não é skill invocável. @retrospective [N dias] — Revisão do histórico de sessões dos últimos N dias para identificar padrões de comportamento, erros recorrentes, e oportunidades de melhoria. Produz proposta de ajuste cirúrgico (1-3 m"
parent: "[evolve](SKILL.md)"
mode: "RETROSPECTIVA DE SESSÃO"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 8/8 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 8 secoes, 121 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Quando usar](#quando-usar)
- [Protocolo](#protocolo)
- [Output esperado](#output-esperado)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Relacionado## Relacionado](#relacionado-relacionado)

> **Não é skill invocável.** MODO RETROSPECTIVA DE SESSÃO de [evolve](SKILL.md) — carregado por ela, não resolvido pelo router.




# Skill: codex-retrospective

Revisão do histórico de sessões dos últimos N dias para identificar padrões de comportamento, erros recorrentes, e oportunidades de melhoria. Produz proposta de ajuste cirúrgico (1-3 mudanças concretas), não reescrita completa.

## Quando usar

- Após série de erros similares repetidos
- Semanal como manutenção preventiva
- Antes de `@harden` para dar contexto de diagnóstico
- Quando comportamento do vault parece derivar do esperado

## Protocolo

### 1. Coletar histórico
```bash
# Sessões recentes
ls -t ~/.claude/projects/*/sessions/ 2>/dev/null | head -20

# Logs de erros do vault
tail -50 04-SYSTEM/system/logs/errors.md 2>/dev/null

# Commits recentes como proxy de atividade
git log --oneline --since="N days ago" 04-SYSTEM/ 03-RESOURCES/sources/
```

### 2. Analisar padrões

Para cada período revisado, identificar:

| Categoria | Pergunta |
|-----------|---------|
| Erros repetidos | Mesmo tipo de erro ≥2x? |
| Desvios de princípio | Ações fora das guidelines de CLAUDE.md? |
| Fricção recorrente | Mesmo passo manual ≥3x? |
| Gaps de skill | Tarefa sem skill existente ≥2x? |
| Routing incorreto | Modelo errado para tipo de tarefa? |

### 3. Proposta (máx 3 itens)

```markdown
## Retrospectiva [YYYY-MM-DD] — últimos N dias

### Padrão detectado 1
- **O que aconteceu:** <descrição concreta com exemplos>
- **Causa provável:** <diagnóstico>
- **Proposta:** <mudança específica — onde aplicar, o quê mudar>
- **Arquivo alvo:** `<path>`

### Padrão detectado 2
...

### Itens sem mudança proposta
- <observação sem ação necessária>
```

### 4. Gate antes de aplicar

Toda proposta de mudança em `04-SYSTEM/automation/agents/` ou `CLAUDE.md` requer confirmação explícita do usuário antes de aplicar. Esta skill produz a proposta; `@nexus` ou usuário aprova.

Mudanças em `04-SYSTEM/automation/skills/` podem ser aplicadas autonomamente se escopo for cirúrgico (1 arquivo, ≤20 linhas).

## Output esperado

- Máximo 3 padrões identificados
- 1 proposta concreta por padrão
- Nenhuma mudança aplicada sem gate explícito para agents/CLAUDE.md

## Completion

- [ ] Histórico de N dias coletado (sessões, errors.md, commits)
- [ ] 5 categorias analisadas (erros repetidos, desvios de princípio, fricção, gaps de skill, routing)
- [ ] Máximo 3 padrões identificados com descrição concreta + causa provável + proposta
- [ ] Propostas para agents/CLAUDE.md: PENDENTE APROVAÇÃO (não auto-aplicado)
- [ ] Propostas para skills: aplicáveis autonomamente se escopo cirúrgico (1 arquivo, ≤20 linhas)

## Failure modes

- **Pattern inflation**: identificar 5+ padrões → forçar priorização, máximo 3
- **Vague proposal**: "melhorar X" sem arquivo alvo e mudança específica → proposta deve ter path + seção + texto
- **Auto-aplicar em agent files**: aplicar mudança em agents/ sem gate → requer confirmação explícita

---

## Relacionado## Relacionado

- [evolve](SKILL.md) — complementar: retrospective = olha N dias para trás; evolve = captura padrões da sessão ATUAL antes que sumam do contexto. Usar evolve ao fim de sessão intensa, retrospective como manutenção periódica.
- [hill-climb](../hill-climb/SKILL.md) — melhoria de agente específico (hill tem escopo, retrospective tem perspectiva temporal)
- hill-mode — agente que implementa as mudanças propostas
- errors — log de erros que alimenta esta skill
- claude-arsenal-codex-retrospective-skill — inspiração original
