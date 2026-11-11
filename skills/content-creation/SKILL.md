---
kind: skill-proc
resolver-status: exposed
type: skill
name: content-creation
input:
  required_fields: [task]
output:
  format: json|md
triggers:
  positive:
    - "escrever post de rede social"
    - "criar conteúdo"
    - "escrever thread de rede social"
    - "escrever copy publicitário"
    - "posicionamento de marca"
    - "calendário de conteúdo"
  negative:
    - "analisar métricas de conteúdo"
    - "layout/design"
    - "revisar voz/tom de texto já escrito (use voice-registers)"
    - "artigo longo de blog com destino definido (use article-draft)"
    - "artigo longo a partir de material bruto (use writing-shape)"
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
source_agent: anchor
status: active
created: 2026-08-20
description: "Use when: estratégia de marca e produção de peça curta de plataforma (post, thread avulsa, copy, calendário, pilares). Métricas de conteúdo publicado vão para content-analysis; voz de texto pronto para voice-registers; artigo longo para writing-shape (sem destino) ou article-draft (blog); thread semanal de AI para x-thread-weekly; foto, vídeo e visual da peça para marketing-content-design."
updated: 2026-10-25
reviewed: 2026-10-25
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-10-25: conferido contra disco com revisao shield (opus, somente leitura). Corrigidos: /meta-learn e modo de evolve; x-thread-weekly esta paused; fonte Guillermo Rauch sem fonte no vault, marcada [nao-verificado]. Conferido ok: type x-thread liga registro B no voice-lint, frame/vox deletados em defac13fc, rotas para writing-shape/writing-fragments/article-draft/marketing-content-design/visual-design, external-publish proibido. NAO alterado: ordem MODO 9 vs content-design-review diverge de escrita.md, projeto-novo.md:153 e upstream-pr.md §Escrita (U8) (corpo: produz a peca e voice-registers audita depois; chamadores: depois de review); a ordem a decidir esta nos chamadores. allowed_effects com 03-RESOURCES/ largo (menor)."
---

# content-creation — estratégia e produção de marca

> **Proveniência:** procedimento transplantado de
> `04-SYSTEM/agents/marketing-system/anchor.md` @ `9e6c4ad61` (fatia S1 do
> plano-refino-automation, 2026-08-23). Os modos **frame** (enquadramento) e
> **vox** (voz e registro na copy) foram absorvidos aqui na Fase 3 e seus
> arquivos deletados em `defac13fc` — mas a absorção deixou para trás a regra que
> proibia produzir peça final, herdada de quando Vox existia. Corrigido em
> 2026-09-02. Histórico: `git log -- <este arquivo>`.

## O que esta skill faz

Duas coisas, na ordem: define **estratégia** de marca/conteúdo (MODOS 1–8) e
**produz a peça curta** de plataforma (MODO 9). Estratégia sem peça vira
planejamento morto; peça sem estratégia vira post avulso.

## Contexto do criador

Michel Csasznik — tech/AI, ADS/FIAP, concurso público, criador solo.
Nicho paralelo: fotografia e vídeo de viagens internacionais (iPhone 17 Pro Max,
DJI Osmo Pocket 3). Plataformas: X, Instagram (Reels, carrossel, Stories),
YouTube (Shorts + long-form). Público: viajantes independentes, entusiastas de
fotografia mobile, tech/AI learners. Tom: direto, profundidade real, zero guru
motivacional. Sem equipe, sem budget de ads.

## Ao ser invocado

1. Identificar o modo solicitado
2. Se objetivo, fase ou nicho forem ambíguos, listar premissas e pedir confirmação
3. Executar com especificidade — zero ideias genéricas
4. Se o modo for estratégico e o usuário quiser a peça, encadear no MODO 9

## Modos

### MODO 1 — AUDITORIA DE MARCA
Ative: `"auditar marca:" + cole perfil atual (bio, links, conteúdo recente)`

CRITÉRIO: ≥3 fraquezas específicas, ≥3 oportunidades perdidas, ações priorizadas por impacto.

→ Diagnóstico: lacunas, fraquezas, oportunidades perdidas
→ Posicionamento ideal para a combinação tech/AI + viagem/fotografia
→ 3 ações prioritárias para os próximos 30 dias
Seja crítico — zero elogios genéricos.

**Exemplo (MODO 1):**
Input: `"auditar marca: X @michel_cs — bio 'ADS/FIAP | IA | Concurso' — últimos posts: 3 sobre Claude, 2 sobre rotina, 1 foto viagem — 340 seguidores"`
Output (trecho): Fraquezas — bio não diz o que o leitor recebe; posts sem pilares fragmentam a identidade; foto de viagem sem gancho tech desperdiça o nicho paralelo. Oportunidade perdida — "tech + viagem" tem densidade baixa no X BR e não aparece em nenhum post. 30 dias: (1) bio com ângulo tech/viagem; (2) thread "como IA mudou meu estudo para concurso"; (3) definir 1 série recorrente.

### MODO 2 — POSICIONAMENTO
Ative: `"posicionamento:" + nicho + objetivos`

CRITÉRIO: Responde quem serve + que problema resolve + por que diferente. Linguagem psicográfica, não demográfica.

→ Quem serve (psicográfico) | problema profundo | diferencial vs. outros criadores
→ 3 versões: LinkedIn | X | Newsletter/Bio Instagram

### MODO 3 — OTIMIZADOR DE PERFIS
Ative: `"otimizar perfis:" + cole perfis atuais`

CRITÉRIO: Cada perfil otimizado para algoritmo + credibilidade imediata em <5 segundos.

→ Por plataforma: headline + bio + seção em destaque + tom recomendado
→ Plataformas: X | Instagram | LinkedIn | Newsletter (Beehiiv)

### MODO 4 — PILARES DE CONTEÚDO
Ative: `"pilares de conteúdo"`

CRITÉRIO: 5 pilares, cada um ataca métrica diferente (alcance / engajamento / conversão / autoridade / retenção).

→ Por pilar: nome + lógica estratégica + 5 ideias específicas com ângulo + formato ideal por plataforma + métrica principal

### MODO 5 — CALENDÁRIO 30 DIAS
Ative: `"calendário 30 dias:" + mês ou tema atual`

CRITÉRIO: Distribuição equilibrada dos pilares. Mínimo: 4 Reels + 4 carrosséis + 2 bastidores/semana no Instagram; 1-2 posts/dia no X.

→ Por post: dia | plataforma | tema + ângulo específico | formato | objetivo | hook sugerido
→ Entrega em tabela por semana

### MODO 6 — TEMPLATES DE POSTS VIRAIS
Ative: `"templates virais:" + quantidade ou tipo`

CRITÉRIO: Cada post tem hook que para scroll + tensão narrativa + linha final compartilhável/salvável.

→ Distribuição: 5 narrativas pessoais com virada | 5 insights contrários (tech/viagem/produtividade) | 5 tutoriais táticos | 5 reframes de perspectiva
→ Por post: hook + lógica ou tensão + linha final

### MODO 7 — ROTINA DE CRESCIMENTO
Ative: `"rotina de crescimento"`

CRITÉRIO: Cronograma minuto a minuto com métricas semanais mensuráveis.

→ Rotina de 20 min/dia: engajamento ativo, quais contas priorizar, scripts de comentário/DM
→ Métricas semanais simples (sem ferramentas complexas)

### MODO 8 — SISTEMA DE MONETIZAÇÃO
Ative: `"monetização:" + produtos ou serviços planejados`

CRITÉRIO: Funil completo (conteúdo → lead → conversão) com rastreamento simples.

→ Funil: conteúdo gratuito → leads qualificados → conversão
→ Scripts de outreach humanos (não automação fria)
→ Follow-up 3 etapas: valor → confiança → oferta

### MODO 9 — PRODUÇÃO DA PEÇA
Ative: `"escrever post/thread/copy:" + tema + plataforma`

CRITÉRIO: Peça pronta para publicar, no formato nativo da plataforma. Hook que
para scroll na primeira linha, uma ideia por post, fecho que dá o que salvar.

→ **X/thread:** 6-8 tweets. Regras de tweet (hook, 1 ideia por tweet, fecho,
  proibidos) são o Registro B de `voice-registers`; não há cópia aqui. Thread
  salva leva `type: x-thread`, que liga o B no `voice-lint.py`. O digest semanal
  de AI não é daqui: é o workflow `x-thread-weekly` (hoje `status: paused`).
→ **Instagram carrossel:** slide 1 = promessa, slides 2-n = 1 ponto cada, último = ação
→ **Reels/Shorts:** roteiro com gancho nos 2 primeiros segundos + beats de fala
→ **Copy curta (bio, CTA, legenda):** 3 variantes, não uma — a escolha é do usuário

Herdado da absorção de **vox** (voz na copy) e **frame** (enquadramento da peça).
Registro de voz: direto, específico, zero guru. Se a peça precisar de auditoria
formal de voz antes de publicar, isso é `voice-registers` — não repita aqui.

## Regras

- Zero ideias genéricas sem ângulo específico
- Nunca inicie com "Claro!", "Com certeza!" ou similares
- Calendário sempre com distribuição equilibrada de pilares
- Peça produzida vem pronta para publicar — não entregue briefing quando o
  usuário pediu o texto

## Output padrão

```
Modo executado: [nome]
Premissas assumidas: [lista ou "nenhuma"]
Artefato: [peça pronta | estratégia | ambos + caminho do arquivo]
```

## Critério de Qualidade

- Estratégia com posicionamento claro e diferenciado
- Público-alvo definido com características mensuráveis
- Peça em formato nativo da plataforma, sem ajuste manual pendente
- Tom de marca consistente com o Contexto do criador

## Ship-page (Rauch)

Priorizar página própria listando o que foi shipado (com links) sobre LinkedIn. Fonte: Guillermo Rauch `[não-verificado]` (nenhuma fonte no vault).

## Quando NÃO usar

- **Analisar desempenho/audiência de conteúdo já publicado** → `content-analysis`.
- **Auditar voz/tom/AI-slop de texto já escrito** → `voice-registers`. Esta skill
  escreve com voz; aquela reprova voz. Se o texto já existe, é aquela.
- **Artigo longo a partir de material bruto** → `writing-shape` (e
  `writing-fragments` se a pile ainda não existe); com destino blog,
  `article-draft`. Esta skill é peça curta de plataforma.
- **Thread semanal de AI** → workflow `x-thread-weekly` (hoje `status: paused`).
- **Foto, vídeo, thumbnail, identidade visual da peça** → `marketing-content-design`.
  UI de produto → `visual-design`.
- **Publicar de fato** → fora de escopo: `external-publish` é `forbidden_effects`.

## Failure modes

- Modo não identificável no pedido → pergunte qual; não escolha pelo usuário.
- Pedido sem plataforma ou sem tema → liste a premissa e peça confirmação (passo 2).
- Briefing entregue quando o pedido era a peça (Regras).
- Ideia sem ângulo: trocar o tema por outro e a frase continuar valendo.
- Thread com regra de tweet local divergindo do Registro B.
- Peça publicada pela skill: `external-publish` é proibido.

## Completion

Critério de aceite:

- [ ] Output padrão preenchido: modo, premissas, artefato com path.
- [ ] Modo com `CRITÉRIO:` próprio: cada item do critério atendido e apontável no artefato.
- [ ] MODO 9: peça no formato nativo da plataforma; copy curta com 3 variantes.
- [ ] Thread salva: `type: x-thread` e `voice-lint.py --strict` sai 0.

## Self-Improvement

Após cada execução com output significativo:
1. Se usuário corrigir output → a skill `evolve` em MODO META-LEARN extrai o princípio (não regra)
2. Se padrão recorrente de erro (≥2×) → flag para `@harden <slug>` com contexto
3. Lições append em `06-GENERATED/tasks/lessons.md` (formato: `- YYYY-MM-DD: [<slug>] <observação>`)

> Ver: [meta-learn](../evolve/meta-learn.md) · [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop
