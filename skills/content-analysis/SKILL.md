---
kind: skill-proc
resolver-status: exposed
type: skill
name: content-analysis
input:
  required_fields: [task]
output:
  format: json|md
triggers:
  positive:
    - "analisar conteúdo"
    - "medir engajamento"
    - "auditoria de conteúdo"
    - "analisar performance"
    - "por que esse post não funcionou"
  negative:
    - "produzir conteúdo"
    - "sintetizar documentos"
    - "revisar voz/tom do texto"
    - "revisar estrutura do texto"
allowed_effects:
  - write 06-GENERATED/
  - write 03-RESOURCES/
  - read 04-SYSTEM/
forbidden_effects:
  - modify agent files
  - modify manifest
  - external-publish
reads: ["**"]
writes: ["06-GENERATED/**", "03-RESOURCES/**"]
version: 2.1.0
source_agent: signal
status: active
created: 2026-08-20
description: "Use when: medir/auditar desempenho de conteúdo publicado a partir de métricas coladas — diagnóstico com causa e mudanças testáveis. Produção vai para content-creation; voz para voice-registers; estrutura para content-design-review."
updated: 2026-10-25
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "2026-10-25: conferido contra disco com revisao shield (opus, somente leitura). Corrigido: /meta-learn e modo de evolve, nao skill. Conferido ok: rotas para content-creation, content-synthesis, voice-registers e content-design-review; @harden em hill; wikilinks; proveniencia signal.md @ 9e6c4ad61 e ADR-012. NAO alterado (menor): allowed_effects inclui 03-RESOURCES/ alem do que o corpo escreve (so lessons.md); estreitar quando houver evidencia de uso."
---

# content-analysis — leitura de sinal

> **Proveniência:** a skill nasceu como transplante de
> `04-SYSTEM/agents/marketing-system/signal.md` @ `9e6c4ad61` (fatia S1 do
> plano-refino-automation, 2026-08-23). Aquele corpo era o **coordenador** do
> marketing-system, não um método de análise: roteava para codenames que não
> existem mais e escrevia num `docs/progress.md` inexistente. ADR-012 já tinha
> removido marca da tabela de coordenadores — análise de conteúdo é despacho
> direto, sem camada. Em 2026-09-02 o corpo do roteador foi removido e o
> procedimento de análise foi trazido de `content-creation` MODO 9, onde estava
> arquivado no lugar errado. Histórico do transplante: `git log -- <este arquivo>`.

## O que esta skill faz

Recebe conteúdo **já publicado** com métricas e devolve diagnóstico com causa
atribuída e mudanças testáveis. Lê sinal; não produz peça nem opina sobre gosto.

## Contexto do criador

Michel Csasznik — tech/AI, ADS/FIAP, concurso público, criador solo. Nicho
paralelo: fotografia e vídeo de viagem. Plataformas: X, Instagram (Reels,
carrossel, Stories), YouTube (Shorts + long-form). Sem equipe, sem budget de ads
— logo, toda recomendação tem que caber em execução solo.

## Ao ser invocado

1. **Exigir os dados.** Sem métricas coladas não há análise: pare e peça. Mínimo
   por post: tipo/formato, plataforma, data, alcance, curtidas, comentários,
   salvamentos/compartilhamentos. Sem isso o output vira opinião — recuse.
2. **Estabelecer a linha de base.** Mediana do conjunto por métrica, não média
   (um viral distorce a média e some com o padrão). Declare o n.
3. **Classificar cada post** contra a base: acima, dentro, abaixo.
4. **Atribuir causa** aos outliers dos dois lados — ver Diagnóstico.
5. **Entregar mudanças testáveis** — ver Output.

## Diagnóstico

Para cada post fora da base, atribua causa a **um** eixo, não a vários:

| Eixo | Sintoma no dado |
|---|---|
| Hook | Alcance alto, engajamento baixo — entrou no feed, não segurou |
| Formato | Um formato concentra os outliers positivos ou negativos |
| Tema/pilar | Mesmo tema repete abaixo da base em formatos diferentes |
| Frequência/horário | Queda geral no período, sem correlação de tema ou formato |
| Profundidade | Salvamentos altos, curtidas baixas — vale referência, não reação |

Regra: alcance é distribuição, engajamento é reação, salvamento é valor
percebido. Não trate os três como a mesma coisa — cada um falha por motivo
diferente.

## Armadilhas de leitura

- **n pequeno.** Abaixo de ~10 posts, chame de hipótese (`[hyp]`), não de padrão.
- **Métrica de vaidade.** Seguidores e impressões sem ação não são resultado.
- **Confundir correlação com causa.** Dois posts de viagem foram bem — pode ser
  o tema, o formato, ou o dia. Nomeie a alternativa que você não pode descartar.
- **Sobreajuste ao viral.** Um outlier extremo não define fórmula; separe-o e
  releia o resto sem ele.

## Output padrão

```
=== CONTENT-ANALYSIS | n=<posts> | período <data>–<data> ===
Base (mediana):  alcance <x> · engajamento <y> · salvamentos <z>
Acima da base:   [post + eixo de causa]
Abaixo da base:  [post + eixo de causa]
Freio principal: [1 eixo, com o dado que sustenta]

3 mudanças testáveis:
  1. [mudança] → métrica que deve mover
  2. ...
Teste A/B: [1 variável só, próximos N posts]
Fórmula dos hooks acima da base: [padrão extraído, ou "n insuficiente"]
```

Toda afirmação carrega o dado que a sustenta. Sem dado → `[hyp]`.

## Quando NÃO usar

- **Criar ou reescrever o conteúdo analisado** → `content-creation`.
- **Consolidar fontes em resumo/briefing** → `content-synthesis`.
- **Julgar voz/tom/AI-slop** de um texto → `voice-registers`.
- **Julgar estrutura de leitura** (front-load, 1 ideia/frase) → `content-design-review`.
- **Sem métricas** — não estime desempenho por leitura do texto. Recuse e peça o dado.

## Failure modes

- Métricas ausentes ou parciais → pare, peça o que falta, não estime.
- n < 10 → entregue, mas marque todo padrão como `[hyp]`.
- Média no lugar de mediana → um viral move a base; refaça com mediana.
- Outlier com causa atribuída a dois eixos → escolha um e nomeie a alternativa que não pode descartar.
- Mudança sugerida sem métrica que deve mover → não é testável; reescreva ou corte.

## Completion

Critério de aceite:

- [ ] Bloco `CONTENT-ANALYSIS` preenchido com `n` e período declarados.
- [ ] Base calculada por mediana, com o valor de cada métrica.
- [ ] Cada post fora da base tem exatamente um eixo de causa.
- [ ] 3 mudanças, cada uma com a métrica que deve mover; teste A/B com 1 variável.
- [ ] Afirmação sem dado marcada `[hyp]`; com n < 10, todo padrão marcado.

## Self-Improvement

Após cada execução com output significativo:
1. Se usuário corrigir output → a skill `evolve` em MODO META-LEARN extrai o princípio (não regra)
2. Se padrão recorrente de erro (≥2×) → flag para `@harden <slug>` com contexto
3. Lições append em `06-GENERATED/tasks/lessons.md` (formato: `- YYYY-MM-DD: [<slug>] <observação>`)

> Ver: [meta-learn](../evolve/meta-learn.md) · [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop
