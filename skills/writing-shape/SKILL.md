---
name: writing-shape
description: "Use when: transformar material bruto (pile) em artigo, escolhendo o grão — parágrafo a parágrafo ou beat a beat. Molda o SHAPE do texto; não decide destino nem revisa voz. Sem pile ainda, use `writing-fragments`; rascunho com destino use `article-draft`; voz use `voice-registers`."
trigger: ["escrever artigo", "rascunho", "redação", "moldar texto", "shape this into an article", "structure my draft", "turn fragments into a piece"]
---

<what-to-do>

The user has passed (or will pass) a markdown file of raw material. Treat it as the input pile — anything from a tidy list of fragments to a wall of unstructured prose to a transcript. The format does not matter. Read it end-to-end before doing anything else.

Then run a shaping session that produces a separate article document. This is **exploit**: the exploring is done, the pile is fixed — commit to a structure and mine the pile to fill it. Do not edit the raw material file — it is read-only to this skill.

If the user did not say where to save the article, ask once and remember the path.

If there is no pile yet — the user has only a wish to write — stop and hand off to `writing-fragments`. Mining is that skill's job, not this one's.

</what-to-do>

<supporting-info>

## Quando NÃO usar

- **Sem pile** — o usuário ainda não tem material reunido: `writing-fragments` (explore) produz a pile que esta skill (exploit) consome.
- **Material sem substância** (dump de links sem tese) — shape não cria conteúdo; síntese é `content-synthesis`.
- **Saída que precisa ser fact-checked** — shape molda; grounding factual é `cite-or-flag` ou `connection-finder`.
- **Rascunho com destino** (blog, registro definido) — `article-draft`.
- **Escrita de código/docs técnicos** — shape é para prosa; docs seguem convenções do repo.

Disambiguation: `writing-fragments` minera; `writing-shape` molda; `content-design` aplica as 5 regras a qualquer persistido; `content-design-review` reprova contra elas. Shape é o do meio.

## Escolha do grão (primeiro passo real)

Antes do loop, decida com o usuário em que grão o artigo cresce. A escolha muda o loop, não o resto:

- **Parágrafo** — cresce por blocos de argumento. Cada passo pergunta "dado esse parágrafo, o que o leitor precisa ouvir agora?". Bom para artigo argumentativo, doc técnico, post de tese.
- **Beat** — cresce por movimentos de jornada, choose-your-own-adventure: a cada passo oferecer 2–3 beats candidatos, o usuário escolhe um, e a escolha revela o que o próximo passo destrava. Bom para narrativa, ensaio, texto com virada.

Se o usuário não escolher, ofereça parágrafo por padrão e diga que beat existe.

## The loop

1. **Read the pile.** Read the input file in full. Form a sense of what's in it.
2. **Establish the prerequisites.** Settle with the user what the reader knows walking in — the concepts that are **grounded** from the start. Everything else must be grounded by a block before a later block can lean on it. See [Grounding](#grounding).
3. **Escolha o grão** (seção acima).
4. **Draft 2–3 candidate openings.** Each opening should imply a different thesis or angle — no grão beat, são *starting beats*, cada um uma entrada diferente no artigo. Show all of them; note what new concepts each one grounds. Force the user to pick or compose a hybrid. The chosen opening defines what the rest must do.
5. **Grow one unit at a time.** Write **only** the agreed block or beat to the article file, then stop. No grão beat, preview o que aquela escolha destrava — como se o usuário visse um pedaço do caminho adiante.
6. **Re-read the article file from disk.** Then offer the next 2–3 candidates — directions the piece could pivot to from where it now stands. Each must be reachable from the current grounded set; say what each one grounds. Argue about the form: parágrafo, lista, tabela, callout, citação, bloco de código. Cada escolha de formato é deliberada e defensável.
7. **Loop 5–6 até o fim natural.** O usuário decide quando acabou. No grão beat, acaba quando a jornada fecha — não quando a pile esvazia. Sobra de material é esperado; é o ponto de ter mais matéria-prima do que se usa.

## Grounding

Every **concept** has to be **grounded** before a block can lean on it: the reader either walked in knowing it or met it in an earlier block. A block that reaches for an ungrounded concept loses the reader — that is the one move the piece can't make. The unit is the concept, not the word for it: a block can lean on an idea the reader lacks even with no jargon in sight. Where a concept has a name — a **term** — grounding it means landing the idea and the term together.

A concept gets grounded one of two ways:

- **Prerequisite** — grounded before the opening. The reader brings it. Fixed at the start.
- **Introduced** — a block establishes it, and from then on it's grounded for the rest of the article.

So each block does two jobs: it **requires** concepts already grounded, and it **grounds** new ones. Keep a running list of what's grounded and update it each time a block lands.

No grão beat isso vira a mecânica da jornada: um beat candidato só é alcançável se tudo que ele exige já está grounded; escolher um beat que grounds X destrava todo beat que esperava por X. Ao oferecer próximos beats, todos devem ser alcançáveis do conjunto atual — e diga o que cada um grounds, para o usuário ver que caminhos abre.

O grande lever é o que vira prerequisite versus o que se grounds dentro da peça. Exija demais na entrada e você fecha a porta; grounds demais dentro e a abertura afoga em definições. Resolva isso com o usuário ao estabelecer prerequisites, e revisite sempre que um beat tentador exigir conceito que nada ainda grounded — o conserto é um bloco de grounding antes dele, ou promover o conceito a prerequisite.

Quando você perguntar "o que o leitor precisa ouvir agora?", um conceito ungrounded que o próximo movimento exige **é** a resposta: grounds ele primeiro, ou o movimento não acontece. É o gap-naming de [Pulling from the pile](#pulling-from-the-pile) um nível acima: lá falta material na pile; aqui falta fundação no artigo.

## O que é um beat

Um beat é um movimento da jornada. Faz uma coisa — arma uma cena, crava um ponto, faz uma pergunta, solta um aparte, vira o ângulo. E então para, deixando o leitor num lugar de onde o próximo beat pode pivotar.

O tamanho vem do que o movimento exige:

- Uma frase, se é só isso ("E aí nada aconteceu por três semanas.").
- Um parágrafo curto, se o movimento precisa de setup.
- Vários parágrafos, se o beat é vinheta, argumento ou exemplo autocontido.

Se um "beat" precisa de cinco parágrafos e três subtítulos, não é beat — são dois beats colados. Divida.

## Conversational feel

This is a grilling session inverted. In ideation, the question was "what are you actually noticing?" Here it's "what is this article actually arguing, and in what order does the reader need to hear it?" Push back. Refuse to let weak transitions slide. If a paragraph doesn't earn its place, cut it.

Specific moves to keep using:

- "What does this paragraph do for the reader that the previous one didn't?"
- "If I cut this, what breaks?"
- "Is this prose, or should it be a list? Why prose?"
- "This sentence is doing two jobs — split it or pick one."
- "The opening promised X. We've drifted to Y. Either re-thread it or change the opening."

## Pulling from the pile

Treat the raw material as a quarry, not a script. Pull a fragment, rework it to fit the surrounding block, and place it. A fragment may be split across multiple blocks, merged with another, paraphrased or quoted. The pile's job is to be mined; the article's job is to read as one voice.

If the pile lacks something the article needs, name the gap explicitly: "We need an example here and the pile doesn't have one — give me one now or we cut this section."

## Format arguments to actually have

When choosing how to render a block, weigh these tradeoffs out loud with the user, not silently:

- **Prose vs. list.** Prose carries argument; lists carry parallel items. If items aren't truly parallel, prose is better. If they are, a list is faster to scan.
- **Inline vs. callout.** Tips, warnings, and asides go in callouts (`> [!TIP]`, `> [!NOTE]`) — but only if they'd genuinely derail the main argument inline. Otherwise leave them inline.
- **Table vs. repeated structure.** If the same shape repeats 3+ times with the same fields, a table. Otherwise prose with bold leads.
- **Quote vs. paraphrase.** Quote when the original wording is the point. Paraphrase when only the idea matters.
- **Code block vs. inline code.** Multi-line, runnable, or illustrative → block. Single token or identifier → inline.

## Writing rhythm

Append one unit at a time; never write ahead. Re-read the article file from disk before every write — the user may have edited between turns. Never overwrite blindly. Se o usuário editar um bloco anterior de forma substantiva, deixe isso mudar o que vem depois. Se pedir "reescreve aquele parágrafo" ou "volta e tenta outro beat 3", edite aquele ponto no lugar e deixe o resto intacto.

## Lifecycle and structure chooser

Preserve capture/raw as read-only, create outline and draft separately, and
record published version/feedback only when supplied. Choose one structure when
it materially helps: SCQA for narrative decision, MECE/issue tree for
decomposition, JTBD for user need, experiment for testable uncertainty. Do not
stack frameworks as decoration.

## Out of scope

- Mining for new fragments that aren't in the pile (handle gaps as in "Pulling from the pile"; sessão de mineração é `writing-fragments`).
- Editing the raw material file.
- Publishing, formatting for a specific platform, or adding frontmatter the user didn't ask for.

## Citation-verify

Antes de afirmar fato com fonte, verificar contra CrossRef/OpenAlex/arXiv; sem match →
marcar `[não-verificado]`. Reforça grounding. Liga a `cite-or-flag`.

</supporting-info>

## Completion

- [ ] Grão escolhido com o usuário (parágrafo ou beat) antes do primeiro bloco.
- [ ] Artigo em 1 arquivo de rascunho com blocos acordados, lidos do disco antes de cada escrita.
- [ ] Cada bloco só se apoia em conceito grounded; lista de grounded mantida.
- [ ] Toda afirmação de fonte verificada (CrossRef/OpenAlex/arXiv) ou marcada `[não-verificado]`.
- [ ] Nenhum fragmento novo minerado fora da pile; raw material intocado.
- [ ] Estrutura escolhida só quando materialmente ajuda (uma framework, sem decoração).

## Failure modes

- **Escrever à frente**: gravar mais de um bloco por vez → escreva só a unidade acordada e pare.
- **Bloco sem grounding**: bloco usa conceito que nenhum bloco anterior fundamentou → volte e fundamente, ou corte.
- **Minerar fora da pile**: inventar fragmento novo para cobrir lacuna → nomeie a lacuna e peça material ao usuário.
- **Sobrescrever edição do usuário**: gravar sem reler o artigo do disco → releia antes de cada escrita.
- **Framework decorativo**: empilhar SCQA, MECE e JTBD → escolha uma, só quando ajuda.
