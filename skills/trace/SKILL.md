---
name: trace
description: "Spec do MODO ALVO = OUTPUT DE AGENTE de `diagnose`. Não é skill invocável. @trace [descrição do output inesperado] — Reverse-engineer por que um agente produziu um output inesperado. Identificar qual parte do agent file (identidade, restrições, modelo, tools) habilitou ou causou o com"
trigger: "@trace [descrição do output inesperado]" | "/trace [agente] [comportamento]" | "trace this agent" | "why did the agent do X" | "root-cause this behavior"
---
> **Não é skill invocável.** MODO ALVO = OUTPUT DE AGENTE de `diagnose` — carregado por ela, não resolvido pelo router.




# Skill: Trace

## Propósito

Reverse-engineer por que um agente produziu um output inesperado. Identificar qual parte do agent file (identidade, restrições, modelo, tools) habilitou ou causou o comportamento — para que hill corrija cirurgicamente.

**Diferença de guard:** guard audita por vulnerabilidades de segurança. `trace` diagnostica comportamento inesperado (pode ser seguro mas errado).

**Diferença de hill:** hill melhora iterativamente. `trace` encontra a causa-raiz antes de qualquer mudança.

---

## Condições de Ativação

Ative quando:
- Agente produziu output que viola sua identidade declarada
- Agente recusou tarefa que deveria aceitar (ou aceitou o que deveria recusar)
- Agente usou modelo errado para a fase
- Comportamento inconsistente entre runs similares
- Antes de `@harden` quando o problema é específico (não generalizado)

NÃO ative para: avaliação geral de qualidade (→ hill); audit de segurança (→ guard); validação pós-implementação (→ verify).

---

## Perfil de modelo

Herda o perfil de `diagnose`. Mode spec nao declara perfil proprio:
e carregado por diagnose e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## Protocolo

### 1. Coletar Contexto

Extrair da descrição do usuário:
- **Output inesperado:** o que o agente fez (exato, não parafrasear)
- **Output esperado:** o que deveria ter feito
- **Input que gerou:** o prompt/trigger que ativou o agente
- **Agente:** slug + versão (do frontmatter)

Se faltarem informações: fazer 1 pergunta por lacuna. Não prosseguir sem output + esperado + input.

### 2. Ler Agent File

Ler `<agent-file>.md` completo. Mapear:
- Identidade declarada (o que o agente diz que é)
- Restrições explícitas (seção "Restrições")
- Tools declaradas (frontmatter `tools`)
- Modelo tier (frontmatter `model_tier`)
- Triggers e condições de ativação
- Fora do escopo

### 3. Reconstruir Cadeia Causal

Percorrer o agent file tentando reproduzir o raciocínio que levou ao output inesperado:

```
Hipótese 1: [qual seção do agent file poderia ter causado isso]
  → Evidência: [citação exata da linha/seção]
  → Como levou ao output: [mecanismo]

Hipótese 2: [lacuna — o que o agent file NÃO diz que deveria dizer]
  → Evidência: ausência de restrição X
  → Como levou ao output: agente sem guardrail para esse caso

Hipótese 3: [ambiguidade — instrução que poderia ser interpretada de dois jeitos]
  → Evidência: [citação]
  → Interpretação problemática: [qual leitura levou ao output]
```

Rankear hipóteses por probabilidade (mais provável primeiro).

### 4. Diagnóstico Final

```
TRACE REPORT: <slug> v<versão>

Input: [input que causou o problema]
Output inesperado: [o que aconteceu]
Output esperado: [o que deveria ter acontecido]

CAUSA-RAIZ MAIS PROVÁVEL:
  Tipo: [LACUNA / AMBIGUIDADE / CONFLITO / MODELO_ERRADO / SCOPE_CREEP]
  Localização: <seção do agent file>:<linha aproximada>
  Mecanismo: [como essa parte do arquivo habilitou o comportamento]

CAUSAS SECUNDÁRIAS (se houver):
  [lista]

CORREÇÃO SUGERIDA:
  Arquivo: <agent-file>.md
  Seção: <nome da seção>
  Mudança: [texto exato a adicionar/modificar — mínimo necessário]
  Justificativa: [por que essa mudança específica resolve sem efeitos colaterais]

PRÓXIMO PASSO: "@harden <slug>" com esta análise como contexto inicial
```

---

## Completion

- [ ] TRACE REPORT entregue com: input, output inesperado, output esperado, causa-raiz, correção sugerida
- [ ] Pelo menos 2 hipóteses listadas e rankeadas por probabilidade
- [ ] Correção sugerida é mínima (1-3 linhas), sem reescrita do agent file
- [ ] Localização exata: seção + linha aproximada do agent file

## Failure modes

- **"Causa desconhecida"**: trace conclui sem hipóteses → sempre listar mínimo 2, mesmo se low-probability
- **Reescrita sugerida**: correção excede 3 linhas → hill não aplica rewrites, apenas edits cirúrgicos
- **Skip da cadeia causal**: trace pula direto para correção sem reconstruir como o agent file habilitou o comportamento → sem diagnóstico, hill não tem contexto para aplicar

---

## Restrições

- NUNCA aplicar a correção sugerida diretamente — apenas diagnosticar (hill aplica)
- NUNCA concluir "causa desconhecida" sem listar pelo menos 2 hipóteses
- NUNCA sugerir reescrita do agent file — correção deve ser mínima (1-3 linhas)
- Se o problema for reproduzível apenas com contexto específico: documentar as condições exatas

---

## Relacionado

- hill-mode — consome o diagnóstico do trace para aplicar correção
- guard — security traces seguem caminho diferente (OWASP LLM checklist)
- probe — probe gera casos, trace investiga casos que já falharam
- `diagnose` — trace é para agentes (reverse-engineer do agent file); diagnose é para código/sistema geral (debugging loop disciplinado)
