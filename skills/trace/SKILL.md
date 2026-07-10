---
name: trace
description: Reverse-engineer por que um agente produziu um output inesperado — identifica qual parte do agent file (identidade, restrições, modelo, tools) causou o comportamento e propõe correção cirúrgica.
trigger: "@trace [descrição do output inesperado]" | "/trace [agente] [comportamento]" | "trace this agent" | "why did the agent do X" | "root-cause this behavior"
---

# Skill: Trace

## Propósito

Reverse-engineer por que um agente produziu um output inesperado. Identificar qual parte do agent file (identidade, restrições, modelo, tools) habilitou ou causou o comportamento — para que a correção seja cirúrgica.

**Escopo:** `trace` diagnostica comportamento inesperado (pode ser seguro mas errado), diferente de uma auditoria de segurança. E `trace` encontra a causa-raiz *antes* de qualquer mudança — não é o passo que aplica a correção iterativamente.

---

## Condições de Ativação

Ative quando:
- Agente produziu output que viola sua identidade declarada
- Agente recusou tarefa que deveria aceitar (ou aceitou o que deveria recusar)
- Agente usou modelo errado para a fase
- Comportamento inconsistente entre runs similares
- Antes de aplicar uma correção, quando o problema é específico (não generalizado)

NÃO ative para: avaliação geral de qualidade; auditoria de segurança; validação pós-implementação.

---

## Modelo por Etapa

| Etapa | Modelo | Razão |
|-------|--------|-------|
| Coleta de contexto do output | Haiku | Estruturação mecânica |
| Leitura e análise do agent file | Sonnet | Identificação de ambiguidade e lacunas |
| Reconstrução da cadeia causal | Sonnet | Raciocínio de causa-raiz |
| Diagnóstico + recomendação cirúrgica | Sonnet | Proposta de correção mínima |

---

## Protocolo

### 1. Coletar Contexto *(Haiku)*

Extrair da descrição do usuário:
- **Output inesperado:** o que o agente fez (exato, não parafrasear)
- **Output esperado:** o que deveria ter feito
- **Input que gerou:** o prompt/trigger que ativou o agente
- **Agente:** slug + versão (do frontmatter)

Se faltarem informações: fazer 1 pergunta por lacuna. Não prosseguir sem output + esperado + input.

### 2. Ler Agent File *(Sonnet)*

Ler o arquivo de definição do agente por completo. Mapear:
- Identidade declarada (o que o agente diz que é)
- Restrições explícitas (seção "Restrições")
- Tools declaradas (frontmatter `tools`)
- Modelo tier (frontmatter `model_tier`)
- Triggers e condições de ativação
- Fora do escopo

### 3. Reconstruir Cadeia Causal *(Sonnet)*

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

### 4. Diagnóstico Final *(Sonnet)*

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
  Arquivo: <caminho do agent file>
  Seção: <nome da seção>
  Mudança: [texto exato a adicionar/modificar — mínimo necessário]
  Justificativa: [por que essa mudança específica resolve sem efeitos colaterais]

PRÓXIMO PASSO: aplicar a correção com esta análise como contexto inicial
```

---

## Exemplo

**Input:** "O agente `summarizer` recebeu um artigo de 3 páginas e devolveu o texto quase inteiro em vez de um resumo curto."

**Trace:**

```
TRACE REPORT: summarizer v1.2

Input: artigo de 3 páginas + "resuma isto"
Output inesperado: ~90% do texto original reproduzido
Output esperado: resumo de 3-5 bullets

CAUSA-RAIZ MAIS PROVÁVEL:
  Tipo: LACUNA
  Localização: seção "Protocolo":linha ~20
  Mecanismo: o protocolo diz "preserve os pontos-chave" mas nunca define
  um limite de tamanho de saída — sem teto, o modelo minimiza perda de
  informação reproduzindo quase tudo.

CAUSAS SECUNDÁRIAS:
  Ambiguidade em "pontos-chave" (nenhum critério de seleção).

CORREÇÃO SUGERIDA:
  Seção: Protocolo
  Mudança: adicionar "Saída máxima: 5 bullets ou 120 palavras."
  Justificativa: teto explícito força seleção sem tocar no resto do agente.
```

---

## Completion

- [ ] TRACE REPORT entregue com: input, output inesperado, output esperado, causa-raiz, correção sugerida
- [ ] Pelo menos 2 hipóteses listadas e rankeadas por probabilidade
- [ ] Correção sugerida é mínima (1-3 linhas), sem reescrita do agent file
- [ ] Localização exata: seção + linha aproximada do agent file

## Failure modes

- **"Causa desconhecida"**: trace conclui sem hipóteses → sempre listar mínimo 2, mesmo se low-probability
- **Reescrita sugerida**: correção excede 3 linhas → correções são edits cirúrgicos, não rewrites
- **Skip da cadeia causal**: trace pula direto para correção sem reconstruir como o agent file habilitou o comportamento → sem diagnóstico, quem aplica não tem contexto

---

## Restrições

- NUNCA aplicar a correção sugerida diretamente — apenas diagnosticar
- NUNCA concluir "causa desconhecida" sem listar pelo menos 2 hipóteses
- NUNCA sugerir reescrita do agent file — correção deve ser mínima (1-3 linhas)
- Se o problema for reproduzível apenas com contexto específico: documentar as condições exatas

---

## Relacionado

- Um passo de melhoria iterativa consome o diagnóstico do trace para aplicar a correção.
- Traces de segurança seguem caminho diferente (checklist OWASP LLM).
- Geração de casos de teste é upstream: gera casos; trace investiga casos que já falharam.
- Ver skill `diagnose` — trace é para agentes (reverse-engineer do agent file); diagnose é para código/sistema geral (debugging loop disciplinado).
