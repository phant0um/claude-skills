---
origin: native
kind: skill-proc
resolver-status: exposed
name: article-publish
type: skill
version: "1.2.0"
created: "2026-08-16"
updated: 2026-10-25
status: active
owner: nexus
tags: ["writing", "blog", "publish"]
description: "Use when: publicar artigo já aprovado (status: ready) de 01-PROJECTS/blog/drafts/ no blog Hugo em phant0um.github.io. Converte wikilink, traduz frontmatter, roda gates e builda. Push exige confirmação humana. Escrever ou revisar o rascunho é `article-draft`."
invocation: "/article-publish <slug>"
triggers:
  positive:
    - publica o artigo
    - manda pro blog
    - sobe o post
    - deploy do blog
  negative:
    - escrever/rascunhar artigo (use article-draft)
    - artigo com status draft (falta liberação humana)
    - editar tema/layout do site (é trabalho de repo, não desta skill)
route: null
consumes: ["01-PROJECTS/blog/drafts/**"]
reads: ["01-PROJECTS/blog/**"]
writes: ["01-PROJECTS/blog/published/**", "01-PROJECTS/blog/drafts/**", "~/dev/phant0um.github.io/content/posts/**", "~/dev/phant0um.github.io/static/og/**"]
tools: ["read", "write", "bash"]
references:
  - "04-SYSTEM/scripts/blog-publish.py"
  - "04-SYSTEM/scripts/voice-lint.py"
  - "01-PROJECTS/blog/README.md"
verifier:
  - "blog-publish.py --check sai 0 (status ready, zero tag epistêmica, frontmatter completo)."
  - "voice-lint.py --strict sai 0."
  - "hugo --gc --minify builda sem erro."
  - "URL do post responde 200 após o deploy do Actions — uma checagem por slug publicado."
human_gate: true
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "2026-10-25: conferido contra disco com revisao shield (opus, somente leitura). Corrigidos: commit nao levava static/og/<slug>.png (post saia com card 404); wikilink sem alias barra (nao avisa); status published tambem passa; writes sem drafts/ e static/og. Conferido ok: gates de title/description/type/date futuro, voice-lint --strict, hooks block-add-all e block-push-main, hugo/gh no PATH, workflow de Actions. NAO executado: hugo build, gh run list, curl, blog-publish em draft real."
---

# article-publish — draft do vault → post no ar

Cadeia: `01-PROJECTS/blog/drafts/<slug>.md` → gates → `content/posts/<slug>.md`
no repo Hugo → commit → **push (confirmação humana)** → Actions → site.

Repo: `~/dev/phant0um.github.io` · Site: `https://phant0um.github.io/`

## Quando NÃO usar

1. **Artigo em `status: draft`**: falta liberação humana; o gate barra e está certo.
2. **Escrever ou revisar texto** → `article-draft`.
3. **Mexer em tema, layout, config do Hugo**: trabalho de repo, não de artigo.
4. **Republicar sem mudança**: se o conteúdo não mudou, não gere commit.

## Gates (ordem fixa, para no primeiro erro)

Cada gate é determinístico e sai != 0 quando falha. **Não contorne gate**: se
um barra, o conserto é no draft, nunca no script.

### 1. Conversão e privacidade

```bash
python3 04-SYSTEM/scripts/blog-publish.py <slug>.md --check
```

Barra: `status` fora de {`ready`, `published`} (`published` passa para republicação) · tag epistêmica remanescente · `title`/`description`
ausente · `type != article` · **`date` no futuro**.

O gate de data existe por incidente: um post com `date` de amanhã fez o Hugo
pular a página, o Actions concluir `success` e a URL devolver 404. Build verde
mede o processo; só o HTTP mede o artefato. Se você declarar data futura de
propósito (post agendado), o script barra — é o comportamento certo, porque
"agendado" e "publicado agora" não podem sair pelo mesmo comando.

Wikilink cujo alvo não está publicado: **com alias descritivo** avisa e vira texto puro; **sem alias**, ou com alias que só reescreve o nome da nota, **barra** (o nome da nota iria a público). Tabela de 4 casos em `01-PROJECTS/blog/README.md`. Default fechado: nota privada nunca vaza como link. Cada aviso merece leitura. Se o parágrafo perde sentido sem o link,
volte ao draft e reescreva.

### 2. Voz

```bash
python3 04-SYSTEM/scripts/voice-lint.py 01-PROJECTS/blog/drafts/<slug>.md --strict
```

Registro A é autodetectado por `type: article`. `--strict` sai 1 só com `error`.

### 3. Build

```bash
python3 04-SYSTEM/scripts/blog-publish.py <slug>.md          # escreve de verdade
cd ~/dev/phant0um.github.io && hugo --gc --minify
```

Build quebrado = post não sai. Erro comum: shortcode inexistente, HTML mal
fechado dentro do Markdown.

## Publicação

### 4. Commit

Pathspec explícito. `git add -A` é bloqueado por hook e recolheria pendência de
outra sessão.

```bash
cd ~/dev/phant0um.github.io && git add content/posts/<slug>.md static/og/<slug>.png && git commit -m "post: <título>"
```

### 5. Push (gate humano)

Push é efeito externo público e **irreversível na prática** (o conteúdo é
indexado). O hook `block-push-main.sh` exige confirmação fora da string do
comando; a skill **não cria o sentinel**. Peça ao usuário:

```bash
touch ~/Obsidian/vault-michel/04-SYSTEM/.push-ok
```

Só então:

```bash
cd ~/dev/phant0um.github.io && git push origin main
```

### 6. Verificar no ar

```bash
gh run list --limit 1
curl -sS -o /dev/null -w "%{http_code}\n" https://phant0um.github.io/posts/<slug>/
```

Não declare publicado sem os dois: Actions `success` **e** HTTP 200. Deploy leva
~1 min após o push.

### 7. Arquivar o draft

```bash
git -C ~/Obsidian/vault-michel mv 01-PROJECTS/blog/drafts/<slug>.md 01-PROJECTS/blog/published/
```

Atualize `status: ready` → `status: published` e registre a URL no frontmatter
(`url:`). O draft vira registro do que foi publicado, não cópia viva; a fonte
de verdade do site é o repo Hugo.

## Saída

Reportar: slug · gates (cada um pass/fail com evidência) · avisos de wikilink e
o que foi feito com eles · SHA do commit · conclusão do Actions · HTTP da URL ·
path do draft arquivado.

## Failure modes

- Declarar publicado sem checar HTTP. Actions verde e site 404 coexistem — a causa mais comum é `date` no futuro, hoje barrada no gate 1.
- Publicar N artigos e checar o HTTP de um só. Cada slug tem o seu; o deploy é comum, o artefato não.
- Editar o script para calar um gate em vez de corrigir o draft.
- Criar o sentinel de push no lugar do humano.
- Deixar o draft em `drafts/` após publicar; na próxima rodada republica.
- Wikilink virado texto puro deixando o parágrafo truncado, e ninguém leu o aviso.

## Completion

Critério de aceite (espelha `verifier:`), por slug:

- [ ] `blog-publish.py <slug>.md --check` sai 0.
- [ ] `voice-lint.py --strict` no draft sai 0.
- [ ] `hugo --gc --minify` builda sem erro.
- [ ] Push feito só depois do sentinel criado pelo humano.
- [ ] `gh run list` mostra `success` e `curl` devolve 200 na URL do slug.
- [ ] Draft movido para `01-PROJECTS/blog/published/` com `status: published` e `url:`.
