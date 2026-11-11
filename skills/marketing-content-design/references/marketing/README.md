---
kind: doc
title: "Marketing System"
description: "Sistema de 3 agentes para execução e distribuição de marketing pessoal"
version: "1.1.0"
updated: 2026-08-17
status: active
tags: [agents, marketing, claude, orchestration]
name: marketing-system-readme
type: doc
reviewed-scope: "checagem mecanica + semantica: 0/0 wikilinks resolvem; 3/3 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=doc, 6 secoes, 111 linhas; itens do pacote R16 resolvidos (13=C, 14=C, 15=C; letras = recomendacao do pacote, bloco vazio)"
reviewed-by: R17 (claude-sonnet; pacote R16)
reviewed: 2026-10-04
---

# Marketing System

Sistema de 3 agentes para **execução e distribuição** de conteúdo de marketing pessoal para Michel Csasznik.
Complementa os agentes de estratégia existentes (`marca-pessoal`, `estrategista-de-conteudo`, `designer-sites`) — não os substitui.

## Arquitetura

Só três arquivos declaram `kind: agent`. Os outros cinco são `kind: reference`: <!-- drift:ok: descreve o desenho de marketing de 2026-08-17, agentes ausentes em disco; decisão humana R16 -->
specs de modo, lidas pelo agente que as absorveu, não invocáveis.

```
signal (orchestrator)
├── anchor → marca + SOCIAL + YOUTUBE          → claude-opus-5-5 · medium
│            lê vox (SOCIAL), frame (YOUTUBE)
└── prism  → foto/vídeo + IMAGEM-IA + SITE + DOCUMENTO → claude-opus-5-5 · medium
             lê lens (IMAGEM-IA), canvas (SITE), folio (DOCUMENTO)
```

Duas ondas de consolidação, e é por isto que a árvore mudou duas vezes: **F2.d**
mandou `vox`+`frame` → anchor, `lens` → prism, `folio` → canvas; **R2** mandou
`canvas` → prism e rebaixou canvas a spec. Quem só viu a primeira onda ainda
chama canvas de agente.

## Roteamento de Modelos

| Agente | Modelo            | Função                                      |
|--------|-------------------|---------------------------------------------|
| Signal | claude-opus-5-5 · medium | Orquestração e roteamento — delega, não produz |
| Anchor | claude-opus-5-5 · medium | Marca, posicionamento, estratégia, calendário + posts/threads + YouTube |
| Prism  | claude-opus-5-5 · medium | Lightroom exact values, DJI shot lists, prompts DALL-E 3, site e documento HTML |

A tabela reflete o frontmatter, que é o que roda. Signal em opus·medium não é <!-- drift:ok: descreve o desenho de marketing de 2026-08-17, agentes ausentes em disco; decisão humana R16 -->
anomalia: `model-routing` §Padrão custo-efetivo prescreve premium para quem
orquestra, e o custo de um roteador está na rota errada, não no texto que ele
escreve.

Cada agente declara perfil, políticas e handoff no próprio arquivo. `anchor`
declara perfil **por atividade**, porque faz estratégia (`deep`) e redação
(`standard`) no mesmo agente. Um arquivo tem um `model-profile` só, então o
frontmatter é o default (`deep`) e o tier real é escolhido no despacho: Signal
delega SOCIAL e YOUTUBE com `model: sonnet`. Regra 6 abaixo.

## Camada no ecossistema

```
ESTRATÉGIA (agentes existentes)     →    EXECUÇÃO (Marketing System)
────────────────────────────────         ──────────────────────────
marca-pessoal-monetizacao-solo      →    Signal → Anchor
estrategista-de-conteudo            →    Signal → Anchor / Fullstack <!-- drift:ok: descreve o desenho de marketing de 2026-08-17, agentes ausentes em disco; decisão humana R16 -->
designer-estrategista-de-sites      →    Signal → Prism (MODO SITE)
criacao-visual-fotos-videos         →    Signal → Prism
```

## Como invocar

Inicie pelo Signal:

> Executar a skill `content-analysis` — `[intenção]. Contexto: [tema / campanha / conteúdo de referência].`

Ou invoque agentes diretamente se souber o modo:

> Executar a skill `content-creation` — `thread: por que IA muda concursos públicos`
> Executar a skill `marketing-content-design` — `one-pager: apresentação de perfil tech para recrutadores`
> Executar a skill `marketing-content-design` — `capa: X — tema sobre produtividade com IA`

## Docs do Sistema

| Arquivo | Propósito |
|---|---|
| `08-ARCHIVE/system/2026-10-11--marketing-docs/progress.md` | Arquivado em 2026-10-11 (descrevia agentes aposentados) |
| `docs/standards.md` | Padrões de voz, paleta, critérios de qualidade |
| `docs/constitution.md` | Princípios e limites do sistema |
| `docs/adr/` | Decisões que afetam padrões ou arquitetura |

## Regras do Sistema

1. Signal é obrigatório para campanhas multi-agente (Anchor + Prism)
2. Nenhum agente inventa estratégia — executam briefing ou chamam agentes de estratégia externos
3. ~~`progress.md` atualizado ao final de cada campanha~~ — arquivado em 2026-10-11, ver `08-ARCHIVE/system/2026-10-11--marketing-docs/`
4. Contexto Michel (tech/AI, ADS/FIAP, marca solo) baked-in em todos os agentes — nunca pedir novamente
5. Promover ou rebaixar agente é mudar `kind`/`type` no frontmatter **e** esta
   página. `kind: reference` com `name:` continua sendo spec: `name` não promove
   nada, e ler só esse campo foi o que fez a última auditoria contar 4 agentes.
6. `model-profile` no frontmatter é **default**, não teto obrigatório. Agente que
   faz duas atividades de preço diferente resolve o tier no despacho — quem chama
   passa o modelo. Tabela de perfil por atividade sem override é documentação,
   não mecanismo: continua rodando tudo no valor do frontmatter.


---

> **Nota de origem (S12, 2026-08-23):** este README era a entrada ativa do
> marketing-system (`automation/agents/marketing-system/`), movido para cá como
> referência aposentada. As chamadas `@signal/@anchor/@prism` foram repontadas
> para as skills content-analysis/content-creation/marketing-content-design.
> Fluxo pendente de validação em runtime.
