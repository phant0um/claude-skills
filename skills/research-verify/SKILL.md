---
origin: native
kind: skill-proc
resolver-status: exposed
name: research-verify
type: skill
reviewed-scope: "checagem mecanica: 0/0 wikilinks resolvem; 1/1 paths citados existem; 0/0 scripts citados resolvem; 0 par modelo-effort invalido; kind=skill-proc, 6 secoes, 45 linhas"
reviewed-by: claude-opus-5
reviewed_by: claude-opus-5-5
review-scope-security: "saida-de-quarentena 2026-09-25 (padrao de 7c024143c anti-over-engineering e 0afe7a456 agent-fault-debug): skill em uso ativo — scout.md calls: research-verify, agent-contracts.json lista a dependencia; scan-external-skill.py ok (0 findings); R8 reativado: a analise que o comentario de quarentena dava por inexistente existe (firecrawl-fire-enrich.md, commit 0ea30a006) e descreve o padrao primario citado no corpo (fases sequenciais, contexto acumulado, source URL por dado); source_repo na allowlist; analysis_digest = sha256 atual da nota"
reviewed: 2026-09-25
description: "Use when: pesquisa multi-round precisa validar se as fontes respondem à pergunta (threshold de confiança) e fazer retry com reformulação dirigida antes de sintetizar com citações."
version: 1.0.0
status: active
updated: 2026-09-25
triggers:
  positive:
    - "pesquisa multi-round"
    - "validação de confiança"
    - "retry dirigido"
    - "deep research"
    - "síntese com citações"
  negative:
    - "fonte única confiável"
    - "síntese sem citações exigidas"
reads: []
writes: []
calls: []
source_repo: firecrawl/fire-enrich
source_analysis: 03-RESOURCES/sources/github/p0/firecrawl-fire-enrich.md
analysis_digest: sha256:bd75f7c11b7b000726d896369d8715b6ec24a1957e5a74970cd86a3f140f0f46
---

## Objetivo

Pesquisa profunda em rounds: decompor pergunta complexa em sub-perguntas → buscar em paralelo → validar se cada fonte responde à pergunta (threshold MIN_ANSWER_CONFIDENCE) → retry com reformulação dirigida (máx MAX_RETRIES) → sintetizar com citações numeradas. Nenhum claim sai sem fonte validada; fonte não validada = [não-verificado], nunca inventada. Padrão primário importado de firecrawl/fire-enrich (MIT): pipeline por fases sequenciais com contexto acumulado, validação progressiva por fase e source URL em cada dado retido; reforçado por firecrawl/firesearch (grafo breakdown→search→validate→retry→synthesize + taxonomia de reformulação), firecrawl/last30flames (recência, fontes públicas, contexto salvo com stale warning) e bytedance/deer-flow (deep-research: "uma busca nunca basta" — carregar evidência antes de gerar conteúdo).

## Configuração

Constantes vivem AQUI — esta seção é a fonte única. A versão importada apontava para um constants file separado que nunca foi criado; para 6 valores, arquivo próprio é overhead (ver `anti-over-engineering`). MAX_SEARCH_QUERIES=12, MAX_SOURCES_PER_SEARCH=4, MIN_ANSWER_CONFIDENCE=0.7, MAX_RETRIES=2, STALE_DAYS=7, FONTES_BLOQUEADAS=[Reddit, X/Twitter, TikTok, Instagram]. Mudar comportamento = editar esta seção; nunca valores soltos no procedimento.

## Quando NÃO usar

- Pergunta simples que 1 busca resolve — use `scout` ou web_search direto.
- Sem ferramenta de busca disponível (sem web access): o loop depende de busca real; aborte e declare falha.
- Pergunta opinativa/subjetiva sem fonte objetiva para pontuar confiança.
- Curadoria/escrita sem verificação factual — herald/content-design.
- Fonte primária inacessível (paywall/login): não substitua por fonte paralela sem marcar; prevalece "não inventar fonte".

## Procedimento

1. **Decompor** — Quebre a pergunta original em sub-perguntas disjuntas (≤ MAX_SEARCH_QUERIES; cada uma respondível por fonte independente). Registre pergunta original + sub-perguntas no contexto de pesquisa. *Done:* a união das sub-perguntas cobre a pergunta inteira, sem sobreposição.
2. **Resolver ambiguidade** — Tópico com múltiplas interpretações: rode passada barata de candidatos (1 busca por interpretação), fixe a entidade/escopo vencedor e reescreva as sub-perguntas com ele. *Done:* toda sub-pergunta referencia a mesma entidade.
3. **Buscar** — Para cada sub-pergunta: busca + extração em markdown full-page. Guarde por fonte: URL, título, trecho, data de acesso. Só fontes públicas; nunca FONTES_BLOQUEADAS. *Done:* todo resultado registrado com URL e data.
4. **Validar confiança (threshold)** — Para cada fonte, responda mecanicamente: "esta fonte responde à sub-pergunta?" Score 0–1. Aprova se score ≥ MIN_ANSWER_CONFIDENCE (0.7). Reprovada = fora da síntese, mas retida no log com score e motivo. *Done:* score registrado para toda fonte.
5. **Retry com reformulação dirigida** — Sub-pergunta sem fonte aprovada: reformule a query com 1 estratégia da taxonomia por tentativa, na ordem: 1) decompose (quebrar em partes menores) 2) rephrase (mesma intenção, outras palavras) 3) synonyms (trocar termos-chave) 4) narrow (restringir escopo/janela) 5) broaden (ampliar escopo) 6) academic (termos formais/literatura) 7) practical (aplicação/prática). Registre a estratégia de cada retry. Máx MAX_RETRIES (2). Esgotou → sub-pergunta marcada [não-verificado]. *Done:* toda sub-pergunta tem ≥1 fonte aprovada OU flag [não-verificado] explícita.
6. **Sintetizar com citações** — Cada claim termina em [N] apontando para a lista de fontes (URL completa). Só fontes aprovadas na fase 4 são citáveis. Conflito entre fontes: apresente ambos os lados com suas citações; não resolva por voto. *Done:* toda claim citada; toda citação resolvível para URL real.
7. **Salvar contexto (opcional)** — Com follow-up previsto ou pedido do usuário, salve contexto (pergunta, sub-perguntas, fontes aprovadas com URL, decisões de retry) com data no header. Reuso de contexto com idade > STALE_DAYS (7): anexe stale warning no topo e revalide as fontes antes de citar. *Done:* contexto salvo tem data; reuso antigo exibe stale warning.

**Validação progressiva por fase (fire-enrich):** o pipeline roda em fases sequenciais — cada fase tem contrato de saída (schema/checklist), alimenta a próxima com contexto acumulado e só avança com o output da fase anterior validado (gate por fase: fase N+1 não inicia sem fase N validada). Dentro de cada fase, buscas em paralelo (≤ MAX_SOURCES_PER_SEARCH). Todo dado retido carrega source URL (cadeia de evidência). A síntese final valida cada dado contra sua fonte e resolve conflitos apresentando os dois lados — nunca por voto.

## Extração por documento antes de sintetizar

Ao combinar N fontes, extraia primeiro os fatos relevantes de cada documento em
nota curta com citação (URL e trecho), e sintetize só a partir das notas. Nunca
despeje N documentos inteiros num único contexto: mais documentos só elevam a
precisão quando cada um é extraído antes; o despejo bruto degrada. Fonte:
Stanford CS329A Parte 7 (Search-o1, reason-in-documents).

Falha típica de agente de pesquisa: perder a fonte fundacional e não julgar
importância além de relevância. Antes de sintetizar, cheque explicitamente se a
fonte fundacional ou mais citada do tema está entre as aprovadas; se não, busque-a.
Fonte: CS329A Partes 8 e 9 (falhas medidas no DeepScholar-bench).

## Verificação

Done mecânico — só declare done com todos os checks verdadeiros:
- [ ] A união das sub-perguntas cobre a pergunta original (sem buraco).
- [ ] Toda claim da síntese tem [N] resolvível para URL da lista de fontes.
- [ ] Toda fonte citada tem score ≥ MIN_ANSWER_CONFIDENCE registrado.
- [ ] Nenhuma URL inventada: toda fonte foi realmente buscada/extraída nesta run, ou revalidada de contexto salvo (com stale warning se > STALE_DAYS).
- [ ] Sub-perguntas sem fonte aprovada estão marcadas [não-verificado], não preenchidas.
- [ ] Limites da seção Configuração respeitados (MAX_SEARCH_QUERIES, MAX_SOURCES_PER_SEARCH, MAX_RETRIES).
- [ ] Cada retry registrado com estratégia da taxonomia (broaden/narrow/synonyms/rephrase/decompose/academic/practical).
- [ ] Gate por fase respeitado: fase N+1 só iniciou com output da fase N validado e todo dado retido tem source URL.

## Exemplo de uso real

Pesquisa multi-round para o `scout` com validação de confiança e retry. Pergunta: "o que a Anthropic lançou de relevante para concorrentes nos últimos 30 dias?" → decompor em [lançamentos de produto, mudanças de preço/API, cobertura de imprensa, posição vs OpenAI/Google]. Busca paralela por sub-pergunta. Validação: blog oficial da Anthropic responde lançamentos (score 0.9, passa); post de X citado cai em FONTES_BLOQUEADAS; matéria de 2025 não responde à janela de 30 dias (score 0.4, reprova). Preço ficou sem fonte aprovada → retry narrow "Anthropic API pricing changes julho 2026" (estratégia registrada). Gate por fase: bloco de produto só avança após cada dado ter URL de fonte validada; conflito de datas reportado com ambas as fontes. Síntese do briefing com citações [1..n] e URLs. Contexto salvo para o próximo briefing do `scout`; reuso > 7 dias → stale warning + revalidação antes de citar.

## Completion

- [ ] Todos os checks da seção Verificação verdadeiros.
- [ ] Síntese entregue com citações [N] resolvíveis para URL real.
- [ ] Sub-perguntas sem fonte aprovada marcadas `[não-verificado]`.

## Failure modes

- **URL inventada**: citar fonte que não foi buscada nesta run → toda fonte vem de busca real ou de contexto revalidado.
- **Conflito resolvido por voto**: escolher o lado com mais fontes → apresente os dois lados com citações.
- **Fonte bloqueada**: usar Reddit, X, TikTok ou Instagram → nunca use FONTES_BLOQUEADAS.
- **Retry sem estratégia**: reformular a query sem registrar a estratégia → registre uma estratégia da taxonomia por tentativa.
- **Contexto velho sem aviso**: reusar contexto com mais de STALE_DAYS → anexe stale warning e revalide.
