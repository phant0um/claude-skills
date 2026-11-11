---
kind: reference
resolver-status: not-exposed  # symlink em ~/.claude/skills e efeito fora do vault; expor so com aprovacao
name: wait-what
type: reference
version: "1.0.0"
title: "Skill: Wait What"
created: 2026-09-26
updated: 2026-09-26
status: active
owner: nexus
source: mattpocock/skills (wait-what) + Poteto (prompt indireto)
tags: [clarity, ste, ubiquitous-language]
description: "Spec do MODO CLARIFICAR de [writing-for-agents](SKILL.md). Não é skill invocável. Reescreve explicação confusa em ASD-STE100 com os termos do GLOSSARY.md do projeto, quando existir, e aponta o que não fecha; serve também de prompt indireto ('reescreva o problema com as suas palavras'). Interrogar plano: grill-me; definir termo novo: domain-modeling."
reads: ["GLOSSARY.md"]
verifier:
  - "Uma ideia por frase, voz ativa, no máximo 20 palavras por frase."
  - "Todo termo de domínio vem do GLOSSARY.md do projeto (quando existir) ou está marcado como novo."
  - "Lacunas da explicação original listadas, não preenchidas por invenção."
parent: 04-SYSTEM/automation/skills/meta/writing-for-agents/SKILL.md
mode: "CLARIFICAR"
consolidated-by: orphan-audit-2026-10-05
reviewed-scope: "checagem mecanica + semantica: 0/0 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 6 secoes, 80 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---

# Skill: Wait What

> **Não é skill invocável.** MODO CLARIFICAR de [writing-for-agents](SKILL.md) — carregado por ela, não resolvido pelo router.


Reescreve uma explicação confusa até ela ficar verificável.

## Quando NÃO usar

- Plano que precisa ser desafiado: use `grill-me`.
- Termo novo sem definição: use `domain-modeling`.
- Texto para publicar: use a cadeia do workflow `escrita`.

## Protocolo

1. Leia o `GLOSSARY.md` do projeto, se existir. Use só os termos dele. Repo com
   `GLOSSARY-MAP.md`: siga o mapa até o `GLOSSARY.md` do contexto certo.
2. Reescreva a explicação em ASD-STE100:
   - uma ideia por frase, até 20 palavras;
   - voz ativa, tempo presente;
   - um termo por conceito, sem sinônimo rotativo;
   - pronome só com referente único.
3. Liste o que a explicação original não diz: causa, condição, número,
   dono, ordem dos passos. Não preencha a lacuna por conta própria.
4. Termo usado que não está no `GLOSSARY.md`: marque `[termo novo]` e
   sugira `domain-modeling`.
5. Feche com uma frase: "O problema é X; falta saber Y."

## Prompt indireto

Antes de corrigir o que o agente fez, peça: "Reescreva o problema com as suas
palavras." Se a reescrita diverge da sua, o erro está no entendimento, não no
código. Corrija o entendimento primeiro.

## Saída

- Reescrita em STE.
- Lista de lacunas.
- Frase de fechamento.

## Completion

- [ ] Explicação reescrita em STE (uma ideia por frase, voz ativa, um termo por conceito).
- [ ] Lista de lacunas entregue, sem lacuna preenchida por conta própria.
- [ ] Termos fora do `GLOSSARY.md` marcados `[termo novo]`.
- [ ] Frase de fechamento "O problema é X; falta saber Y." presente.

## Failure modes

- **Preencher a lacuna**: inventar causa, número ou dono que o original não diz → liste como lacuna.
- **Sinônimo rotativo**: dois termos para o mesmo conceito na reescrita → escolha um e mantenha.
- **Corrigir código antes do entendimento**: pular o prompt indireto → peça a reescrita do problema primeiro.
- **Plano no lugar de explicação**: usar esta skill para desafiar plano → plano vai para `grill-me`.
