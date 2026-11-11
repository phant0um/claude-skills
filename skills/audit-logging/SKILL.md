---
kind: skill-proc
resolver-status: exposed
type: skill
name: audit-logging
input:
  required_fields: [event_type, message]
output:
  format: markdown
  targets: [04-SYSTEM/record/logs/operations.md, 04-SYSTEM/record/logs/pipeline-log.md]
triggers:
  positive:
    - "append em log"
    - "registrar operação"
    - "append de decisão já tomada no operations.md"
  negative:
    - "editar log existente"
    - "relatório consolidado"
allowed_effects:
  - append 04-SYSTEM/record/logs/
  - append 04-SYSTEM/system/decisions/
forbidden_effects:
  - edit existing log entries
  - delete logs
  - modify manifest
version: 2.0.0
source_agent: ledger
status: active
created: 2026-08-20
description: "Use when: registrar eventos, progresso, receipts e trilha append-only (operations.md, pipeline-log) — infraestrutura de registro chamável por outras skills (ex.: meta/decisions), sem autoridade arquitetural. Decisão arquitetural canônica é meta/decisions. decisions não serve para o append mecânico de uma decisão ou ADR entry já tomada em operations.md/pipeline-log (isso é aqui), e editar entrada já gravada não é append nem é aqui."
updated: 2026-10-24
reviewed: 2026-10-24
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Reescrita em 2026-10-24. Nao ha script que escreva operations.md ou pipeline-log.md; a disciplina e so de convencao. Removidos docs/progress.md, logs/sessions/ e docs/adr/ (paths do projeto de origem que nao existem aqui; anotados em 2026-08-31 mas o corpo continuava mandando usa-los), o modelo de ADR duplicado (canonico: skill decisions) e o modelo haiku-5-5 low declarado sem checagem. Conferido: formato de entrada do operations.md e do pipeline-log.md, hooks block-add-all.sh e block-push-main.sh. NAO conferido: salience/decay (principio sem enforcement em codigo); operations.md tem updated 2026-08-29, entao nao ficou provado que o log ainda recebe entradas no ritmo descrito."
---

# audit-logging — trilha append-only

> **Sem driver em código.** Nenhum script escreve `operations.md` ou `pipeline-log.md`; a disciplina é convenção. Quem
> chama (Nexus ou outra skill) escreve a entrada. Se esta página divergir de um hook ou schema, o hook e o schema valem.
> Procedimento histórico (progress.md, logs/sessions/, modelo de ADR): `git show 24cf4b348:04-SYSTEM/automation/skills/pipeline/audit-logging/SKILL.md`.
>
> **Proveniência:** procedimento transplantado de `04-SYSTEM/automation/agents/nexus-agent-system/ledger.md` @ `2b69d9b3b` (S1, 2026-08-23); reescrito em 2026-10-24.

## Onde registrar

| Destino | O que entra |
|---------|-------------|
| `04-SYSTEM/record/logs/operations.md` | toda operação de escrita relevante, com timestamp |
| `04-SYSTEM/record/logs/pipeline-log.md` | execuções do pipeline diário e semanal |
| `04-SYSTEM/system/state/context/hot.md` | estado vivo (não existe `progress.md` neste vault) |
| `04-SYSTEM/system/decisions/adr/` | ADR: só pela skill `decisions` |

Formato observado: `operations.md` usa `## <AAAA-MM-DDTHH:MM> — <título>` com `**Operação:**`, `**Agente:**`, `**Escopo:**`.
`pipeline-log.md` usa `## Pipeline Diário <data>` com `**Triagem:**`, `**Ingest:**` e link para o relatório.

## Regras

- **Append-only.** Nunca edite nem apague entrada gravada. Correção = entrada nova que aponta para a anterior.
- Arquivo de log ausente: crie com header. Evento sem classificação: use `manual`.
- **Extração, não transcrição:** registre o princípio que muda comportamento futuro, não o transcript.
- **Promotion gate:** candidato a memória durável passa por (muda comportamento futuro? duplica? escopo certo?) e carrega
  proveniência (evento ou sessão de origem + quem escreveu). Escrita durável só na consolidação, não no meio do ciclo.
- **Escopo e decay** (princípio mem0, sem enforcement em código): `[user]` não decai; `[agent]` decai devagar; `[session]`
  decai rápido. Decay move para o log, nunca apaga. ADR é imune.
  Ver agent-memory-architecture · memory-layer · observability.
- Handoff humano: `[DECISION NEEDED]` ao Nexus antes de delete de log, force push ou reescrita de histórico.

## Commit local (push é do humano)

```bash
git -C ~/Obsidian/vault-michel status --porcelain   # nada mudou -> nao commite
git -C ~/Obsidian/vault-michel add <pathspec explicito>
git -C ~/Obsidian/vault-michel commit -m "vault: YYYY-MM-DD — <acao> <objeto>"
```

`block-add-all.sh` recusa `git add -A` e `git add .` (recolheria pendência de outra sessão e `06-GENERATED/`).
`block-push-main.sh` exige um sentinel de push criado **pelo humano**; o agente nunca o cria.
Política de squash: flips de kanban e artefatos F3.3 do mesmo ciclo fecham em **um** commit.

## Quando NÃO usar

- Decisão arquitetural (justificativa, alternativas, ADR) → `decisions`. Esta skill só faz o append mecânico.
- Editar entrada existente: proibido.
- Relatório analítico → `report-synthesis`. Comunicação externa → `content-synthesis`. Código → `forge`.

## Failure modes

- Sessão relevante sem entrada.
- Decisão de arquitetura só no log, sem ADR.
- `git add -A`, force push, criar o sentinel no lugar do humano, commitar `.env` ou token.
- Reescrever entrada antiga em vez de acrescentar uma nova.
