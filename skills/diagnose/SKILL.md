---
name: diagnose
description: "Use when: executar loop de debugging disciplinado para falhas que resistiram a 1+ tentativas diretas — proibido pular etapas ou fixar sem hipótese confirmada. MODO ALVO=SESSÃO DE AGENTE: sessão de agente em loop de tool calls, retry storm (429), context overflow, drift de prompt ou alucinação de path — capturar evidência, classificar, recovery reversível, introspection report."
trigger: "@diagnose [bug]" | "/diagnose [bug]" | "diagnose this" | "debug this" | "isso não resolve, me ajuda a diagnosticar"
---



# Skill: Diagnose

## Propósito
Executar loop de debugging disciplinado para falhas que resistiram a 1+ tentativas diretas. Proibido pular etapas ou fixar sem hipótese confirmada.

> **Leading word: tight.** A tight loop é fast, deterministic, e red-capable (vai red no bug). Um loop flaky de 30s é quase inútil; um loop tight de 2s é um superpoder de debugging.

---

## Condições de Ativação
Ative esta skill quando:
- Bug não resolvido após 1 tentativa direta
- Falha com comportamento intermitente ou não-reproduzível
- Erro cuja causa-raiz é desconhecida (não apenas sintoma visível)
- `@diagnose [descrição do bug]` chamado explicitamente

NÃO ative para: erros óbvios de sintaxe; falhas já diagnosticadas aguardando fix; tarefas sem componente de bug.

---

## Perfil de modelo

Perfil `deep` — diagnostico e a linha textual do perfil no catalog; a etapa Hypothesise carrega
o raciocinio causal de que o resto do loop depende
(model-routing §Padrao custo-efetivo; model-catalog §Perfis).
Esta skill nao mantem pins locais por etapa.

## Protocolo de Execução

### ETAPA -1 — Selecionar ALVO (obrigatório antes da ETAPA 0)

O que falhou?

- **Código, build, teste, dado** → ALVO = SOFTWARE. Seguir ETAPA 0 abaixo.
- **Output de um agente** (agente disse/fez algo inesperado; a pergunta é *qual
  parte do agent file habilitou isso*) → ALVO = OUTPUT DE AGENTE. Carregar
  `trace` e executar por lá. Não seguir
  para a ETAPA 0.
- **Sessão de agente em falha agora** (loop de tool calls, retry storm 429,
  context overflow, drift de prompt, alucinação de path — a pergunta é *como
  conter e recuperar*) → ALVO = SESSÃO DE AGENTE. Executar a seção
  `## MODO ALVO = SESSÃO DE AGENTE` abaixo. Não seguir
  para a ETAPA 0.

Teste que separa os dois alvos de agente: OUTPUT DE AGENTE é atribuição estática
sobre um output já produzido; SESSÃO DE AGENTE é recuperação de uma sessão viva
em falha.

### ETAPA 0 — Build a Tight Feedback Loop

> **Esta é a skill.** Todo o resto é mecânico. Se você tem um loop tight que vai red no bug, você vai encontrar a causa. Se não tem, nenhuma quantidade de leitura de código vai salvar.

Seja agressivo e criativo. Recuse desistir. 10 ways de construir um loop (em ordem de preferência):

1. **Failing test** no seam que alcança o bug (unit, integration, e2e)
2. **Curl / HTTP script** contra dev server rodando
3. **CLI invocation** com fixture input, diffando stdout vs snapshot known-good
4. **Headless browser script** (Playwright/Puppeteer) — drives UI, asserta DOM/console/network
5. **Replay captured trace** — salva request/payload/event log real, replay no code path isolado
6. **Throwaway harness** — subset mínimo do sistema (1 service, mocked deps) que exercita o bug
7. **Property/fuzz loop** — se bug é "sometimes wrong output", 1000 random inputs procurando failure mode
8. **Bisection harness** — automatiza "boot at state X, check, repeat" para `git bisect run`
9. **Differential loop** — mesmo input em old-version vs new-version, diff outputs
10. **HITL bash script** — último recurso. Drive humano com script estruturado

**Tighten o loop** (tratar como produto):
- **Faster?** Cache setup, skip unrelated init, narrow test scope
- **Sharper signal?** Asserta sintoma específico, não "didn't crash"
- **More deterministic?** Pin time, seed RNG, isolate filesystem, freeze network

**Bugs não-determinísticos:** objetivo não é repro limpo, é **higher reproduction rate**. Loop trigger 100×, paraleliza, add stress, narrow timing windows, inject sleeps. Bug 50% flake é debuggable; 1% não — keep raising rate.

**Quando genuinamente não pode construir loop:** parar e dizer explicitamente. Listar o que tentou. Pedir: (a) access ao environment reproduzível, (b) artifact capturado (HAR, log dump, core dump), (c) permissão para instrumentation temporária em produção. **Não prosseguir para hipóteses sem loop.**

Output obrigatório:
```
LOOP: <tipo escolhido (1-10)>
COMMAND: <1 comando que já rodou pelo menos 1× que vai red no bug>
OUTPUT: <output do comando acima>
TIGHT: [fast + deterministic + red-capable | flaky <X%> | não-reproduzível]
```

> **Se você se pegar lendo código para construir teoria antes deste comando existir, STOP.** Hipótese sem loop red-capable é o failure mode exato que esta skill previne.

### ETAPA 1 — Reproduce
Objetivo: confirmar que o bug existe e é consistente.

```
- Execute o caminho exato que produz a falha
- Documente: input → comportamento observado → comportamento esperado
- Se não reproduzir em 3 tentativas → PARE, reporte ao usuário (bug pode ser flaky)
```

Output obrigatório:
```
REPRODUCE: [sim | não | flaky]
INPUT: <condições exatas>
OBSERVED: <o que acontece>
EXPECTED: <o que deveria acontecer>
```

### ETAPA 2 — Minimise
Objetivo: isolar o menor caso que ainda reproduz o bug.

```
- Remova dependências, dados e contexto irrelevantes um por um
- Teste após cada remoção — se bug sumir, o removido era relevante
- Pare quando remover qualquer coisa fizer o bug desaparecer
```

Output obrigatório:
```
MINIMAL CASE: <menor reprodução encontrada>
REMOVED: <o que foi eliminado sem perder o bug>
```

### ETAPA 3 — Hypothesise
Objetivo: formular hipóteses causais ordenadas por probabilidade.

```
- Liste 3-5 hipóteses para a causa-raiz (não o sintoma)
- Para cada hipótese: o que ela prevê que seria verdade se correta?
- Ordene por: (probabilidade × facilidade de testar)
- Escolha a #1 para testar primeiro
```

Output obrigatório:
```
H1: <hipótese> | Prevê: <observação testável> | P: alta/média/baixa
H2: <hipótese> | Prevê: <observação testável> | P: alta/média/baixa
...
TESTAR PRIMEIRO: H<n>
```

### ETAPA 4 — Instrument
Objetivo: adicionar observabilidade mínima para confirmar ou refutar H1.

```
- Adicione logs/asserts/breakpoints no ponto que distingue H1 das outras
- NÃO fixe ainda — apenas observe
- Execute com instrumentação → colete evidência
- Se evidência refuta H1: volte à ETAPA 3, mova para H2
- Se evidência confirma H1: avance para fix
```

Output obrigatório:
```
INSTRUMENTAÇÃO: <o que foi adicionado e onde>
EVIDÊNCIA: <o que foi observado>
CONCLUSÃO: H<n> [confirmada | refutada]
```

### ETAPA 5 — Fix
Objetivo: correção dirigida pela hipótese confirmada — nada além do necessário.

```
- Fix apenas o que a hipótese confirmada indica
- NÃO refatore código adjacente
- NÃO adicione features ou "melhorias de oportunidade"
- Remova toda instrumentação adicionada na ETAPA 4
```

### ETAPA 6 — Regression Test
Objetivo: garantir que o fix não quebra nada e não regride.

```
- Execute o caso mínimo da ETAPA 2 — deve passar
- Execute o suite de testes existente — zero regressões permitidas
- Se não houver testes: escreva 1 teste que teria capturado o bug antes
```

Output obrigatório:
```
CASO MÍNIMO: [passou | falhou]
SUITE: [passou | N falhas]
NOVO TESTE: <path do arquivo criado, se aplicável>
```

---

## Completion

- [ ] ETAPA 1 Reproduce: bug confirmado (sim/não/flaky) com input exato documentado
- [ ] ETAPA 2 Minimise: menor caso de reprodução isolado
- [ ] ETAPA 3 Hypothesise: 3-5 hipóteses listadas, rankeadas, #1 escolhida para testar
- [ ] ETAPA 4 Instrument: evidência coletada confirma ou refuta H1
- [ ] ETAPA 5 Fix: correção dirigida pela hipótese confirmada, instrumentação removida
- [ ] ETAPA 6 Regression: caso mínimo passa + suite existente zero regressões

## Failure modes

- **Fix sem hipótese**: pular ETAPA 3-4 e fixar por gut feeling → proibido, hipótese confirmada é obrigatória
- **Múltiplos fixes simultâneos**: mudar 2+ coisas entre runs → isola variável, um fix por vez
- **Skip do Minimise**: testar no contexto grande → mascara causa-raiz, sempre isolar
- **Hipóteses esgotadas**: ETAPA 3 sem confirmação → chamar `heavy-think` com minimal case, não forçar fix

---

## Regras de Ouro

- **Proibido fixar sem hipótese confirmada** — gut feeling não conta
- **Proibido pular MINIMISE** — testar em contexto grande mascara a causa
- **Proibido múltiplos fixes simultâneos** — isola a variável
- **Se ETAPA 3 esgotar hipóteses sem confirmação**: chame `heavy-think.md` com o minimal case

---

## Artefatos de Saída
- Fix aplicado no código
- Teste de regressão adicionado (se ausente)
- Relatório inline no formato por etapa acima


## Quando NÃO usar

- **Erro óbvio de sintaxe/typo** — corrigir direto; loop de diagnóstico é overhead.
- **Falha já diagnosticada aguardando fix** — diagnose termina na causa confirmada; implementar é de `core/implement`.
- **Tarefa sem componente de bug** (feature, refactor, docs) — diagnose é loop de debugging, não execução.
- **Bug com 0 tentativas diretas** — a skill assume 1+ falha; primeira tentativa pode ser direta, sem o loop.

Disambiguation: `reasoning/diagnose` é o loop disciplinado para falhas resistentes; `systematic-debugging` não existe em automation — use `reasoning/diagnose` (fase 0 de diagnóstico precede — diagnose absorve o padrão, não o substitui); `core/tdd` escreve o teste de regressão depois da causa confirmada.

## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO ALVO = OUTPUT DE AGENTE** — `trace`
- **MODO ALVO = SESSÃO DE AGENTE** — seção abaixo; absorvido de
  agent-fault-debug

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

**S5 — Lição (opcional).** Durável → 1 linha no arquivo de lições do projeto (ex. `lessons.md`), depois de conferir se já não existe.

**Completion do modo:** evidência capturada antes de qualquer ação; padrão
classificado; check executado e registrado; recovery reversível com estado
anterior anotado; report completo. Falha declarada com evidência também é
término; sucesso sem evidência não é.

Exemplo: pipeline-drain repete a mesma ingestão 6× em 40s com 429 e
`Retry-After: 60` → retry storm; check confirma backoff ignorado; abort + 1
retry após 60s + fases serializadas; lição: retry de pipeline-drain respeita
Retry-After, >3 repetições = abortar e escalar.
