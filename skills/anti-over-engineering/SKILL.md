---
origin: native
kind: skill-proc
resolver-status: exposed
name: anti-over-engineering
type: skill
reviewed-scope: "2026-10-25: conferido contra disco com revisao shield (opus, somente leitura). Corrigidos: Hermes citado como runtime (aposentado 2026-10-11, model-routing.json:75); simplify-code dado como so arquivada (existe versao viva no plugin michel); complexity-ratchet chamado de skill (e modo de codebase-design, nao invocavel); pipeline-drain apontado como skill (e workflow); data fixa no formato do ledger; reads do frontmatter sem scripts/ e workflows/. Conferido ok: analysis_digest sha256, existencia de diagnose, prototype, spec-lifecycle, code-review, code-optimize, numeros do ponytail contra a pagina-fonte do vault. NAO conferido: numeros contra o README upstream do ponytail; evals/; o ledger lessons.md nunca recebeu linha `debt:` (informativo)."
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed_by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
review-scope-security: "saida-de-quarentena 2026-09-05: scan-external-skill.py ok (0 findings); leitura de intencao: texto de procedimento puro, sem exec/rede/credencial; reads/writes do frontmatter batem com o corpo (le 04-SYSTEM/automation/skills/, escreve 06-GENERATED/tasks/lessons.md); irmas citadas resolvem (core/complexity-ratchet, reasoning/diagnose); analysis_digest rebaselinado para a nota atual"
reviewed: 2026-10-25
description: "Use when: feature nova no vault (script, skill, agente) pede implementação; decidir ANTES de escrever se merece código ou 1-liner. Escada YAGNI→codebase→stdlib→nativo→uma-linha; níveis lite/full/ultra; debt ledger. Também antes de REESCREVER código que já existe (portar para outra linguagem, cachear, consolidar). NÃO usar para ajuste local em código já escrito (code-optimize), revisão de PR (code-review) ou debug em andamento. implement só serve com PRD/issue já decidindo o quê construir, e office-hours avalia ideia de produto: decidir se código novo no vault vale a pena ou dá para simplificar antes de escrever é aqui."
version: 1.0.0
status: active
updated: 2026-10-25
triggers:
  positive:
    - "over-engineering"
    - "yagni"
    - "adicionar feature sem pedido claro"
    - "implementar script"
    - "preciso escrever código novo para isso, vale a pena?"
    - "cabe em uma linha de código"
    - "existe versão em uma linha"
    - "dá pra simplificar isso antes de implementar?"
    - "vale a pena implementar"
    - "pedir feature sem caso de uso"
  negative:
    - "ajuste local em código já escrito (code-optimize)"
    - "revisão de PR (code-review)"
    - "debug em andamento"
reads:
  - 04-SYSTEM/automation/skills/
  - 04-SYSTEM/automation/workflows/
  - 04-SYSTEM/scripts/
writes:
  - 06-GENERATED/tasks/lessons.md
source_repo: dietrichgebert/ponytail
analysis_digest: sha256:75cdc06919b30cd6b8e2b294f5e2720ff72c04838a42d4b096be889499996b79
source_analysis: 03-RESOURCES/sources/github/p0/dietrichgebert-ponytail.md
---

## Objetivo

Gate de decisão ANTES de escrever: toda feature nova do vault (script, skill, agente, automação) passa pela escada YAGNI→já-existe→stdlib→nativo→uma-linha antes de virar implementação. O melhor código é o que nunca foi escrito [obs]. Atua no degrau que as irmãs não cobrem: a decisão de NÃO escrever. Vizinhos que atuam DEPOIS: a skill code-optimize (otimiza código existente) e o modo ratchet de codebase-design (`complexity-ratchet.md`, mede complexidade). Esta skill decide antes — se alguma irmã for invocada sem o gate, rode o gate (full) primeiro.

## A escada (heurística ANTES de escrever)

Sete degraus, do mais barato ao mais caro. Suba um degrau SÓ quando o atual falhou com evidência (teste real, não suposição):

1. **YAGNI** — o pedido resolve problema que existe AGORA? Sem usuário, sem dor, sem dado → resposta é "não implementar". Evidência: nomear o caso de uso concreto que falha sem a feature.
2. **Já existe no codebase** — busque no vault (busca por conteúdo em 04-SYSTEM/automation/skills/ e 04-SYSTEM/scripts/: Grep ou `rg` no Claude Code) por função/skill com a mesma intenção. Achou → reusar, nunca duplicar (regra dedupe do vault).
3. **stdlib** — a ferramenta padrão entrega? Ex: find, grep, rg, jq, python3 + pathlib, shell nativo.
4. **Feature nativa** — o runtime/plataforma (Obsidian, macOS, Claude Code) já tem? Ex: busca nativa, template, comando built-in.
5. **Dependência já instalada** — pacote/CLI presente no ambiente. Instalar dependência nova só se 1–4 falharam com evidência.
6. **Uma linha** — 1 comando/1-liner resolve? Prefira `find … | xargs …` a script de 40 linhas.
7. **Mínimo que funciona** — implementação mínima: sem abstração antecipada, sem configuração especulativa.

Critério mecânico: para cada degrau, 1 linha registrando por que falhou (ou passou). Degrau pulado sem registro = over-engineering.

## Intensidade: lite / full / ultra

A escada é a mesma; o que muda é a intrusividade:

- **lite** — pergunta pontual de viabilidade ("dá pra fazer em 1-liner?"): aplicar só os degraus 6–7; não tocar em código existente.
- **full** (default para feature nova) — escada completa + regras anti-abstração + marcador `debt:` em toda simplificação deliberada.
- **ultra** — pedido explícito, revisão de features existentes, ou proposta de reescrever/substituir código existente (outra linguagem, cache, consolidação): escada + varredura ranqueando "maior corte primeiro" (net: -N linhas) + benchmark com baseline.

Seleção mecânica: pedido de implementação nova → full; dúvida de viabilidade → lite; "auditar/revisar simplificação" → ultra. Dúvida → full.

## Quando NÃO usar

- Ajuste local em código já escrito e funcionando sem queixa: use code-optimize (otimiza) ou o modo ratchet de codebase-design (`complexity-ratchet.md`, mede) — esta skill é o gate ANTES, não o martelo DEPOIS. Exceção: proposta de reescrever ou substituir esse código (portar para outra linguagem, adicionar cache, consolidar processos) é implementação nova e passa por esta skill em modo ultra, com "não fazer nada" como baseline honesto.
- Requisito regulatório/contratual explícito (TJAM, financeiro, compliance): a escada não sobrepõe norma; mínimo exigido por regra não é over-engineering.
- Usuário pediu explicitamente arquitetura ou prova de conceito: respeitar (ver prototype, spec-lifecycle).
- Bug em andamento: debugar primeiro (`reasoning/diagnose` — systematic-debugging não existe); não interromper com escada.
- Revisão de PR/diff alheio: code-review, não esta skill.

## Procedimento

Entrada: pedido de feature nova (script/skill/agente) ou dúvida de implementação.

1. **Escreva o caso de uso em 1 frase** (sujeito + verbo + resultado). Se não der, o pedido está vago: devolva pergunta antes de qualquer código. Done: frase de 1 linha existe.
2. **Suba a escada do degrau 1 ao 7** (seção acima), anotando 1 linha de evidência por degrau (comando/arquivo testado + resultado). Pare no primeiro degrau que passa.
3. **Se passou no degrau 2–6:** entregue o reuso ou o 1-liner — mostre o comando ou o ponteiro para o artefato existente; NÃO crie arquivo novo. Done: resposta ≤5 linhas.
4. **Se chegou ao degrau 7:** declare o mínimo — nº de arquivos, funções, linhas estimadas, e o que fica FORA (config, abstração, edge cases sem usuário). Done: lista "fora de escopo" com ≥1 item.
5. **Aplique o nível de intensidade** (default full): regras anti-abstração — (a) nenhum parâmetro sem usuário real; (b) nenhuma interface com 1 única implementação; (c) nenhum handler/evento para 1 chamada; (d) nomes por intenção, não mecanismo. Done: (a)–(d) verificadas uma a uma.
6. **Toda simplificação deliberada vira contrato:** marcador `debt: <teto>, <upgrade path>` na linha do código simplificado + 1 linha no ledger `06-GENERATED/tasks/lessons.md` no formato `YYYY-MM-DD | <caminho> | <teto> | <gatilho>`. Done: todo `debt:` tem par no ledger e vice-versa (sem órfãs).
7. **Feche com custo total:** LOC finais + delta vs baseline yagni-oneliner (seção Benchmark). Done: 2 números, sem narrativa.

Stop condition: degrau que passa OU usuário insistindo em implementar com degrau anterior válido — nesse caso registrar a insistência como dívida no passo 6.

Failure modes: pular degrau sem evidência; aceitar "pode ser que precise" como evidência; criar arquivo novo com degrau 2 válido.

## Dívida deliberada — 'later means never'

Simplificação deliberada não é dívida oculta: é contrato. Três regras:

1. **Toda simplificação tem marcador no local:** `debt: <teto>, <upgrade path>` — teto = quando reavaliar (data ou evento); upgrade path = o que fazer se falhar.
2. **Toda dívida tem linha no ledger** (06-GENERATED/tasks/lessons.md). 'Later means never': sem teto e sem gatilho, "depois" vira "nunca" — a dívida apodrece silenciosa.
3. **Gatilho estourado = upgrade obrigatório no próximo ciclo:** teto passou OU sintoma real (pedido de feature duplicado, erro, lentidão). Dívida com teto vencido e sem ação → marcar `[vencida]` no ledger.

Critério mecânico: 1 `debt:` no código ↔ 1 linha no ledger; ledger sem marcador correspondente = órfã (corrigir ou apagar).

## Benchmark com baseline honesto

Nenhuma proposta de implementação se justifica sem medir contra o baseline preguiçoso:

- **caveman** — solução ingênua mínima (loop com if, copiar-pastar).
- **yagni-oneliner** — o 1-liner que resolve 80% do caso (ex: `find … | wc -l` em vez de script de contagem).

Regra: a proposta vence SÓ se for melhor que os dois baselines em ≥1 métrica (LOC, tokens, custo, tempo) com número anotado. Baseline honesto é o yagni-oneliner, não "nada". Empate ou derrota → entregue o baseline. Nota: o plugin-fonte reporta -54% LOC, -22% tokens, -20% custo, -27% tempo vs sem-skill (n=4, Haiku 4.5) [obs — autoclavado pelo autor; tratar como indicativo, não promessa].

## Verificação

Done mecânico — todos os itens:

- [ ] Caso de uso em 1 frase existe (passo 1).
- [ ] Degraus percorridos com ≥1 linha de evidência cada; nenhum pulado sem registro.
- [ ] Degrau vencedor declarado (1–7); se 2–6, nenhum arquivo novo foi criado.
- [ ] Se degrau 7: "fora de escopo" com ≥1 item + anti-abstração (a)–(d) verificadas.
- [ ] Todo `debt:` no artefato tem linha no ledger com teto+gatilho; nenhuma órfã.
- [ ] Custo fechado: LOC finais vs baseline yagni-oneliner (2 números).

Qualquer item falhou → declarar falha e reabrir o passo correspondente.

## Exemplo de uso real

Pedido: "quero um script de ingest novo para processar os clippings desta semana".

1. Caso de uso: "mover clippings da 00-INBOX para 03-RESOURCES com frontmatter validado" — 1 frase ok.
2. Escada: (1) YAGNI: sim, há clippings acumulados [evidência: contagem na inbox]. (2) Já existe: busca por conteúdo (Grep/`rg`) em 04-SYSTEM/automation/skills/ → o workflow `pipeline-drain` (F0–F3, em `04-SYSTEM/automation/workflows/vault-maintenance/`) e a skill ingest-verify já cobrem ingest e validação. → Degrau 2 passou; pare.
3. Entrega: apontar pipeline-drain existente + comando de invocação; NÃO criar script novo. Resposta ≤5 linhas.
4. Se o usuário insistir em script próprio: implementar no degrau 7 com mínimo declarado e registrar a insistência como dívida: `debt: 2026-09-01 (teto), migrar para pipeline-drain se F3 atrasar (upgrade path)` + 1 linha no ledger.

## Calls (skills e modos vizinhos)

- **code-optimize** — otimiza código que JÁ existe (pós-escrita).
- **codebase-design, modo ratchet** (`dev/codebase-design/complexity-ratchet.md`; não é skill invocável) — mede complexidade DEPOIS de implementar.
- **code-review / simplify-code** — revisão de diff/PR existente; não duplicar varredura aqui. (`simplify-code` tem versão viva em `04-SYSTEM/automation/skills/dev/simplify-code/SKILL.md`, com `disable-model-invocation: true`: só o usuário a invoca. A cópia antiga está em `08-ARCHIVE/system/agents/skills-dup-2026-07/simplify-code/SKILL.md`.)
- **prototype / spec-lifecycle** — quando o usuário pede explicitamente arquitetura ou prova de conceito.

## Completion

- [ ] Todos os itens de `## Verificação` marcados.
- [ ] Degrau vencedor (1–7) declarado com 1 linha de evidência por degrau percorrido.
- [ ] Custo fechado: LOC finais vs baseline yagni-oneliner.

## Failure modes

- **Degrau pulado sem evidência**: subir na escada por suposição → registre 1 linha de teste real por degrau.
- **"Pode ser que precise" como evidência**: aceitar necessidade hipotética → YAGNI reprova; nomeie o caso concreto que falha.
- **Arquivo novo com degrau 2 válido**: duplicar o que já existe → reuse o artefato existente.
- **Dívida órfã**: `debt:` no código sem linha no ledger, ou o inverso → cada marcador tem par.
