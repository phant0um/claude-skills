---
origin: native
kind: skill-proc
resolver-status: exposed
name: voice-registers
type: skill
reviewed-scope: "Colisao de trigger [ALTO] resolvida na raiz (2026-09-02). voice-registers e skill de AUDITORIA ('revisar VOZ de artefato persistido') mas anunciava 3 gatilhos de PRODUCAO: 'escrever conceito', 'gerar thread', 'escrever skill'. Eram a causa das colisoes com content-creation (thread), content-design (escrever pagina/conceito) e writing-for-agents/skillify (escrever skill) — nao o inverso. Os 3 removidos; os casos ficam cobertos por content-design (desc ja cita conceito, gatilho 'escrever conceito' adicionado la), content-creation ('thread') e writing-for-agents ('criar skill', 'editar SKILL.md'), entao nenhum caso ficou orfao. Adicionados 2 negativos de roteamento (producao e estrutura). Medicao: script de overlap de tokens sobre os 13 skill-proc de content/."
reviewed-by: claude-opus-5
reviewed_by: claude-opus-5-5
review-scope-security: "saida-de-quarentena 2026-09-25 (padrao de 7c024143c anti-over-engineering e 0afe7a456 agent-fault-debug): skill em uso ativo — nucleo da F2 de workflows/portas/escrita.md, 3 runs registradas em .escrita-state.json; scan-external-skill.py ok (0 findings); R8: source_repo vercel/eve na allowlist e analysis_digest confere com source_analysis (sha256 recalculado)"
reviewed: 2026-09-25
version: "2.3.0"
description: "Use when: revisar VOZ de artefato persistido antes de salvar/publicar (concept, x-thread, skill, doc, apostila, texto externo curto: comentário de GitHub, corpo de PR, resposta a revisor) — registrar auditivo (AI-slop, palavras-banidas, tom) e rodar `voice-lint.py`. NÃO confundir com [content-design](../content-design/SKILL.md) (que cuida de ESTRUTURA: front-load, 1 ideia/frase); voice-registers é só camada de voz, não de forma."
triggers:
  positive:
    - "revisar voz e tom do texto"
    - "registro de voz"
    - "tom do texto"
    - "revisar texto antes de publicar"
    - "auditar escrita"
    - "ai-slop"
    - "deslop"
    - "texto robótico"
    - "palavras-banidas"
    - "texto genérico"
    - "humanizar texto"
    - "humanizer"
    - "parece escrito por IA"
  negative:
    - "artefato transitório (scratch, /tmp) que não vai ser publicado — rascunho de comentário/PR no scratch entra, ver §Texto externo curto"
    - "texto já aprovado sem revisão de voz"
    - "escrever o texto do zero — esta skill audita voz, não produz (conceito/nota: content-design; post/thread/copy: content-creation; SKILL.md e doc de agente: writing-for-agents)"
    - "estrutura de leitura: front-load, 1 ideia/frase, corte (use content-design-review)"
reads: []
writes: []
calls:
  - content-design
updated: 2026-09-25
status: active
source_repo: vercel/eve
analysis_digest: sha256:08771763c095d349b649f105eee234adcea1b2e0b0dce2dc7d6443a64631de3d
source_analysis: 03-RESOURCES/sources/github/p0/vercel-eve.md
analysis_digest_rebaselined: 2026-09-02
analysis_digest_rebaseline_reason: "Digest anterior (ffee072d) fixava a nota de 2026-08-09. Ela foi reescrita duas vezes depois: 9e49125d4 (2026-08-11, 141 docs P0 no template repo-audit) e 01447dae2 (2026-08-12, fatia de pipeline). Diff 0ea30a006..HEAD conferido: mudou template (secoes obs/interp/acao), stars 4500->4547 e pushed_at; a tese que justificou a importacao — valor no human-writing, modo Detect de AI-slop, classificacao Adaptar/P2 — esta preservada e ampliada, nao contradita. Rebaseline sobre a nota de 2026-08-12."
consolidated-by: R3
voice-lint: exempt
---

<what-to-do>

## O que é

Camada de **voz** do texto persistido. `content-design` resolve **estrutura**
(front-load, 1 ideia/frase, concreto); este resolve voz. Rodar os dois:
estrutura primeiro, voz depois.

Duas metades, um só arquivo: **registro** (qual voz o destino pede — §Registros)
e **slop** (o que nenhuma voz aceita — §Catálogo, lista única; os registros apontam para ele).

Entrada: texto-alvo (path ou colagem) + destino (concept / x-thread / skill-doc /
apostila / nota). Saída: relatório `[padrão] [trecho citado] [dano] [correção]`
\+ contagem por padrão. **Modo Detect: não reescreve.** Limpeza só com
autorização explícita (passo 8 do Procedimento).

**Proibido emitir "AI score"** ou % de confiança: critério é padrão nomeado com
evidência literal, nunca número.

## Quando NÃO usar

1. **Texto curto (<3 frases) sem tese** — catálogo não aplica; responda "fora de escopo" em 1 linha. Exceção: texto externo curto (§Texto externo curto) — curto, mas publicado.
2. **Código de produção** — `fallback-like code` é regra de prosa/docs, não auditoria de runtime.
3. **Citação literal de fonte** (lei, edital, citação de autor) — não tocar; auditoria é de autoria própria.
4. **Sem intenção de persistir** — `.raw/`, `00-INBOX/clippings/`, transcript, output de conversa. Comentário de GitHub, corpo de PR e resposta a revisor **persistem**: ficam publicados com o seu nome. Rascunho deles no scratchpad entra.
5. **Pedido de "AI score"/% de chance de ser IA** — recusar.

## Registros

Escolha pelo destino do texto. **Um texto = um registro.** Misturar registro é o
erro mais comum.

| Registro | Corpus | Modelo | Frase-teste |
|---|---|---|---|
| **A** | `03-RESOURCES/concepts/`, `sources/`, resumo, entity | Karpathy | "Isso poderia ser o contrário?" |
| **B** | `06-GENERATED/x-thread/` | Thariq | "Essa frase funciona sozinha?" |
| **C** | skill, rulebook, `CLAUDE.md`, `AGENTS.md`, ADR, README | Boris | "Cabe numa tela?" |

### Registro A — Nota / concept (Karpathy)

**A1. Tese não-óbvia obrigatória.** Negue a linha 1. Se a negação não poderia ser verdade, é definição, não tese — reescrever.
- ❌ "O harness é o conjunto de prompts, tools e memória do agente."
- ✅ "O harness é a política efetiva, não o prompt. Trocar harness muda mais resultado que trocar modelo."

**A2. Uma ideia carrega o peso.** Máx 3 bullets em "Argumentos principais". Cinco bullets paralelos = três são preenchimento. Promova o mais forte a prosa, corte o resto.

**A3. Bloco `## O que ainda não sei` obrigatório** em concept page. É a humildade confiante virando campo, não tom. Uma a três linhas. Mapeia direto na tag `[hyp]`.

**A4. Teste microgpt.** Não explica em 3 frases + 1 exemplo mínimo → tag `#nao-entendi-ainda`. Não fingir profundidade com abstração.

**A5. Léxico:** §Catálogo item 3 (palavras-banidas) e item 4 (puffery).

**A6. Opinião direta, incerteza marcada.** "Acho que", "suspeito que" são permitidos e desejáveis — desde que a tag epistêmica (`[obs]`/`[interp]`/`[hyp]`) acompanhe. Hedge sem tag é ruído; opinião com tag é sinal.

### Registro B — X thread (Thariq)

**B1. Tweet 1 = aforismo.** ≤2 linhas. Contraste ou tríade. Sem preâmbulo.
- ✅ "Everyone moved from loops to graphs. Nobody priced the graph."

**B2. Último tweet *de conteúdo* = tríade paralela**, citável fora da thread. Forma: três termos, mesma estrutura sintática.
- Modelo: `thin prompts, thick artifacts, thin skills`
- Um tweet de distribuição (link do artigo + hashtags) pode vir **depois** dele e não conta como fecho. A tríade tem que ser o último tweet que argumenta; o linter não mede isto, você mede.

**B7. Thread que acompanha artigo publicado leva o link no corpo.** `source_article` no frontmatter é proveniência interna e ninguém que lê a thread o vê. Link e hashtags vão num tweet próprio, o último. Enquanto o artigo não estiver no ar com HTTP 200, a thread não é postável — o link seria 404.

**B8. Bloco `## Editorial Notes` obrigatório** ao final do arquivo, fora da contagem de tweets. Registra: tema e por que ele · idioma e termos mantidos no original · fonte primária lida (e qual **não** foi usada) · cada benchmark atribuído à sua suíte · a lista de números com o que cada um verifica · ressalvas preservadas e em quais tweets · anti-overlap com threads anteriores · confiança separada entre números e generalização · pendência de publicação. É o que permite auditar a thread meses depois sem reabrir as fontes.

**B3. Corpo: 1 ideia por tweet, ≤3 frases.** Tweet que só anuncia o próximo → deletar e fundir.

**B4. Densidade concreta.** Nome próprio, número ou data em ≥50% dos tweets. Thread sem nenhum número é opinião, não report.

**B5. Proibido:** §Catálogo item 5 (throat-clearing) e item 3, mais emoji decorativo e "A thread 🧵". Hashtag no tweet de distribuição (B7) é permitida; hashtag no meio do argumento, não.

**B6. Teste do mantra.** Ao menos 1 frase da thread funciona sozinha, sem contexto. Nenhuma funciona → não publicar, reescrever o hook.

### Registro C — Harness / instrucional (Boris)

**C1. Imperativo, 2ª pessoa.** `Do X. Don't Y.` Nada de "é recomendável que", "o agente deve idealmente".

**C2. Exemplo antes da explicação.** Par bom/ruim quando a regra é sutil. Mais de 1 parágrafo antes do 1º exemplo → cortar.

**C3. "Why this matters" ≤1 linha.** Ou corta. Doc instrucional não motiva, instrui.

**C4. Cabe em 1 tela.** Não cabe → são 2 docs, com ponteiro entre eles.

**C5. Regra checável mecanicamente sai do doc e vira hook.** Doc é probabilístico; hook é determinístico. Ver `04-SYSTEM/system/hooks/`.

**C6. Sem prosa de transição.** Tabela, lista, bloco de código. Parágrafo só quando o raciocínio não cabe em item.

**C7. Sem AI-slop:** §Catálogo item 2 (hedges/conectivos de encheção). Linter: `voice-lint.py` regra C7 (warn — corte é decisão editorial, não erro de fato).

## Passe de números (antes do catálogo)

Duas regras que nenhum padrão estético pega e que geram erro de fato. Rode-as no
passe 3 do Procedimento, junto com o passe de fontes.

**N1. Razão carrega o denominador na mesma frase.** Taxa, média, custo unitário e
"por X" só saem com o denominador escrito por extenso. Trocar o denominador
muda o fato, e nenhuma regra de voz detecta a troca.
- ❌ "custo por tarefa de US$ 0,028 a US$ 0,195"
- ✅ "custo por tarefa **bem-sucedida** de US$ 0,028 a US$ 0,195"

**N2. Números de fontes distintas não dividem frase.** Duas medições de suítes,
períodos ou tabelas de preço diferentes numa só frase convidam o leitor a tratá-las
como a mesma razão. Separe em frases (ou tweets) e nomeie a suíte em cada uma.
- ❌ "Entrada fresca custa 5x a cacheada, e o cache sai a 1/10 da taxa."
- ✅ "Na comparação da Composio, entrada fresca custava ~5x a cacheada." + "No benchmark de junho — outra suíte, outra tabela — a leitura de cache saiu a ~1/10."

**N3. Generalização carrega o n.** "Costuma", "geralmente", "usually",
"typically" afirmam frequência. Uma frequência precisa de amostra. Escreva quantos
casos você viu, ou afirme só os casos.
- ❌ "A static client's first call is usually a read." (n=2, comentário de 2026-09-24)
- ✅ "In the two runs I checked, the first call was a read."

Teste dos três: circule cada número e cada frequência. Denominador, suíte e n são
identificáveis sem sair da frase? Não → reescreva antes de qualquer passe estético.
Em modo externo o linter marca `GEN` (warn); ele não sabe o n, só força a pergunta.

## Catálogo de padrões (Detect)

Lista única — os registros acima apontam para cá. Para cada padrão: procure no
texto inteiro; ≥1 ocorrência → registre com trecho literal; nenhuma → "0
ocorrências" no relatório. Teste mecânico embutido em cada item.

Compilado de vercel/eve `human-writing` (Apache-2.0), oh-my-codex
`ai-slop-cleaner` e vercel-labs `writing-guidelines` [obs] — reescrito para PT-BR
e adaptado aos textos do vault [interp].

1. **Fallback-like code** (snippets em docs): código que mascara erro em vez de tratar — `catch {}` vazio, `?? "default"` que engole null sem decisão, `try { ... } catch { return fallback }` sem log nem rethrow. Classifique **masking** (engole a falha) vs **grounded** (fallback é decisão documentada). Só reporte masking.
**Antes de aplicar o item 2, leia esta distinção.** Ela decide se você corta ou
mantém, e errar aqui reverte revisão boa. **Hedge vazio** não tem referente:
apague e a frase diz o mesmo. **Escopo de validade** nomeia suíte, amostra,
período, versão ou condição sob a qual o dado vale; apague e a frase passa a
afirmar mais do que a fonte sustenta. O segundo é dado, não ruído, e é
obrigatório sempre que a evidência vem de uma medição específica.

| | Hedge vazio (corte) | Escopo de validade (mantenha) |
|---|---|---|
| Exemplo | "É importante notar que o piso domina a fatura." | "Naquela suíte, o piso × turnos acompanhou os tokens com R² 0,99." |
| Teste | apague: significado idêntico | apague: vira lei geral a partir de uma medição |
| Marcas | "vale ressaltar", "de certa forma", "pode-se dizer" | "naquele benchmark", "nessa amostra", "até a versão X", "nas 12 tarefas" |

Verbo importa junto: `prevê`, `prova`, `garante` afirmam mecanismo;
`acompanhou`, `foi compatível com`, `sobreviveu à troca de modelo` afirmam o que
foi observado. Use o segundo grupo quando o desenho for observacional ou de
passagem única. Corolário: **passagem única sem variância nunca vira "prevê"**.

2. **Hedges vazios e conectivos de encheção**: "é importante notar que", "vale ressaltar", "cabe destacar", "deve-se considerar", "em última análise", "não surpreendentemente", "como se sabe", "de certa forma", "praticamente", "além disso", "não apenas X, mas também Y", "em suma", "como vimos", "de maneira geral", "no que diz respeito a". Teste: apague a expressão; frase mantém o significado → é hedge vazio, remova.
3. **Palavras-banidas PT-BR**: "mergulhar" (delve), "fomentar" (foster), "alavancar" (leverage), "desbloquear" (unlock), "capacitar" (empower), "sinergia", "revolucionário", "game-changer", "paradigma", "poderoso", "transformador", "holístico", "robusto", "no cerne", "à medida que navegamos", "no mundo atual", "jornada", "dinâmico", "ecossistema", "inteligente" (adjetivo vago), "otimizar" (sem métrica), "vem ganhando espaço", "cada vez mais", "não é só X, é Y". Regra: cada ocorrência → substituir por palavra concreta ou cortar. Não banir em citação literal.
   **Equivalente EN** (texto externo em inglês): "delve", "leverage", "unlock", "empower", "synergy", "game-changing", "transformative", "paradigm shift", "robust", "powerful", "holistic", "seamless", "ecosystem", "journey", "in today's world", "gaining traction", "increasingly", "it's not just X, it's Y"; encheção: "furthermore", "moreover", "it's worth noting", "in conclusion", "with regard to". A lista canônica é a de `voice-lint.py` (`EN_HYPE`/`EN_VAGO`/`EN_SLOP`); esta linha é o resumo.
4. **Importance puffery**: frase que infla a importância do que acabou de dizer — "isto é crucial porque...", "o que torna isso ainda mais relevante", "um ponto fundamental", "não podemos subestimar". Teste: a frase seguinte já demonstra a importância? Se sim, corte a puffery.
5. **Throat-clearing** (aquecimento): abertura sem informação — "Neste artigo, vamos explorar", "Here's why", "Let's dive in", "À medida que o cenário evolui", "Antes de mais nada, é importante entender", "Nos últimos anos, temos visto". Teste: pule o primeiro parágrafo; texto começa igual → corte. Mesma falha que `content-design-review` R1: se o review já reprovou a abertura, cite o R1 e não conte de novo.
6. **Colon reveals**: promessa de explicação no lugar da explicação — "Há três razões para isso:" seguido de paráfrase, ou pergunta + dois-pontos + repetição. Teste: o conteúdo após os dois-pontos acrescenta dado novo? Não → reescreva como afirmação direta.
7. **Falsos grupos de três**: trios paralelos de empacotamento — "simples, eficiente e escalável", "rápido, seguro e confiável", "clareza, consistência e qualidade". Teste: cada item sobrevive sozinho com significado distinto? 2 de 3 são sinônimos/decoração → colapse.
8. **Repetição de tese** (restatement): a mesma tese dita 3+ vezes (abertura, meio, conclusão) com zero dado novo. Teste: sublinhe a tese em cada parágrafo; 2ª e 3ª ocorrências sem fato/contra-argumento → marque "repetição; corte ou vire dado". Parente de `content-design-review` R5 (duplicata entre parágrafos): R5 pega parágrafo repetido, este pega a tese reescrita com outras palavras.
9. **Estrutura genérica**: "Introdução → 3 pontos igualmente longos → conclusão que repete" aplicável a qualquer assunto. Teste: troque o assunto por outro e o texto continua igual? → genérica. Correção: realocar peso para o ponto com mais evidência; cortar seções simétricas sem conteúdo próprio.
10. **"Fácil/simples" não justificado**: chamar de fácil/simples o que exige trabalho — "basta configurar", "é simples entender". Regra: não rotular esforço alheio; troque por instrução concreta.

### Portados de blader/humanizer (11–19)

Nove padrões de [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup, via `blader/humanizer`) que faltavam aqui. O repo **não** está instalado: seria um quarto registro em inglês competindo com A/B/C, e a consolidação de 2026-08-10 existe para não ter lista duplicada. Clipping da fonte em `08-ARCHIVE/approved/2026/05/`. Os padrões dele que já estavam cobertos (throat-clearing, hedge, puffery, rule-of-three, conclusão genérica, sycophancy, artefato de chatbot) ficaram como estão — não duplicar numeração.

11. **Fuga da cópula**: "configura", "constitui", "serve como", "apresenta-se como", "funciona como" no lugar de "é" e "tem". Teste: a frase aceita "é"/"tem" sem perder informação? Sim → troque. Verbo pomposo é o marcador mais barato de texto de LLM.
12. **Ciclagem de sinônimos**: o mesmo referente reescrito a cada menção — "o harness… o andaime… a camada… o invólucro". Prosa técnica repete o termo exato; variar confunde quem procura o conceito. Teste: liste as menções do referente; >2 formas diferentes sem motivo → padronize numa.
13. **Falsas amplitudes**: "de X a Y" onde X e Y não são extremos de nenhum eixo — "do prompt de sistema ao futuro da engenharia". Teste: existe uma escala real entre os dois? Não → liste os itens direto.
14. **Excesso de em-dash**: travessão como pontuação padrão em vez de vírgula ou ponto. **Mecânico:** `voice-lint` regra `H14`, teto 30 por mil palavras em A e B (warn); C tem `C7-emdash`, mais apertado. Backlog medido em 2026-08-29: 297 de 981 arquivos acima do teto — número declarado de propósito, para ninguém confundir warn silencioso com corpus limpo.
15. **Excesso de negrito**: negrito em tudo não destaca nada. **Mecânico:** regra `H15`, teto 35 por mil palavras (warn); backlog 73 de 981. Regra editorial: negrito marca a tese e os termos que o leitor vai procurar depois, não ênfase de leitura.
16. **Listas com cabeçalho inline**: "**Performance:** a performance melhorou" — o rótulo repete o conteúdo. Teste: apague o rótulo; a frase perde algo? Não → vire prosa corrida.
17. **Títulos em Caixa Alta De Cada Palavra**: "Negociações Estratégicas E Parcerias". Em PT-BR, só a primeira palavra e nomes próprios.
18. **Anúncio de si mesmo (signposting)**: "Aqui está o que você precisa saber", "vamos ao que interessa", "dito isso". Parente do item 5, mas no meio do texto e não na abertura. Teste: a frase transporta informação nova? Não → corte e comece pelo conteúdo.
19. **Cabeçalho fragmentado**: heading de uma palavra seguido de uma frase que repete o heading — "## Custo" + "O custo importa." Ou o heading trabalha (e a primeira frase avança), ou some.

## Regras duras de não-invenção

1. **Nunca afirmar fato sem fonte.** Número, data, lei, norma, citação, resultado de prova → exigem fonte citada no próprio texto. Sem fonte → marque `[não-verificado]` no relatório; a afirmação NÃO sai publicada.
2. **Nunca inventar exemplo, medição ou dado** para "ilustrar". Exemplo hipotético só rotulado "exemplo ilustrativo" e nunca com número inventado.
3. **Nunca inferir resultado que só a execução prova** (CI, banca, edital, teste): não afirmar "a banca cobra X" sem o edital aberto; não afirmar "o teste passa" sem rodar.
4. **Citação literal**: conferir palavra a palavra com a fonte; alteração = aspas + colchetes. **Tradução entre aspas é violação desta regra.** Aspas dizem "estas foram as palavras". Se a fonte disse outra coisa em outra língua, as palavras entre aspas não existem. Duas saídas: cite no idioma original entre aspas (tradução opcional fora delas), ou parafraseie sem aspas.
   - ❌ `The output said the errors "seem to have been temporary".` — a fonte era "Os erros de antes parecem ter sido temporários"
   - ✅ `The output said the earlier errors looked temporary.` ou `The output said: "Os erros de antes parecem ter sido temporários" (the earlier errors seem to have been temporary).`
5. Fato sem fonte é **violação de não-invenção**, prioridade 1, antes de qualquer padrão estético. Nada avança até esse passe fechar.
6. **Fato conferido é fato reaberto, não lembrado.** No passe de fatos, abra o artefato que sustenta cada afirmação (log, output de comando, diff, issue) e confira. Afirmação que você lembra mas não consegue reabrir sai do texto ou vira `[não-verificado]`. O caso real (2026-09-24): "started fine from the Dock" saiu num comentário publicado com o passe de fatos feito de memória; ninguém reabriu a fonte.

## Procedimento

0. **Entrada**: receba texto-alvo + destino. Confirme autoria própria ou revisão autorizada.
1. **Estrutura primeiro**: rode `content-design` (calls). Voz sobre estrutura torta gasta passe à toa.
2. **Registro**: identifique A/B/C pelo destino. Um só. Varra as regras do registro na ordem.
3. **Passe fatos**: sublinhe toda afirmação factual (número, data, nome, norma, resultado) e toda citação entre aspas. Cada uma: reabra a fonte agora (não-invenção 6) e confira; citação, palavra a palavra e no idioma (não-invenção 4). Sem fonte reabrível → `[não-verificado]`. Aplique N1–N3 (§Passe de números) e a distinção hedge × escopo de validade (topo do §Catálogo). Não avance com fatos pendentes.
4. **Passe catálogo**: percorra o texto inteiro na ordem 1→19. Para cada ocorrência registre `[padrão] [trecho literal] [dano] [correção]`. Não reescreva; só registre.
5. **Passe estrutura**: leia só headings + primeira frase de cada seção. Aplique os testes dos itens 8–9.
6. **Linter**: `python3 04-SYSTEM/scripts/voice-lint.py <arquivo>` — autodetecta registro por `type:` do frontmatter. Rascunho fora do vault sem `type:`: passe `--register A` (sem registro o linter sai 2, de propósito). `error` bloqueia; `warn` é para ler, não para ignorar em silêncio. Se precisar do que o linter cobre ou do modo externo, leia [cobertura-linter](references/cobertura-linter.md). `--strict` sai 0 também quando `files_judged: 0` (arquivo do vault com `type:` desconhecido ou ausente não é julgado, e isso é falso-verde): confirme na saída `files_judged >= 1` e `errors == 0`, conforme [cobertura-linter](references/cobertura-linter.md).
7. **Relatório**: ordene por severidade (1: não-invenção; 2: fato sem fonte; 3: repetição/estrutura; 4: demais padrões). Formato `[padrão] — trecho — dano — correção`. Feche com contagem por padrão ("0 ocorrências" explícito).
8. **Saída**: entregue o relatório. **Não edite o arquivo** sem autorização explícita. Se a autorização para limpar veio, leia [passes-limpeza](references/passes-limpeza.md).

## Texto externo curto

Comentário de GitHub, corpo de PR, resposta a revisor, corpo de issue. Curto,
mas publicado com o seu nome e fora do alcance de correção. Registro A. Aplique:

1. **Não-invenção inteira**, com 4 (tradução entre aspas) e 6 (fato reaberto)
   rodados no rascunho, não de memória.
2. **N3**: frequência sem n sai ou ganha o n.
3. **Catálogo** itens 2–5 no idioma do texto (EN: §Catálogo item 3, equivalente EN).
4. **Linter**: `python3 04-SYSTEM/scripts/voice-lint.py --strict --register A <rascunho>`.

Não se aplicam: A2, A3 e tag epistêmica (`[obs]`/`[hyp]` é notação interna; em
texto público a incerteza vai por extenso, como no artigo).

## Exemplares (`voice: gold`)

Um por registro, checados limpos pelo linter:

| Reg | Arquivo |
|---|---|
| A | loop-engineering-patterns |
| B | `06-GENERATED/x-thread/2026-08-03-ai-weekly-mcp-operations.md` |
| C | [contradiction-sweep](../contradiction-sweep/SKILL.md) |

O exemplar B mora em `06-GENERATED/` — saída gerada, fora do commit. Este
ponteiro é a cópia que sobrevive; se o arquivo for regenerado, escolha outro
pelo linter e atualize a linha.

## Relação com outras camadas

- **ingest-rulebook** (ingest-rulebook) — validade de página de ingest (frontmatter, corpo, links). Ortogonal: rulebook diz se a página é válida, esta diz se está bem escrita.
- **Caveman** comprime a *conversa*. Esta skill trata do *artefato salvo*. Ortogonais.

</what-to-do>

## Failure modes

- **Auditoria que reescreve**: modo Detect não edita; reporte como falha.
- **"AI score" emitido**: proibido; critério é padrão nomeado com trecho citado.
- **Catálogo por amostragem**: texto inteiro; trecho pulado = relatório incompleto.
- **Fato sem fonte tratado como estético**: não-invenção bloqueia publicação.
- **Registros empilhados**: escolha um e refaça.

## Completion

Critério de sucesso: todos os itens abaixo marcados.

- [ ] Registro identificado pelo destino e aplicado de forma consistente; nenhum registro empilhado.
- [ ] Relatório lista cada padrão do catálogo com contagem: ≥1 ocorrência com trecho literal OU "0 ocorrências" explícito.
- [ ] Toda afirmação factual tem fonte citada ou está marcada `[não-verificado]`, conferida reabrindo a fonte, não de memória.
- [ ] Toda citação entre aspas bate palavra a palavra com a fonte, no idioma da fonte; nenhuma tradução entre aspas.
- [ ] `voice-lint.py` rodado; nenhum `error` pendente.
- [ ] Nenhum trecho do texto-alvo foi modificado durante a auditoria (modo Detect).
- [ ] Se houve limpeza: texto limpo re-auditado; 0 ocorrências nos itens 1–19; 0 fatos sem fonte.
- [ ] Nenhum "AI score" foi emitido.

Falhou qualquer item → reporte o item; não declare done.
