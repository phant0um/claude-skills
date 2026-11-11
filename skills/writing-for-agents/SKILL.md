---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: writing-for-agents
description: "Use when: escrever ou editar qualquer documento que um AGENTE consome — SKILL.md, CLAUDE.md/AGENTS.md, arquivo de policy, doc alcançado por ponteiro. Trata a redação como alavanca de comportamento: pointer fraco é bug de variância, não de conteúdo. Diferente de [content-design](../content-design/SKILL.md) (estrutura de texto para HUMANO ler) e de [voice-registers](../voice-registers/SKILL.md) (voz); writing-for-agents é redação para consumo por modelo. skillify decide quando um workflow repetido vira skill, diagnose depura falha em execução e content-design-review audita texto para humano: redigir uma SKILL.md, consertar skill que não dispara e enxugar policy inchada é aqui."
triggers:
  positive:
    - "editar SKILL.md"
    - "editar CLAUDE.md"
    - "skill não dispara"
    - "policy inchada"
  negative:
    - "texto para humano ler (artigo, thread, resumo)"
    - "revisão de voz/tom (use voice-registers)"
consolidated-by: orphan-audit-2026-10-05 (absorveu wait-what como modo)
updated: 2026-10-25
effort: medium
reads: []
writes: []
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisao 2026-10-25: linha duplicada do ambiente fundida em Poda (sem hyp); CLAUDE.md sujeito a Autonomia; relacao com a porta escrita explicita. NAO conferido: description longa repete identidade do corpo (poda pendente); negativo contra hill-climb em skill nao dispara (trigger-eval 2/3); content-design sem negativo reciproco; evals/ fora do run-skill-evals."
---

> Adaptado de `mattpocock/skills` → `productivity/writing-for-agents` (2026-08-30).
> Mecânica específica de skill: [SKILL-MECHANICS](SKILL-MECHANICS.md).

Referência para qualquer documento que um agente consome. A embalagem muda; a
redação não. As mesmas alavancas tornam cada um previsível — porque o agente
repete o mesmo **processo** a cada run, não o mesmo output.

## Context pointer

**Context pointer** = referência que vive no contexto do agente, nomeia material
fora do contexto e codifica a condição de alcançá-lo. A `description` de uma
skill é um pointer. Uma linha do `CLAUDE.md` que nomeia um doc é o mesmo objeto.

**A redação do pointer, não o alvo, decide quando e com que confiabilidade o
agente alcança o material.** Alvo obrigatório atrás de pointer mal redigido é
bug de variância: afie a redação primeiro; inline o material só se afiar falhar.

Pointer faz dois trabalhos: dizer o que é o material e listar as **branches** que
devem disparar o alcance (branch = caso distinto que o doc trata). Cada palavra
de pointer sempre-carregado custa em todo turno — poda mais dura que o corpo:

- **Front-load da leading word.** O pointer é onde o disparo acontece.
- **Um trigger por branch.** Sinônimo que renomeia uma branch é uma branch escrita
  duas vezes. Colapse.
- **Corte identidade que o corpo já carrega.**

Pointer para case study, benchmark ou exemplo datado declara "ilustra, não garante"; se doc e ambiente divergem, vale o ambiente (ver §Poda).

## As duas cargas

- **Context load** — custo do material sempre carregado na janela: linha de
  `CLAUDE.md`, `description` de skill. Gasta token e atenção dispare ou não.
- **Cognitive load** — custo no humano: saber quais docs existem e quando pegar
  cada um. O humano é o índice. Não é custo a minimizar: é o preço da agência
  humana. Gaste onde julgamento humano importa; remova onde não.

Material alcançado só por pointer escapa da context load ao preço da linha do
próprio pointer. Material sem pointer nenhum roda inteiro na cognitive load.

## Hierarquia de informação

Dois tipos de conteúdo: **steps** (ações ordenadas) e **reference** (definições,
regras, fatos consultados sob demanda). Misturam livremente. A decisão é onde
cada peça senta na escada, ordenada por quão imediatamente o agente precisa:

1. **Step in-file** — o que o agente faz, em ordem. Camada primária.
2. **Reference in-file** — consultada sob demanda. Conjunto plano de pares
   (todas as regras de uma revisão no mesmo degrau) é arranjo legítimo, não smell.
3. **Reference disclosed** — empurrada para arquivo separado, alcançada por
   pointer, carregada só quando o pointer dispara.

Empurre de menos e o topo incha; empurre demais e você esconde o que o agente
precisa. Essa tensão é a decisão inteira.

**Progressive disclosure** = descer a escada para o topo continuar legível. Não é
primariamente otimização de token: é como a hierarquia se protege. Teste mais
limpo é branching — inline o que toda branch precisa, empurre atrás de pointer o
que só algumas alcançam. Num doc com steps, reference in-file que devia estar
disclosed enterra os steps e transforma atendê-los em cara-ou-coroa.

**Co-location** é o companheiro dentro do arquivo: a escada decide *quão fundo*,
co-location decide *o que senta ao lado*. Definição, regras e ressalvas de um
conceito sob um heading só. Teste: o doc deve ler como documentação escrita para
o agente. (Distinto de duplicação: aquela repete um significado em dois lugares;
espalhamento fragmenta um significado em muitos.)

**Sprawl** é o modo de falha: doc longo demais mesmo com toda linha viva e única.
A atenção rala no excesso. Cura é a escada — disclose reference atrás de pointer,
e split por branch ou sequência.

## Steps e critério de conclusão

Todo step termina num **completion criterion**. Duas propriedades:

- **Clareza** — o agente distingue done de not-done? Limite vago ("entendimento
  alcançado") convida **premature completion**: encerrar antes de terminar, com a
  atenção escorregando para *estar pronto*. Os steps visíveis ainda à frente
  puxam; a clareza do critério é a resistência. Defenda em ordem: **afie o limite
  primeiro** (local e barato); só se for irredutivelmente difuso *e* você observar
  a pressa, esconda os steps posteriores partindo a sequência. Esconder só funciona
  através de fronteira real de contexto (handoff ou subagente) — chamada inline
  deixa os steps no contexto e não limpa nada.
- **Demanda** — quanto exige. "Toda model modificada contabilizada" força trabalho
  minucioso onde "produza uma lista de mudanças" não. Demanda dirige o **legwork**
  (a escavação latente na redação, não escrita como step próprio) e não é presa a
  step: "toda regra aplicada" amarra um corpo de reference plana do mesmo jeito.

Os critérios mais fortes são checáveis **e** exaustivos.

## Quando fazer split

Split gasta uma das duas cargas. Só quando o corte paga:

- **Por sequência** — parta uma corrida de steps onde os posteriores tentam o
  agente a apressar o da frente. O inverso vale: fundir sequências expõe cada step
  ao que vem depois e convida premature completion.
- **Por invocação** — específico de skill: ver SKILL-MECHANICS.

## Leading words

**Leading word** = conceito compacto já presente no pretraining, com o qual o
agente pensa enquanto roda o doc (*lesson*, *fog of war*, *tracer bullets*).
Repetido como token, nunca como frase, acumula definição distribuída e ancora uma
região inteira de comportamento no menor número de tokens, recrutando priors que o
modelo já tem. Cunhar a sua funciona se você definir bem — mas palavra inventada
não recruta prior nenhum: você paga em tokens de definição o que uma palavra
pré-treinada dá de graça. Procure a palavra existente primeiro.

Ancora duas vezes. No corpo, **execução**: o agente busca o mesmo comportamento
toda vez que a palavra aparece. No pointer, **invocação**: quando a mesma palavra
vive nos seus prompts, docs e código, o agente liga essa língua compartilhada ao
material e o alcança com mais confiabilidade.

Cace oportunidades de refatorar com leading word. Tríade soletrada em três
lugares, pointer gastando uma frase para gesticular uma ideia — cada um é
passagem implorando para colapsar em um token:

- "rápido, determinístico, baixo overhead" → *tight* (um loop *tight*).
- "um loop em que você acredita" → *red*, virando gate difuso em estado binário
  observável (o loop fica *red* no bug, ou não fica).

Ganha duas vezes: menos token e gancho mais afiado. Assuma que todo doc carrega
reformulações que leading words aposentam. Vá achar.

**Negação** é o modo de falha ao lado: dirigir por proibição arrasta o
comportamento proibido para o contexto e o torna **mais** disponível, não menos.
*Não pense num elefante* — e o elefante é tudo que há. A proibição meio-lê como
instrução de fazer. Prompt o **positivo**: declare o comportamento alvo
("escreva comentário de uma linha") para o banido nunca ser dito. Proibição só
paga como guardrail duro impossível de frasear no positivo — e mesmo aí, pareie
com o alvo positivo.

## Poda

- Um significado, **uma fonte de verdade**. Duplicação custa manutenção, token, e
  infla a proeminência do significado acima do rank real na escada. (Inverso
  acidental da leading word, que repete o token de propósito, nunca o significado.)
- **O ambiente também é fonte de verdade** (scripts do `package.json`, layout de
  diretório, `--help`). Doc que o reafirma é **cache**: cópia de um lookup, só paga
  a carga quando o lookup é caro. Cacheie o que o agente não acha olhando — a
  convenção não escrita, a razão por trás da escolha, a pegadinha que nenhum config
  confessa. Deixe lookup de um arquivo/um comando para o ambiente, onde não
  envelhece.
- Cheque **relevância** linha a linha. Linha perde relevância por nunca incidir na
  tarefa (exposição pura, ou branch que devia estar disclosed) ou por envelhecer.
  Sem disciplina de poda, o destino padrão é **sedimento**: camadas rançosas que
  assentam porque adicionar parece seguro e remover parece arriscado.
- Cace **no-ops** frase a frase: instrução que o modelo já obedece por default paga
  carga para não dizer nada. O teste (muda o comportamento versus o default?) é
  relativo ao **modelo**, não ao leitor: duas pessoas discordando sobre um no-op
  discordam sobre o default, e resolvem rodando o doc, não debatendo. Quando a
  frase falha, delete a frase inteira em vez de aparar palavras. O teste também
  avalia leading word: palavra fraca demais para bater o default (*seja minucioso*
  quando o agente já é meio-minucioso) é no-op, e o conserto é palavra mais forte
  (*implacável*), não outra técnica.

## Quando NÃO usar

writing-for-agents é redação para consumo por **modelo**. Quando o leitor é
humano, a irmã certa:

- **Estrutura de texto para humano ler** (artigo, thread, relatório) →
  [content-design](../content-design/SKILL.md).
- **Voz e tom** → [voice-registers](../voice-registers/SKILL.md).

Editar `CLAUDE.md` segue antes a autonomia do próprio arquivo (§Autonomia e contrato 5): seção invariante só com aprovação humana.

Na porta `escrita`, esta skill é pré-passo para skill ou policy; content-design, review e voice-registers (registro C) continuam depois.

O corte é o **leitor**, não o formato: um `README` que só um humano lê segue
content-design; uma `description` de skill que só um agente lê segue esta.

## Modos absorvidos

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO CLARIFICAR** — [wait-what](wait-what.md) — explicação (sua, do agente ou de um doc) ficou confusa: reescrever em ASD-STE100 com os termos do GLOSSARY.md do projeto, quando existir.

## Completion

- [ ] Todo step do texto escrito termina num completion criterion checável e exaustivo.
- [ ] Um significado, uma fonte de verdade: nada duplicado nem reafirmado do ambiente.
- [ ] Texto podado linha a linha por relevância e no-ops.

## Failure modes

- **Critério vago**: limite do tipo "entendimento alcançado" → convida premature completion; afie o limite primeiro.
- **Esconder steps inline**: partir a sequência sem fronteira real de contexto → não limpa nada; use handoff ou subagente.
- **Cache do ambiente**: doc que reafirma `--help` ou layout de diretório → deixe o lookup para o ambiente.
- **No-op aparado**: frase que não muda o default mantida com palavras cortadas → delete a frase inteira.
- **Leitor humano**: aplicar esta skill a texto que só humano lê → use `content-design`.
