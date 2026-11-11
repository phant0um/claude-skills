---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: handoff
description: "Use when: compactar a conversa atual em handoff para outra sessão retomar (stow para auto-retomada). Plano em ondas para outro modelo executar é plan-handoff."
updated: 2026-11-10
argument-hint: What will the next session be used for?
---

# Handoff

Compactar conversa atual em documento de handoff. Agente fresco continua o trabalho sem perder contexto.

## Regras (Pocock original)

1. **Salvar em temp file.** Gerar path com `mktemp -t handoff-XXXXXX.md`. Ler arquivo antes de escrever.
2. **Nao duplicar artefatos.** PRDs, plans, ADRs, issues, commits, diffs — referenciar por path ou URL, nao copiar.
3. **Sugerir skills.** Indicar quais skills a proxima sessao deve usar.

## Estrutura do Handoff

```markdown
# Handoff — [titulo curto do trabalho]

## Objetivo
[1-2 frases: o que estamos tentando fazer e por que]

## Estado Atual
- O que foi feito: [lista]
- O que falta: [lista]
- Bloqueios: [se houver]

## Decisoes Tomadas
[Decisoes arquiteturais/design ja resolvidas — nao re-discutir]

## Artefatos Existentes
- PRD: [path ou URL]
- Issues: [path ou URL]
- Commits: [hashes relevantes]
- Diffs pendentes: [path]
- Arquivos modificados: [lista]

## Proximo Passo
[Acao especifica e imediata pra proxima sessao]

## Skills Recomendadas
[Quais /skills usar na proxima sessao]

## Contexto Critico
[Gotchas, edge cases, decisoes nao-obvias que o proximo agente PRECISA saber]
```

## Processo

1. Revisar conversa inteira — identificar decisoes, artefatos, estado
2. Coletar paths de todos arquivos criados/modificados
3. Identificar trabalho pendente
4. Gerar handoff com estrutura acima
5. Salvar via `mktemp -t handoff-XXXXXX.md`
6. Se rodando dentro do vault-michel: gravar cópia permanente em `03-RESOURCES/sessions/` (ver "Persistência no vault" abaixo) e atualizar `sessions-index.md`
7. Reportar path(s) pro usuario

## Persistência no vault

O temp file (`mktemp`) evapora — some com a máquina/sessão. O vault registra erro (`04-SYSTEM/system/logs/errors.jsonl`) e decisão (`04-SYSTEM/system/decisions/decisions.md`), mas nunca a **intenção** por trás do trabalho. Por isso, sempre que o handoff (ou o modo stow) rodar dentro do vault-michel, além da saída padrão, gravar também:

`03-RESOURCES/sessions/YYYY-MM-DD-<slug>.md`, frontmatter no padrão do vault mais dois campos explícitos:

```yaml
---
title: <título curto do trabalho>
type: session
created: YYYY-MM-DD
tags: [session, ...]
intent: <1 frase — o que se queria fazer>
outcome: <1 frase — o que de fato saiu>
---
```

`intent` e `outcome` são deliberadamente separados: o vault já sabe registrar o que aconteceu (decisions.md, errors.jsonl); o que faltava era registrar o que se pretendia, para comparar depois com o que saiu. Corpo do documento segue a mesma estrutura do handoff (Objetivo/Estado Atual/Decisões/Artefatos/Próximo Passo/Contexto Crítico) — ver `03-RESOURCES/sessions/2026-07-17-vault10x-rotinas.md` como referência de formato.

Depois de gravar, acrescentar 1 linha em `03-RESOURCES/sessions/sessions-index.md` (seção "Notas"), no formato já usado no arquivo:

```
- YYYY-MM-DD-<slug> — <resumo de 1 linha>
```

Isso NÃO substitui o temp file (passo 5 continua valendo para o handoff efêmero entre agentes) — é um registro adicional e permanente. Não mexer em `hot.md`, manifest ou state a partir daqui.

## Brief de delegação (economia Fable)

Handoff/dispatch é brief de delegação. Custo de agente = turnos + contexto arrastado + o que o lead refaz sozinho — não preço/token. Disciplina do manager (não micromanager):

1. **Enumerar constraints + edge cases + "done".** Brief spec-quality > ditado passo-a-passo. Ex: "operator() O(1) no comprimento: SEM full scan" (constraint explícita) em vez de reimplementar. Constraint não-escrita = esquecida → bug.
2. **Delegar cedo, com escopo inteiro.** Handoff tarde (após solo-explorar e implementar) desperdiça — decisões já feitas, contexto já caro. Passar reconhecimento + implement+test+lint como um brief.
3. **Confiar no retorno; revisar barato.** 1 diff review, não puxar arquivos de volta e reescrever a lead-price. Bug real no retorno → outro handoff barato, não rewrite.
4. **Não delegar o indelegável.** Debugging serial (contexto acumulado É o trabalho) e tarefas curtas sem componente separável → fazer direto. O mesmo julgamento que escreve bom brief sabe quando não escrever.

## Constraints

- NAO copiar conteudo de artefatos — referenciar por path
- NAO incluir historico de debugging/tentativas falhas (so conclusoes)
- NAO incluir contexto que ja esta em CLAUDE.md ou memory
- Handoff deve ser lido em < 30 segundos por agente fresco
- Maximo ~200 linhas. Se mais → algo esta sendo duplicado

## Modo stow (self-resume)

Mesma mecanica de varredura, framing diferente. **handoff** = curado pra OUTRO agente/sessao pegar. **stow** = guardar MEU tesouro pra poder limpar o contexto AGORA com confianca e retomar eu mesmo depois — "stow your treasure before you sail again" (Kun Chen). Independe de haver proxima sessao definida.

Difere de `/compact` (sumariza + descarta, com ruido da janela) e de `/clear` (wipe seco, perde tudo): stow **persiste** decisoes/aprendizados/next-steps abertos em disco ANTES do wipe.

Ajustes no modo stow:
- Storage: nao usar `mktemp` (efemero). Salvar em local duravel — no vault, `03-RESOURCES/sessions/YYYY-MM-DD-<slug>.md` (frontmatter + `intent`/`outcome` como em "Persistência no vault" acima, e atualizar `sessions-index.md`); fora do vault, `.claude/stow-<slug>.md`.
- Secao "Skills Recomendadas" opcional (talvez retomes na mesma config).
- Regra de decisao contexto: **stow+clear** quando tarefa muda ou contexto morto · **handoff** quando entrega pra sessao/agente novo · **compact** so se nao der pra encerrar a fase (aceita ruido).

## Linhagem

- **Upstream:** Matt Pocock (handoff original — temp file, referência-não-cópia, sugerir skills) + Fable/Cognition (delegation-brief: constraints+edge+done, delegar cedo).
- **Original (vault):** modo stow (self-resume durável no vault) + brief de delegação operacionalizado.
- **Critério:** mecanismo > autor. Fonte rastreável, não privilegiada.
