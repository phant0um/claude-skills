---
kind: skill-proc
resolver-status: exposed
origin: native
type: skill
name: study-digest
input:
  required_fields: [source_path, time_budget]
  optional_fields: [focus]
output:
  format: markdown
triggers:
  positive:
    - "study-digest"
    - "estudar em pouco tempo"
    - "condensar CONTENT para estudar"
    - "tenho 30 min para estudar a fase"
    - "colinha da fase"
  negative:
    - "ingerir apostila"
    - "explicar conceito"
    - "resumir fontes"
    - "escrever artigo"
    - "flashcards"
    - "simulado"
    - "concurso"
    - "revisão espaçada"
    - "ingerir PDF ou URL novo"
consumes: [source_path]
reads: ["02-AREAS/fiap/**", "02-AREAS/concurso/materias/**"]
writes: ["02-AREAS/fiap/**/STUDY-*.md", "02-AREAS/concurso/materias/**/STUDY-*.md"]
allowed_effects:
  - write 02-AREAS/fiap/**/STUDY-*.md
  - write 02-AREAS/concurso/materias/**/STUDY-*.md
forbidden_effects:
  - modify source_path
  - modify manifest
  - external-publish
tools: [Read, Grep, Bash, Write]
references:
  - "SKILL-BASE"
  - "[content-synthesis](../content-synthesis/SKILL.md)"
  - "ingest-fiap-batch"
  - "mestre"
verifier: ["python3 04-SYSTEM/scripts/study-digest-verify.py <STUDY.md> (exit 0)"]
human_gate: false
version: 1.0.0
status: active
created: 2026-10-11
updated: 2026-11-10
description: "Use when: condensar um documento longo já ingerido (ex.: 02-AREAS/fiap/fase-N/CONTENT.md) em material de estudo para um tempo curto, com ponteiro para a seção de origem. Roda sob demanda, no Code. Ingerir apostila vai para ingest-fiap-batch; resumir fontes ou diff vai para content-synthesis; explicar do zero vai para o Mestre no Claude Chat."
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7+W8: corpo completo lido pelo shield (opus, somente leitura); W6a/W7b: exposicao e taxa F4 no modo full; W8/W8b: full-N no scratchpad, Pegadinhas condicional e taxa F4 do full; checks frontmatter/lint/evals verdes; 187 linhas, 9 secoes"
---

# study-digest - material de estudo curto a partir de CONTENT.md

> Base: SKILL-BASE.

## Propósito

Um documento consolidado como CONTENT.md passa de 300 KB. Esta
skill gera o oposto: um arquivo que se estuda no tempo que existe. Corta, não
reescreve nem inventa. Cada ponto aponta a seção de onde veio.

## Entradas

- `source_path`: arquivo `.md` longo do vault, normalmente `CONTENT.md`. Tem que estar em `02-AREAS/fiap/` ou `02-AREAS/concurso/materias/`.
- `time_budget`: `30min`, `2h`, `1d` ou `full` (modo full, abaixo). Qualquer outro valor: parar antes de montar o nome do arquivo.
- `focus` (opcional): tema ou disciplina que pesa na seleção. Sem `focus`, vale a
  ordem de importância do próprio documento.

Valores [hyp], recalibrar após o primeiro uso real; se o source tem roteiro ou
lista de prioridade, a calibração do source vale e a tabela é só teto.

| `time_budget` | Pontos de conceito | Perguntas de recall | Teto de linhas lidas [hyp] |
|---|---|---|---|
| 30min | até 10 | 10 | 600 |
| 2h | até 25 | 25 | 1500 |
| 1d | até 60 | 60 | 3000 |
| full | sem teto | sem teto | sem teto: cobre o source inteiro (ver Modo full) |

## Sequência

1. Validar entrada: `source_path` existe e é `.md`; a pasta dele está em
   `02-AREAS/fiap/` ou `02-AREAS/concurso/materias/`; `time_budget` está na tabela; o source tem 300 linhas ou
   mais (`wc -l`). Qualquer falha: parar e reportar. Source com menos de 300
   linhas: parar e mandar ler direto.
2. Mapear o documento sem lê-lo inteiro: `grep -n '^#' <source_path>` e o
   `wc -l`. Se existir seção de prioridade (ex.: "As N ideias..."), ler só ela.
3. Escolher as seções que entram: as de maior peso. Peso = ordem da seção de
   prioridade do source, ou número de capítulos da coluna "Onde" quando houver
   tabela. Sem critério próprio. Registrar as que ficaram fora e o motivo.
4. Ler cada seção escolhida por faixa de linhas (`Read` com `offset` e `limit`),
   nunca o arquivo inteiro. Somar as linhas lidas; não passar do teto da tabela.
5. Escrever cada ponto no formato abaixo: afirmação de 1 frase, trecho literal
   do source com 5 palavras ou mais, copiado sem alteração, e a citação.
6. Montar a saída (formato abaixo) em
   `STUDY-<stem>-<time_budget>[-<focus-slug>].md`, na mesma pasta do
   `source_path`; `<stem>` é o nome do source sem `.md`. Arquivo existente é
   sobrescrito só se: o frontmatter dele tem `type: study-digest`, o `source:` é
   igual, e `git diff --quiet -- <arquivo>` sai 0. Sem frontmatter: parar. Outro
   caso: parar e reportar.
7. Verificar: rodar `python3 04-SYSTEM/scripts/study-digest-verify.py <STUDY.md>`.
   Exit diferente de 0 = falhou. Pontos que o verifier reprova saem do digest e
   entram na conta de falha (F4 abaixo); rodar o verifier de novo até exit 0.

Falha = (removidos + [hyp]) / gerados. Conta só Conceitos e Cai na prova
primeiro (modo full: Briefing e Glossário, que substituem essas duas). Acima de 20%: falhou, reportar. O relatório informa as duas contagens:
gerados e removidos com [hyp] separado, e a taxa de falha.

## Modo full (estilo guia de estudo)

Cobre o source inteiro, sem escolher seções. Custa várias vezes mais tokens
que `30min`; rode só quando o usuário pedir `full`.

1. Faixas: `python3 04-SYSTEM/scripts/study-digest-batches.py <source> --until '<REGEX>'`
   (`--until` deixa de fora a lista de questões e o gabarito; declare o corte em
   Ficou de fora).
2. Uma execução no perfil `economy` (`model-routing.json`) por faixa (nunca haiku-4-5), em paralelo, lê a faixa inteira e grava
   pontos no formato de ponto em arquivo temporário de nome único por faixa
   (`batch-<N>.md` e `verify-<N>.md` em pasta própria `full-<N>/` no scratchpad da sessão, fora do vault; pasta
   compartilhada deixou execuções sobrescreverem umas às outras), um por linha, nas seções
   `Briefing`, `Glossário` e `FAQ` (e `Pegadinhas`, se a faixa trouxer apontamento de erro do próprio source). Glossário: `- <termo>: <definição> | "<trecho>" | ...`.
   FAQ: `- P: <pergunta> R: <resposta> | "<trecho>" | ...`.
3. Redução (orquestrador): juntar as faixas, tirar pontos repetidos, ordenar pela
   ordem do source, montar `STUDY-<stem>-full.md`. A redução não cria ponto novo:
   só copia ou descarta linhas das faixas.
4. Rodar o verifier (passo 7). Informar linhas lidas por faixa e a cobertura
   (linhas lidas / linhas do source, fora o corte `--until`).

## Formato de saída

Frontmatter: `title`, `type: study-digest`, `source: "<caminho do source relativo à raiz do vault, com .md>"`
(entre aspas), `source_commit` (saída de `git log -1 --format=%h -- <source_path>`),
`time_budget`, `focus`, `verifier` (o comando do passo 7), `created`.

Formato de ponto (Cai na prova primeiro e Conceitos), uma linha:

```
- <afirmação> | "<trecho>" | <stem>
```

- `<heading exato>`: texto do heading do source sem os `#`. O verifier ignora `*` na comparação; escreva sem `**` para o link de heading resolver no Obsidian [hyp: não testado].
- Heading de fórmula (letras matemáticas unicode, ex.: `## 𝐶𝑎𝑝𝑖𝑡𝑎𝑙 ...`) não delimita seção para o verifier; não cite um.
- `<trecho>`: uma linha do source, literal, com 5 palavras ou mais, sem aspas duplas dentro, e que não termina em palavra de ligação (de, que, não, com...): o verifier reprova frase cortada.
- `[hyp]` fica só para afirmação que o trecho sustenta em parte; o verifier aceita a linha e a conta de F4 soma.

Modo full troca as seções 1 a 4 por **Briefing**, **Glossário** e **FAQ**; **Pegadinhas** só se o próprio source apontar erros (a redução não cria ponto); `Ficou de fora` no fim.

Seções, nesta ordem:

1. **Cai na prova primeiro**: os 3 a 5 pontos de maior peso.
2. **Conceitos**: um ponto por item, no formato acima.
3. **Pegadinhas**: só o que o próprio material aponta (ex.: apêndice de erros). Sem confusões comuns vindas de fora.
4. **Recall**: pergunta + a citação que a responde, no mesmo formato de ponto. A citação é a resposta: cubra-a ao estudar. Pegadinhas e Recall entram no verifier; só Conceitos e Cai na prova (no modo full, Briefing e Glossário) entram na taxa de falha.
5. **Ficou de fora**: seções omitidas e o motivo.

## Stop conditions

- `source_path` não existe, não é `.md` ou está fora de `02-AREAS/fiap/` e `02-AREAS/concurso/materias/`: parar e reportar.
- `time_budget` fora de {30min, 2h, 1d, full}: parar antes de montar o nome.
- Source com menos de 300 linhas: parar e mandar ler direto.
- Falha acima de 20% (F4): falhou, reportar.
- Nunca editar o `source_path`.

## Failure modes

- Citação que não resolve: o ponto sai do digest e entra na conta de removidos. Mais de 20%: falhou.
- Fonte curta (menos de 300 linhas): parar; ler direto.
- Fonte que já tem seção de prioridade: ler só ela. Se a seção existe e foi ignorada, o digest está errado.
- Digest velho: se o `source_commit` do STUDY difere do `git log -1` atual do source, regerar; não reaproveitar.

## Quando NÃO usar

- Ingerir apostila nova: ingest-fiap-batch.
- Resumo de fonte ou diff para outra pessoa: [content-synthesis](../content-synthesis/SKILL.md).
- Explicar um conceito do zero a um aluno: Mestre, no Claude Chat.
- Cartões de revisão espaçada e concurso: fora do escopo; esta skill não cria cartão.

## Critério de sucesso

- [ ] `STUDY-<stem>-<time_budget>[-<focus-slug>].md` existe e tem `type: study-digest`.
- [ ] `study-digest-verify.py` sai 0 sobre o STUDY.
- [ ] `source_path` não mudou (`git diff --stat` vazio nele).
- [ ] Relatório com contagens de pontos (gerados, removidos, [hyp]), linhas lidas e taxa de falha.
