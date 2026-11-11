---
origin: native
kind: skill-proc
resolver-status: exposed
name: article-draft
type: skill
version: "1.2.0"
created: "2026-08-16"
updated: 2026-10-25
status: active
owner: nexus
tags: ["writing", "blog"]
description: "Use when: escrever artigo técnico longo para o blog a partir de material do vault (concept, source, decisão, erro corrigido). Monta rascunho em 01-PROJECTS/blog/drafts/ no registro A (Karpathy). Material bruto sem destino vai para writing-shape; thread para x-thread-weekly ou content-creation; publicar é `article-publish`."
invocation: "/article-draft <tema>"
triggers:
  positive:
    - escreve artigo sobre
    - artigo para o blog
    - rascunho de artigo
    - post técnico
    - transforma isso em artigo de blog
  negative:
    - thread do X (use content-creation; o digest semanal x-thread-weekly está pausado)
    - concept page (use ingest/concept; artigo é para público externo)
    - publicar artigo pronto (use article-publish)
    - doc de harness/skill (registro C, não A)
    - moldar pile em artigo sem destino definido (use writing-shape; esta skill exige destino blog)
    - peça curta de plataforma — post de X, carrossel, copy (use content-creation)
route: null
consumes: ["03-RESOURCES/concepts", "03-RESOURCES/sources", "06-GENERATED/tasks/lessons.md"]
reads: ["03-RESOURCES/**", "06-GENERATED/**", "01-PROJECTS/blog/**"]
writes: ["01-PROJECTS/blog/drafts/**"]
tools: ["read", "write", "grep", "bash"]
references:
  - "04-SYSTEM/automation/skills/content/voice-registers/SKILL.md"
  - "04-SYSTEM/automation/skills/content/content-design/SKILL.md"
  - "01-PROJECTS/blog/README.md"
verifier:
  - "Draft existe em 01-PROJECTS/blog/drafts/ com type: article e status: draft."
  - "voice-lint.py roda no draft e não retorna error (warn é decisão editorial)."
  - "Tese da linha 1 é negável; bloco '## O que ainda não sei' presente."
human_gate: false
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "2026-10-25: conferido contra disco com revisao shield (opus, somente leitura). Corrigidos: wikilink nao publicado sem alias BARRA o publish (blog-publish.py:284-289), nao vira texto puro; cadeia de escrita sem content-design-review; voice-registers.md inexistente (e voice-registers/SKILL.md) e alegacao de quarantine (status active); rota de thread para workflow pausado; tools sem bash; template sem date. Conferido ok: catalogo item 9, A1-A6, voice-lint --strict, paths de consumes/reads."
---

# article-draft — artigo técnico a partir do vault

Artigo de blog é **concept page estendida**: mesma voz Karpathy (registro A),
mesmo gate de tese não-óbvia. Difere no comprimento e no leitor: externo, sem
acesso ao vault, sem contexto das suas notas.

## Quando NÃO usar

1. **Thread do X** → `content-creation` MODO 9 para thread avulsa (registro B, Thariq); o workflow semanal `x-thread-weekly` está `status: paused`.
2. **Concept page** → o destino é `03-RESOURCES/concepts/`, leitor é você mesmo;
   artigo é para fora e não pode depender de wikilink.
3. **Doc de harness, skill, ADR** → registro C (Boris), não A.
4. **Publicar rascunho já pronto** → `article-publish`.
5. **Tema sem trabalho real por trás**. Artigo nasce de implementação, erro ou
   decisão. Resumo de documentação alheia não é artigo; é nota de source.

## Posição na cadeia

A ordem das skills é de escrita (linha
`article`), não daqui: writing-shape → **article-draft** → content-design →
content-design-review → voice-registers → article-publish. Esta skill escreve o rascunho; content-design
e voice-registers revisam depois. Qualquer trecho reescrito na revisão volta
pelo linter do passo 8.

## Entrada

Tema + material de origem. Se o usuário não apontar a origem, procure antes de
escrever: `03-RESOURCES/concepts/`, `sources/`, `06-GENERATED/tasks/lessons.md`,
decisões recentes. **Sem material, pare e diga**. Não invente experiência.

## Procedimento

### 1. Achar a tese

Uma frase que **poderia ser falsa**. Negue-a: se a negação é absurda, é
definição, não tese; procure de novo.

- ❌ "Agentes precisam de contexto bem gerenciado." (ninguém discorda)
- ✅ "Contexto grande piora o agente antes de melhorar. O gargalo é seleção, não capacidade."

Sem tese negável, **não há artigo**. Pare e reporte.

### 2. Levantar a evidência

Cada afirmação de consequência precisa de lastro: código que você rodou, erro
que você viu, número que você mediu, fonte que você leu. Liste antes de
escrever. Afirmação sem lastro sai do artigo ou vira dúvida declarada no bloco
`## O que ainda não sei`.

### 3. Estruturar

Ordem que funciona para artigo técnico longo:

| Seção | Papel |
|---|---|
| Abertura | Tese + o caso concreto que a produziu. Sem aquecimento. |
| O problema | O que quebrou, com detalhe suficiente para o leitor reproduzir |
| O que tentei antes | Caminhos descartados e **por quê**. É aqui que mora o valor |
| A solução | Mecanismo, não receita. Código curto e real |
| Trade-off | O que a solução custa. Artigo sem custo declarado é propaganda |
| O que ainda não sei | Obrigatório. Uma a três linhas |

Seção sem conteúdo próprio: corte (voice-registers §Catálogo item 9, estrutura genérica).

### 4. Escrever no registro A

Regras que valem aqui (detalhe em `voice-registers/SKILL.md` §Registro A):

- **A1** tese não-óbvia na abertura.
- **A3** bloco `## O que ainda não sei`, obrigatório, checado pelo linter.
- **A4** teste microgpt: não explica em 3 frases + 1 exemplo → marque
  `#nao-entendi-ainda` e não publique essa seção.
- **A6** opinião direta é desejável; incerteza precisa estar marcada.

**A2 (máx 3 bullets) não se aplica**: o linter só a mede sob a heading
"Argumentos principais", que artigo não usa. Delta documentado aqui em vez de
alterar a skill voice-registers (`status: active`, dono da voz).

### 5. Incerteza vira prosa, não tag

Draft pode usar `[obs]`/`[interp]`/`[hyp]` enquanto você pensa, mas o artigo
publicado **não os leva**; `blog-publish.py` bloqueia. Converta:

| Tag | Prosa |
|---|---|
| `[obs]` | afirmação direta (é o que você observou) |
| `[interp]` | "minha leitura é que…", "entendo isso como…" |
| `[hyp]` | "suspeito que…", "aposto que…, mas não testei" |

### 6. Wikilink é dívida

O leitor não tem seu vault. Todo `link` cujo alvo não esteja publicado **sem alias barra o publish** (`blog-publish.py`: o nome da nota iria a público como texto); com alias descritivo vira texto puro e avisa. Escreva como se não houvesse link: dê alias descritivo ou remova a referência, e o
parágrafo precisa fechar sozinho. Referência externa entra como URL normal.

### 7. Gravar

Path: `01-PROJECTS/blog/drafts/<slug>.md`

```yaml
---
type: article
status: draft          # draft -> ready libera a publicação
title: ""
description: ""        # 1 frase, vira o subtítulo e a meta description
tags: []
slug: ""               # vira a URL: /posts/<slug>/
date: YYYY-MM-DD       # o README do blog manda declarar; blog-publish.py carimba now() no destino
---
```

### 8. Verificar

```bash
python3 04-SYSTEM/scripts/voice-lint.py --strict 01-PROJECTS/blog/drafts/<slug>.md
```

`error` → corrija antes de entregar. `warn` → decisão editorial, reporte e deixe
o usuário escolher.

## Saída

Reportar: tese em 1 linha · path do draft · lastro de cada afirmação principal ·
resultado do voice-lint · o que ficou no bloco "não sei" · próximo passo
(revisão humana → `status: ready` → `article-publish`).

## Failure modes

- Tese que ninguém contestaria: artigo sem motivo para existir.
- Afirmação de consequência sem lastro, apresentada como fato.
- Seções simétricas preenchidas para parecer completo.
- Parágrafo que só faz sentido com o wikilink resolvido.
- `status: ready` marcado pela própria skill; quem libera é o humano.

## Completion

Critério de aceite (espelha `verifier:`):

- [ ] `01-PROJECTS/blog/drafts/<slug>.md` existe com `type: article` e `status: draft`.
- [ ] `voice-lint.py --strict` no draft sai 0; cada `warn` listado no relatório.
- [ ] Linha 1 é tese negável, e a negação dela foi escrita no relatório.
- [ ] `## O que ainda não sei` presente, com 1 a 3 linhas.
- [ ] Cada afirmação principal tem lastro nomeado no relatório (arquivo, comando ou fonte).
