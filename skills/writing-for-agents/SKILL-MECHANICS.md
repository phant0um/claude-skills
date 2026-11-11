---
origin: native
type: reference
status: active
version: "1.0.0"
kind: reference
parent: "[writing-for-agents](SKILL.md)"
resolver-status: not-exposed
name: skill-mechanics
description: "Branch específica de skill de writing-for-agents: frontmatter, escolha de invocação e router skill."
updated: 2026-08-30
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisao 2026-10-25: papel de router skill aponta para moc-skills.md (ROUTER.md e index.md nao cumprem); contradicao sobre description de skill user-invoked removida. NAO conferido: regras do vault (resolver-status + symlink via check-skill-exposure.py; r1:trigger-first) ainda nao documentadas aqui."
---

# Mecânica de skill

Branch específica de [writing-for-agents](SKILL.md):
o que muda quando o documento é uma skill. Todo o resto da redação é a referência
universal no SKILL.md.

## Invocação

Duas escolhas, trocando entre as duas cargas:

- **Model-invoked** — mantém `description`, então o agente dispara sozinho e outras
  skills alcançam. Você continua podendo digitar o nome: model-invocation *inclui*
  o alcance do usuário; description só adiciona descoberta pelo agente, nunca
  remove a do humano. A description é o context pointer de topo da skill, forçado a
  ficar carregado sempre: context load permanente em troca de descoberta. Skill
  model-invoked cujo conteúdo é todo reference também serve de casa para reference
  compartilhada — outra skill a invoca, então material de várias vive num lugar só.
  Mecânica: omitir `disable-model-invocation`, escrever description voltada ao
  modelo carregando as branches de trigger (as regras de pointer valem inteiras).
- **User-invoked** — tira a description do alcance do agente: só o humano digitando
  o nome invoca, e nenhuma outra skill alcança. Context load zero, mas gasta
  cognitive load: você é o índice que lembra que ela existe. Mecânica:
  `disable-model-invocation: true`; a description vira voltada ao humano — resumo
  de uma linha, listas de trigger removidas.

Escolha model-invocation só quando o agente precisa alcançar sozinho, ou outra
skill precisa. Se só dispara na mão, faça user-invoked e não pague context load.

Reference compartilhada que duas skills user-invoked precisam não cabe em nenhuma
das duas: sem description, nenhuma dispara a outra. Empurre para arquivo simples
fora do sistema de skills.

## Split por invocação

O corte por invocação (o corte por sequência vive no SKILL.md): separe uma skill
model-invoked quando existir **leading word distinta** que deva dispará-la sozinha
(palavra de trigger que você de fato usa nos prompts), ou quando outra skill
precisar alcançá-la. Você paga context load pela nova description sempre-carregada,
então esse alcance independente tem que valer.

## Router skill

Quando skill user-invoked se multiplica além do que você lembra, essa cognitive
load empilhada se cura com **router skill**: uma skill user-invoked que nomeia as
outras e diz quando pegar cada uma — um item para lembrar em vez de muitos. Ela só
consegue sugerir, nunca disparar: skill user-invoked tem a description fora do contexto do agente, então
nada além do humano a alcança.

No vault, o índice de skills é `04-SYSTEM/automation/agents/_index/moc-skills.md`. `04-SYSTEM/ROUTER.md` roteia tarefas, não lista skills, e `~/.claude/skills/index.md` só lista Graphify e Wizard; nenhum dos dois é router skill.
