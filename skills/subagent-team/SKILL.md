---
origin: native
kind: skill-proc
resolver-status: exposed
skill: subagent-team
version: 1.2
author: Nexus Agent System

id: "subagent-team"
name: "subagent-team"
title: "Skill: Subagent Team"
type: "skill"
created: "2026-06-19"
status: "active"
updated: 2026-09-25
tags: ["orchestration", "parallel", "team", "researcher", "editor", "pm", "analyst"]
owner: "nexus"
description: "Use when: @team <task> · trabalho paralelo em mais de dois domínios independentes. Parallel orchestration card; decompose multi-domain work, brief specialists, consolidate outputs, and audit completion. MODO BRIEF: destilar a sessão em campos de TaskPacket antes de delegar."
invocation: "both"
triggers:
  positive:
    - "@team <task>"
    - "parallel work across more than two independent domains"
    - "destilar contexto da sessão antes de delegar a subagente"
  negative:
    - "strictly sequential dependency"
    - "under-ten-minute task"
    - "single-specialty work"
route:
  profile: "deep"
  risk: "high"
consumes: []
reads: ["task", "domain-briefs", "subagent-results", "filesystem-state"]
writes: []
tools: []
references: []
verifier: ["Require bounded parallel delegation, one writer per file, completion auditing, and resolution of blocking critic findings."]
human_gate: true
consolidated-by: R3 (absorveu sdd como modos)
reviewed-scope: "checagem mecanica + semantica: 8/8 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 13 secoes, 255 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---


# Skill: Subagent Team

## Propósito
Orquestrar um time de sub-agentes especializados para tarefas que requerem múltiplas perspectivas simultâneas — substituindo workflows seriais por execução paralela coordenada.

---

## Condições de Ativação
Ative esta skill quando:
- A tarefa envolver >2 domínios distintos que podem ser trabalhados em paralelo
- O usuário solicitar `@team [tarefa]`
- Uma análise profunda exigir simultaneamente: pesquisa + estrutura + revisão crítica

NÃO ative para: tarefas sequenciais estritas; operações que precisam de output de um agente para iniciar outro; tarefas <10 min.

---

## Catálogo de Sub-Agentes Disponíveis

| Sub-Agente | Especialidade | Quando Convocar |
|-----------|--------------|----------------|
| **Researcher** (+ web search MCP) | Coleta e síntese de dados, fact-checking | Sempre que houver questões factuais abertas |
| **Editor** | Refinamento de texto, clareza, consistência | Output textual que vai para usuário final |
| **PM (Product Manager)** | Priorização, user stories, OKRs | Decisões de produto/feature |
| **Analyst** | Dados, métricas, padrões quantitativos | Qualquer análise com números |
| **Critic** | Revisão adversarial, red-team | Antes de decisões críticas irreversíveis |
| **Ops** | Tarefas operacionais, scripts, automação | Execução mecânica de procedimentos |

## Perfil de modelo

Perfil `deep` — já declarado em `route.profile` do frontmatter: erro de
decomposição cascateia para todos os sub-agentes convocados
(model-routing §Padrão
custo-efetivo; model-catalog
§Perfis).

> **Modelo por papel não vive aqui.** A tabela acima mapeia papel → especialidade
> → gatilho, que é conteúdo próprio desta skill. Modelo e effort de cada
> sub-agente resolvem na policy (§Régua rápida), não numa coluna local.
>
> **Padrão commander-and-hands** (formalizado em fable-5-subagent-setup-parallel-agents): modelo caro planeja e revisa, baratos executam. → model-routing · subagent-spawning

---

## Protocolo de Execução

### PASSO 1 — Decomposição *(Nexus/Sonnet)*
Quebre a tarefa em sub-tarefas independentes:
- Identifique: quais sub-tarefas NÃO dependem umas das outras (paralelizáveis)
- Identifique: dependências sequenciais obrigatórias
- Atribua: cada sub-tarefa ao sub-agente mais adequado

Exemplo de decomposição para "análise competitiva de produto X":
```
PARALELO:
  Researcher → coleta dados de mercado, reviews, pricing
  Analyst → busca métricas de crescimento e benchmarks
  PM → define critérios de avaliação e framework de análise
SEQUENCIAL (após paralelos):
  Editor → consolida em documento coeso
  Critic → revisão adversarial do documento final
```

### PASSO 2 — Briefing dos Sub-Agentes *(Nexus)*

**Antes de montar o prompt:** se a sessão tiver >10 mensagens de contexto, rodar o §MODO BRIEF abaixo para cada sub-agente antes de continuar.

Para cada sub-agente, forneça na ordem:
```
[1] Brief da sessão (campos de TaskPacket do MODO BRIEF: evidence, negatives, scope)
[2] Skills injetadas (conteúdo completo das skills relevantes para este agente)
    → consultar tabela de roteamento do Nexus: nexus
[3] Prompt do sub-agente:
    Você é o <Nome> do time Nexus.
    Tarefa: <sub-tarefa específica>
    Input disponível: <o que você tem acesso>
    Output esperado: <formato e conteúdo exato>
    Prazo de contexto: <tokens budget — mantenha conciso>
    Modelo de entrega: escreva em <arquivo>.md ao concluir
```

**Regra:** nunca entregar apenas o prompt sem brief + skills. Sub-agente sem contexto re-deriva premissas resolvidas e pode contradizer decisões da sessão.

### PASSO 3 — Execução Paralela *(múltiplos sub-agentes)*
- Dispatcher os sub-agentes paralelizáveis simultaneamente
- Cada sub-agente escreve seu output em arquivo dedicado: `team/<agente>-output.md`
- Não espere por todos para iniciar os sequenciais — inicie assim que dependências forem satisfeitas

**Dimensionamento de lote** (quando o trabalho for processamento de arquivos).
Limites validados em 2026-06-28 sobre 441 arquivos: ≤45 arquivos/subagente
completa (~310s); 60–80 é borderline (~540s); 87+ estoura o timeout de 600s.

1. **Cap duro: 50 arquivos por dispatch.**
2. **Chunk de 8–10 arquivos** por chamada dentro do subagente — 15–20 desacelera cada chamada.
3. **>150 arquivos: dividir em waves** — disparar wave 1, **re-contar o que sobrou**, disparar wave 2.
4. **Sempre re-contar após o dispatch** (`grep -rL`). Subagente pode terminar tudo e estourar o timeout antes de reportar: silêncio não é falha, e relatório não é evidência.
5. **Recuperação de timeout:** varrer os gaps programaticamente e re-disparar em lotes ≤30.

### PASSO 4 — Consolidação *(Editor/Haiku)*
- Leia todos os `team/*-output.md`
- Elimine redundâncias, resolva contradições (marque divergências com `[CONFLITO]`)
- Produza `team/consolidated.md` mantendo atribuição de cada contribuição <!-- drift:ok: saída criada em runtime -->

### PASSO 5 — Revisão Adversarial (se crítico) *(Critic/Opus)*
Instrução para o Critic:
```
Leia consolidated.md com olhar de red-team.
Questione:
- Pressupostos não declarados
- Conclusões que não seguem dos dados
- Riscos não endereçados
- Vieses de confirmação
NÃO seja construtivo — seja cético. Seu papel é encontrar o que está errado.
Output: lista de findings com severidade (BLOQUEANTE | IMPORTANTE | MENOR)
```

Se findings BLOQUEANTES: retorne ao agente responsável para revisão.

---

## Artefatos de Saída
- `team/<agente>-output.md` — saídas individuais
- `team/consolidated.md` — versão integrada <!-- drift:ok: saída criada em runtime -->
- `team/critic-review.md` — se revisão adversarial foi executada <!-- drift:ok: saída criada em runtime -->

---

## Pitfalls

Falhas e correções de batches de subagentes (timeout, self-report vs filesystem, manifest concorrente, batch sizing, git autonomy): consultar `[reference](reference.md)` quando um batch falhar — não fazem parte do protocolo normal.
---

## Completion

- [ ] Sub-agentes convocados conforme necessidade (não todos para tarefa simples)
- [ ] Brief injetado em cada sub-agente (decisões + skills + tarefa)
- [ ] Critic findings BLOQUEANTES tratados (não ignorados)
- [ ] Single-threaded writes: 1 agente escreve por arquivo
- [ ] Max spawn depth: 2 (parent → subagent → 1 nível)
- [ ] Se sub-agente exceder 2× tempo: cancelado e atribuído ao próximo

## Failure modes

- **Over-spawn**: convocar todos sub-agentes para tarefa que 1 resolve → desperdício
- **Ignore blocking findings**: Critic flaga BLOQUEANTE e parent ignora → findings existem para isso
- **Concurrent writes**: 2+ agentes escrevem mesmo arquivo → single-threaded writes obrigatório
- **Deep spawn**: subagent spawna subagent que spawna subagent → max depth 2, retorna ao parent

---

## Restrições
- NUNCA convoque todos os sub-agentes para tarefas que um único agente resolve
- NUNCA use Opus para Researcher, Editor, ou Ops — desperdício claro
- NUNCA ignore findings BLOQUEANTES do Critic — eles existem para isso
- Se um sub-agente exceder 2× o tempo estimado: cancele e atribua ao próximo mais capaz
- **Max spawn depth: 2** (parent → subagent → 1 nível mais). Se subagent precisa de modelo mais capaz → retorna ao parent com contexto, não escala sozinho
- **Single-threaded writes:** apenas 1 agente escreve por arquivo. Outros contribuem inteligência (review, análise), não ações de escrita concorrentes


## MODO BRIEF — destilar a sessão em TaskPacket

Absorvido de [context-handoff](context-handoff.md)
(adr-nx-019). O brief deixa de ser formato próprio: emite campos do TaskPacket,
que é o contrato canônico de briefing
(prompt-contracts).
Serve ao PASSO 2 e a qualquer delegação única após sessão longa.

**Quando:** sessão com >10 mensagens, ou subagente que decide sobre algo que a
sessão já decidiu. **Não:** subagente autônomo com input próprio (ex.: wiki-ingest
sobre `.raw`); delegação de 1 passo sem histórico; handoff entre sessões (use o
handoff-file).

1. **Filtrar pelo destino.** O agente que recebe define o que é relevante:
   guard → escopo e restrições; hill → comportamento observado e versão do agente;
   verify → spec e critérios de aceite; extend → o que entra e o que não muda;
   review → o que mudou e o que preservar.
2. **Varrer a sessão e mapear para o TaskPacket:**

| Da sessão | Campo do TaskPacket |
|-----------|---------------------|
| Decisões tomadas (com porquê, se não óbvio) | `evidence` |
| Estado atual (arquivos mudados, versões) | `evidence` |
| Restrições ativas (CLAUDE.md, pedidos do usuário) | `negatives`, com `when/auth/else/effect` |
| Tarefa delegada, 1-3 frases | `objective` |
| Fora do escopo desta delegação | `scope.deny` ou `negatives` |
| Tópicos irrelevantes ao destino | não entram (filtro, não campo) |

3. **Ordem no prompt:** brief (campos acima) → skills injetadas → prompt do
   sub-agente (PASSO 2).

Limites: máximo 30 linhas; brief maior é problema de escopo, não de brief. Sem
decisão relevante, 3 linhas bastam. Nunca colar o histórico da conversa. Nunca
omitir decisão que o subagente poderia contradizer. Restrição escrita como prosa
("não criar arquivos") em vez de `negatives` estruturado perde força vinculante
na compactação (prompt-contracts §Por que `negatives` é estruturado).

## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO REVIEW POR TASK (sdd)** — [sdd](sdd.md)

## Quando NÃO usar

- **Dependência estritamente sequencial** entre as partes — paralelizar não ganha; executar serial.
- **Tarefa <10 min ou domínio único** — overhead de briefing/consolidação > ganho; fazer direto.
- **Trabalho single-specialty** — um especialista basta; time para uma skill só é cerimônia.
- **Escrita no mesmo arquivo por 2+ agentes** — viola writer único; consolidar antes ou serializar.

Disambiguation: `orchestration/subagent-team` paraleliza domínios independentes; `orchestration/router-select` escolhe modo antes — team assume modo já definido. Escrever o plano em ondas para outro modelo executar depois (sem despachar agora) é `plan-handoff`.
