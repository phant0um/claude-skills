---
type: reference
status: active
kind: reference
name: heavy-think
version: 1.0
author: Nexus Agent System
tags: [reasoning, parallel, deliberation, complex, stem]
updated: 2026-08-09
description: "Spec do MODO HEAVY-THINK (1 perspectiva, profundidade) de [council](SKILL.md). Não é skill invocável."
parent: 04-SYSTEM/automation/skills/reasoning/council/SKILL.md
mode: "HEAVY-THINK (1 perspectiva, profundidade)"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 5/5 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 9 secoes, 138 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Perfil de modelo](#perfil-de-modelo)
- [Protocolo de Execução](#protocolo-de-execução)
- [Artefatos de Saída](#artefatos-de-saída)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Restrições## Restrições](#restrições-restrições)

> **Não é skill invocável.** MODO HEAVY-THINK (1 perspectiva, profundidade) de [council](SKILL.md) — carregado por ela, não resolvido pelo router.




# Skill: Heavy Think

## Propósito
Resolver problemas de alta complexidade através de raciocínio paralelo multi-trajetória seguido de deliberação sequencial. Aplicável quando uma única passagem de inferência é insuficiente.

---

## Condições de Ativação
Ative esta skill quando a tarefa envolver:
- Raciocínio multi-step com >3 decisões interdependentes
- Arquitetura de sistema com trade-offs não óbvios
- Debugging de falhas que resistiram a 2+ tentativas diretas
- Análise estratégica com múltiplos cenários futuros
- Qualquer pergunta onde "errar caro muito" (segurança, dados críticos)

NÃO ative para: queries factuais diretas; tarefas de rotina; formatação; perguntas conversacionais; escolhas entre duas opções com trade-off real (→ use [debate](debate.md) em vez disso).

**Heavy-think vs Debate:**
- `heavy-think` = problema bem definido, precisa de múltiplas trajetórias para chegar à solução certa
- `debate` = decisão entre A vs B com trade-off real, precisa de confronto estruturado

---

## Perfil de modelo

Herda o perfil de [council](SKILL.md). Mode spec nao declara perfil proprio:
e carregado por council e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## Protocolo de Execução

### ETAPA 1 — Classificação do Problema
Antes de spawnar trajetórias, classifique:
- **Tipo**: STEM-verificável | Código | Design/Arquitetura | Estratégia | Análise
- **Complexidade**: Alta (K=8) | Média (K=4) | [se Média, considere skill mais simples]
- **Verificabilidade**: Resposta binária verificável | Julgamento subjetivo

Se o tipo for "Análise Estratégica" e a resposta for preferencial (não verificável), alerte: "Heavy Think é mais eficaz em problemas com resposta objetiva. Continuar?"

### ETAPA 2 — Parallel Reasoning *(K×Sonnet em paralelo)*
- Spawne K sub-agentes Sonnet **sem acesso às saídas dos outros**
- Instrua cada sub-agente a adotar uma estratégia diferente:
  - Agente 1: abordagem bottom-up
  - Agente 2: abordagem top-down
  - Agente 3: abordagem por analogia/pattern-matching
  - Agente 4: abordagem adversarial (tente refutar a solução óbvia)
  - (Se K=8: repita com variações de cada estratégia)
- Cada agente produz: `{reasoning_chain, conclusion, confidence_0_to_1}`

### ETAPA 3 — Memory Cache (serialização)
- Colete todas as K saídas
- Descarte thinking interno, mantenha apenas: reasoning_chain + conclusion
- **Shuffle** a ordem para evitar position bias no deliberador
- Serialize como: `Thinker [i]: <reasoning> → Conclusão: <conclusion> (confiança: <X>)`

### ETAPA 4 — Sequential Deliberation
Instrução para o deliberador:
```
Você recebe K raciocínios paralelos sobre o mesmo problema.
SUA TAREFA:
1. Classifique o tipo de problema (determina profundidade de análise)
2. Avalie CRITICAMENTE cada raciocínio — não siga a maioria automaticamente
3. Identifique: concordâncias robustas, contradições importantes, insights únicos
4. Se todos os thinkers estiverem errados, re-derive a resposta do zero
5. Sintetize uma resposta final que integre os melhores insights
PROIBIDO: concatenar superficialmente as respostas; ignorar thinkers minoritários sem justificativa
FORMATO: apenas a resposta final + justificativa — sem meta-análise visível ao usuário
```

### ETAPA 5 — Iterative Deliberation
- Se a confiança da deliberação for <0.7: adicione a saída do ETAPA 4 ao memory cache e execute mais 1 round de deliberação
- Máximo 2 iterações adicionais (N=3 total)
- **Atenção ao trade-off**: iterações melhoram HMean mas degradam HPass — pare se a melhoria incremental for <0.05

---

## Artefatos de Saída
- Resposta final sintetizada (sem exposição das trajetórias ao usuário)
- `heavy-think-log_<timestamp>.json` para auditoria (opcional, apenas se solicitado)

---

## Completion

- [ ] 3 trajetórias independentes geradas (Expert, Beginner, adversarial/edge-case)
- [ ] Score HMean ≥ 0.7 OU ETAPA 5 executada (max 3 rounds total)
- [ ] Resposta final sintetizada (trajetórias internas não expostas ao usuário)
- [ ] Se score < 0.7 após 3 rounds: reportar incerteza, não forçar resposta

## Failure modes

- **Trajectory exposure**: mostrar trajetórias internas ao usuário → apenas síntese final é visível
- **Max-length bias**: selecionar trajetória mais longa como melhor → Max-Length é a estratégia pior
- **N=4+ iterations**: executar além de 3 rounds → ganho não compensa custo, noise aumenta
- **Trivial activation**: usar heavy-think para problema que Nexus resolve em <30s → desperdício

---

## Restrições## Restrições
- NUNCA exponha as trajetórias internas ao usuário — apenas a síntese final
- NUNCA selecione a trajetória mais longa como melhor (Max-Length é a estratégia pior)
- NUNCA execute iteração N=4+ — o ganho não compensa o custo e o noise aumenta
- Se o problema puder ser resolvido por Nexus diretamente em <30s, NÃO ative esta skill
