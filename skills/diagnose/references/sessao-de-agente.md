---
name: sessao-de-agente
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/reasoning/diagnose/SKILL.md
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Corrigido `04-SYSTEM/system/logs/errors` (nao existe) para `errors.md`. 06-GENERATED/tasks/lessons.md existe. Padroes de falha lidos, nao reproduzidos."
---

## MODO ALVO = SESSÃO DE AGENTE

Sessão de agente **viva** em falha: conter e recuperar. Aqui não há loop
red-capable a construir; o insumo irrecuperável é a evidência da sessão, e a
ordem é lei: evidência antes de ação, retry só depois do diagnóstico.

**Não usar quando:** o alvo é código ou output (ETAPA 0 ou OUTPUT DE AGENTE);
transcript/log já se perdeu (reportar que não há evidência e aguardar
recorrência); a falha é de infraestrutura provada (API fora para todos, rede,
credencial, quota zerada); é a primeira execução de skill nova (rodar de novo
com input completo); a instrução mudou no meio (renegociar, não debugar); não
dá para citar o sintoma.

**S0 — Capturar evidência antes de mexer.** Nada de kill, restart ou limpar
histórico antes. Transcript/log citado literal: (a) timestamp do início do
sintoma; (b) sequência exata das últimas tool calls, input→output; (c) texto do
erro com status code; (d) número de repetições; (e) estado real do mundo (paths,
arquivos). Critério: responde "o que o agente fez, nesta ordem, e onde parou"
sem depender de memória.

**S1 — Classificar o padrão.**

| Padrão | Sintoma observável | Causa provável | Check + recovery |
|---|---|---|---|
| Loop de tool calls | Mesma chamada ≥3× com input/output idênticos; zero progresso | Objetivo ambíguo; tool sem efeito visível no estado | Check: o estado real mudou entre chamadas? Recovery: abortar; reafirmar o objetivo em 1 frase; verificar o mundo real; encolher para 1 passo |
| Retry storm 429 | 429/503 em sequência com retry imediato; backoff ausente ou <1s | Retry-After ignorado; paralelismo excessivo | Check: há Retry-After? Recovery: parar retries; backoff ≥60s; serializar; reduzir concorrência |
| Context overflow | Erro de token; instruções iniciais truncadas; agente "esquece" o objetivo | Histórico acumulado; tool output gigante | Check: contexto vs limite. Recovery: compactar; tool output para arquivo + ponteiro; subagente de compressão; nunca continuar sem compactar |
| Drift de prompt | Age fora da instrução; cita política inexistente; contradiz a skill | Instrução canônica soterrada ou contradita | Check: a instrução original está no contexto? Recovery: reler skill/AGENTS.md; reafirmar citando a linha; remover a instrução conflitante |
| Alucinação de path | Lê/escreve path inexistente; inventa conteúdo; cria estrutura sem pedido | Path deduzido do nome, não verificado | Check: o path existe? Recovery: usar o path real; nada de path novo sem confirmação; reverter escrita feita |

Dois padrões juntos (ex.: overflow causando drift) são tratados os dois.

**S2 — Um check discriminante.** Uma observação que separa as causas
candidatas, um check por vez, resultado registrado (confirma/descarta) antes de
qualquer recovery. Ordem: reafirmar objetivo → verificar mundo real → encolher
escopo → check → só então retry.

**S3 — Recovery contido.** Menor ação reversível primeiro (parar retries,
reafirmar instrução, editar 1 linha) antes de destrutiva (kill, reescrita,
reinício). Anotar o estado anterior antes de cada ação. Retry sem diagnóstico
repete o sintoma e, em 429, piora o rate limit.

**S4 — Introspection report** (na resposta final):

| Campo | Registrar |
|---|---|
| sintoma | Erro/log citado literal + timestamp inicial |
| padrão | Linha da tabela S1, ou "fora da tabela" + justificativa |
| evidência | Tool calls, repetições, estado real |
| causa | Hipótese confirmada + check que a confirmou; não confirmada = `[hyp]` |
| ação | O que foi feito, em que ordem, quão reversível |
| resultado | done/falhou + critério observado, sem maquiagem |
| lição | 1 linha acionável contra recorrência |

**S5 — Lição (opcional).** Durável → 1 linha em `06-GENERATED/tasks/lessons.md`,
depois de conferir `04-SYSTEM/system/logs/errors.md` para não duplicar.

**Completion do modo:** evidência capturada antes de qualquer ação; padrão
classificado; check executado e registrado; recovery reversível com estado
anterior anotado; report completo. Falha declarada com evidência também é
término; sucesso sem evidência não é.

Exemplo: pipeline-drain repete a mesma ingestão 6× em 40s com 429 e
`Retry-After: 60` → retry storm; check confirma backoff ignorado; abort + 1
retry após 60s + fases serializadas; lição: retry de pipeline-drain respeita
Retry-After, >3 repetições = abortar e escalar.
