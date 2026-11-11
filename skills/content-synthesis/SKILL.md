---
kind: skill-proc
resolver-status: exposed
type: skill
name: content-synthesis
input:
  required_fields: [content_type, source_paths]
output:
  format: markdown
triggers:
  positive:
    - "sintetizar conteúdo"
    - "resumir fontes"
    - "resumo"
    - "briefing"
    - "changelog"
  negative:
    - "medir conteúdo"
    - "registrar decisão"
allowed_effects:
  - write 04-SYSTEM/
  - write 03-RESOURCES/
forbidden_effects:
  - modify agent files
  - modify manifest
  - external-publish
reads: ["**"]
writes: ["04-SYSTEM/**", "03-RESOURCES/**"]
version: 1.2.0
source_agent: herald
status: active
created: 2026-08-20
description: "Use when: comprimir fontes ou diff em status, release notes, README, changelog, briefing, corpo de PR ou docstring. Métrica de conteúdo publicado vai para content-analysis; artigo de blog para article-draft; estrutura e voz do texto pronto para content-design e voice-registers."
updated: 2026-10-25
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisao 2026-10-25: proveniencia herald corrigida (nexus-agent-system), Breaking alinhado ao exemplo. Verificado: voice-lint --strict, rotas, ADR dir, agentes vivos. NAO conferido: rubrica de PR Voss como fonte; README fora do vault (registro A vs C) e formato de PR upstream (check-pr-body) ficam para decisao nos callers."
---

# content-synthesis — output técnico em texto para humanos

> **Proveniência:** procedimento transplantado de `04-SYSTEM/automation/agents/nexus-agent-system/herald.md` @ `6304e261b` (fatia S1 do plano-refino-automation, 2026-08-23). `source_agent` do frontmatter preservado. Em 2026-09-25 saíram o nome de persona e a linha de modelo: skill não escolhe modelo.

## Propósito

Transforma output técnico (diff, log, fonte) em texto que uma pessoa lê e usa.
Comprime; não analisa nem inventa.

## Ao ser invocado

1. Identificar audiência: dev, PM, stakeholder ou público externo?
2. Extrair os pontos essenciais do input (sem inventar)
3. Estruturar no formato adequado para a audiência
4. Estrutura: [content-design](../content-design/SKILL.md). As 5
   regras e o corte moram lá, não aqui.
5. Voz: [voice-registers](../voice-registers/SKILL.md) (registro,
   catálogo de slop, não-invenção). O registro vem do destino:
   - README, changelog, docstring, doc do vault → **C** (tabela §Registros).
   - Corpo de PR, corpo de issue, resposta a revisor → **A**, pela linha
     "Texto externo curto" de escrita e
     §Texto externo curto de voice-registers. Não é C.
6. Linter antes de entregar. Arquivo do vault:
   `python3 04-SYSTEM/scripts/voice-lint.py --strict <arquivo>`. Rascunho fora do
   vault sem `type:`: acrescente `--register A` (sem registro o linter sai 2).
   `error` bloqueia a entrega; `warn` se lê e se reporta.
7. Texto que sai do vault (PR, issue, README público) só é publicado com
   aprovação humana. Esta skill entrega o rascunho e para. Na rota docs de
   escrita, este texto é produção, não entrega final:
   ainda passa por content-design-review
   e [voice-registers](../voice-registers/SKILL.md). Se a revisão alterar o texto, o parecer afetado é refeito.

## Formatos disponíveis

- **Status update**: O que foi feito, o que está pendente, bloqueios
- **Release notes**: O que mudou, impacto para o usuário, breaking changes
- **README**: Propósito, instalação, uso rápido, links
- **Briefing**: Contexto, decisão, próximos passos
- **Changelog**: Formato Keep a Changelog (Added/Changed/Fixed/Removed)
- **PR Description**: Diff → descrição estruturada para review
- **Code Docs**: Docstrings, API docs, ADRs

---

## Protocolos Estruturados

### Protocolo README

Gatilho: "content-synthesis readme" ou "gerar readme"

1. **Scan** — ler `package.json`/`pyproject.toml`/`Cargo.toml`/`go.mod`, config files, estrutura de diretórios
2. **Detectar** — linguagem, framework, runtime, dependências principais, entrypoints
3. **Estruturar** — gerar README com seções:
   - Title + 1-line description (do package.json `description` ou repo name)
   - Badges (CI, license, version — só se detectados no repo)
   - Features (extraídas do código, não inventadas)
   - Quick Start (install + run com comandos reais do package manager detectado)
   - Usage (1-2 exemplos práticos com código real do repo)
   - Tech Stack (enumerar dependências principais do manifest)
   - Configuration (env vars, config files — só se existirem)
   - Contributing (só se `CONTRIBUTING.md` existir ou repo for open source)
   - License (do `LICENSE` file ou manifest)
4. **Não inventar** — se não há CI, não colocar badge. Se não há env vars, não criar seção Configuration
5. **Linguagem** — EN para README público, PT-BR só se solicitado

### Protocolo Changelog

Gatilho: "content-synthesis changelog" ou "release notes"

1. **Coletar** — `git log --format='%h %s%n%b' <last_tag>..<SHA fixado>` (corpo inclui footer `BREAKING CHANGE:`). Fixe o SHA alvo antes de escrever prosa
2. **Classificar** — mapear cada commit para categoria Keep a Changelog:
   - `feat:` / `add:` → **Added**
   - `fix:` / `patch:` → **Fixed**
   - `refactor:` / `perf:` → **Changed**
   - `remove:` → **Removed**; breaking = `!` no tipo ou footer `BREAKING CHANGE:`
   - `revert:` anula o commit-alvo (não liste como Added); commit ambíguo → ler o diff antes de classificar
   - `docs:` → descartar (interno)
   - `chore:` / `ci:` → descartar (interno)
3. **Transformar** — commit message técnica → user-facing language (o que mudou para quem usa, não o que foi feito no código)
4. **Agrupar** — por categoria, ordem: Added → Changed → Deprecated → Removed → Fixed → Security
5. **Breaking changes** — seção `### Breaking` própria, com instrução de migração (no exemplo abaixo, no fim da versão; ordem Added → Changed → Deprecated → Removed → Fixed → Security → Breaking)
6. **Versão** — inferir semver do diff: feat → minor, fix → patch, breaking → major

### Protocolo PR Description

Gatilho: "content-synthesis pr" ou "descrição do PR"

1. **Diff** — `git diff <base_branch>...HEAD` (ou `git diff main...HEAD`)
2. **Estruturar** — gerar PR body com:
   - **Summary** — 1-2 frases: o que muda e por quê
   - **Changes** — bullet list de mudanças agrupadas por área (api, ui, tests, config)
   - **Type** — [ ] bug fix / [ ] feature / [ ] refactor / [ ] docs / [ ] breaking
   - **Testing** — 3 linhas: rodou de fato (comando + saída) / rodou contra mock ou fixture / não verificado
   - **Preservado** — contratos e comportamentos que devem continuar iguais, com a verificação que sustenta cada um
   - **Fora do escopo** — o que não foi tratado de propósito; pendências relacionadas
   - **Incidental** — mudança fora do escopo aprovado, destacada (não só justificada)
   - **Checklist** — [ ] tests added/updated, [ ] docs updated, [ ] no breaking changes (ou listar breaking)
3. **Perigo de merge** — bloco curto obrigatório no corpo, para o revisor
   calibrar a profundidade pelo perigo e não pelo tamanho do diff:
   - **Porta:** mão única ou mão dupla? Reversível com `revert` simples é mão
     dupla; migração, dado, API pública e efeito externo são mão única.
   - **Blast radius:** quem ou o quê quebra se estiver errado.
   - **Como reverter:** comando ou passos concretos; em mão única, o plano de
     mitigação. Fonte: Voss, "The Death of the Code Review".
4. **Abertura humana** — a primeira frase do PR é escrita por humano. O rascunho deixa `<!-- abertura: humano -->` no lugar da primeira frase. O corpo gerado vai dentro de `<details><summary>modelo · effort</summary>`, com linha em branco depois de `</summary>` (sem ela o GitHub não renderiza o markdown). Com template do repo alvo, o template manda (upstream-pr §Escrita (U8)).
5. **Formato** — GitHub markdown (suporta ``` code blocks, checkboxes, tables)
6. **Scope** — se diff >500 linhas, agrupar por arquivo/módulo ao invés de listar commit por commit
7. **Voz** — rascunho no scratchpad, registro A, passos 5–7 de "Ao ser invocado". Não poste o PR.

### Protocolo Code Docs

Gatilho: "content-synthesis docs" ou "documentar código"

1. **Detectar linguagem** — Python (docstrings Google/NumPy), JS/TS (JSDoc), Rust (rustdoc), Go (godoc)
2. **Scan** — identificar funções/classes/módulos públicos sem documentação
3. **Gerar** — docstrings/doc comments para cada símbolo público:
   - **Args** — nome, tipo, descrição (do código, não inventada)
   - **Returns** — tipo, descrição
   - **Raises** — exceções que podem ser lançadas (se detectáveis do código)
   - **Example** — 1 exemplo de uso prático (se não-trivial)
4. **Estilo** — seguir convenção existente no arquivo (se arquivo usa Google docstrings, usar Google)
5. **ADR** — se o código implementa decisão arquitetural não-óbvia, **proponha**
   o ADR; não escreva. `docs/decisions/` não existe e fica fora de
   `allowed_effects` (esta skill só escreve em `04-SYSTEM/` e `03-RESOURCES/`).
   ADR do vault é artefato de governança: vive em
   `04-SYSTEM/system/decisions/adr/`, numerado em sequência, e criar um é decisão
   humana — entregue o rascunho e pare. Em repo de código externo, aponte o
   caminho relativo do repo ao usuário; não escreva fora do vault.
   - Context (por que essa decisão foi necessária)
   - Decision (o que foi decidido)
   - Consequences (trade-offs, limitações)
6. **Não documentar o óbvio** — `count += 1` não precisa de docstring



## Regras

- Nada fora do input: as regras de não-invenção são as de voice-registers
  (§Regras duras de não-invenção), não uma cópia local
- Sem jargão técnico para audiência não-técnica
- Máximo 3 níveis de hierarquia em documentos
- Todo documento tem data, versão e audiência no cabeçalho
- Linguagem: PT-BR para interno, EN para código e documentação pública

## Output padrão
Formato produzido: [tipo]  
Audiência alvo: [quem vai ler]  
Localização: [onde foi salvo]  
Revisão necessária: [sim/não]

## Fora do Escopo
- Análise técnica profunda (→ Scout)
- Implementação de código (→ Forge)
- Decisões editoriais sobre produto (→ Nexus)

## Critério de Qualidade
- Audiência não-técnica entende sem perguntas de follow-up
- Zero informação inventada — tudo derivado do input
- Documento tem data, versão e audiência no cabeçalho

## Exemplos

**Input:** "content-synthesis release notes da v2.1"
**Output:** "## v2.1\n### Added\n- OAuth2 login com Google\n### Fixed\n- Timeout em uploads >10MB\n### Breaking\n- Removido /v1/legacy"

**Input:** "content-synthesis readme para o repo futmanager"
**Output:** README.md com title, description (do package.json), Quick Start (pip install + python gameapi.py), Tech Stack (Python stdlib), Usage (exemplo de init de jogo), License MIT — apenas seções com dados reais detectados no repo.

**Input:** "content-synthesis pr para branch feature/auth"
**Output:** PR body: Summary (1 frase), Changes (5 bullets agrupados: api/ui/tests/config), Type (feature), Testing (curl + pytest commands), Checklist.

## Quando NÃO usar

- Análise de métricas/desempenho → `content-analysis`.
- Registro append-only de decisão → `audit-logging`.
- Artigo de blog com tese → `article-draft`; material bruto sem destino → `writing-shape`.
- Post, thread ou copy de marca → `content-creation`.

## Failure modes

- Fonte ou `source_paths` ausente → pare e reporte qual falta; não preencha com suposição.
- Tipo de output fora de "Formatos disponíveis" → pergunte antes de escrever.
- Corpo de PR julgado no registro C → A5/C1 mal aplicados; o destino externo manda A.
- Badge, seção Configuration ou feature sem arquivo que a sustente no repo → invenção; corte.
- PR ou issue postado pela skill → efeito externo sem aprovação.

## Completion

Critério de aceite, todos checáveis:

- [ ] Cada afirmação do texto aponta para o input (arquivo, commit ou linha do diff).
- [ ] `voice-lint.py --strict` sai 0 no artefato (rascunho externo: com `--register A`).
- [ ] Cabeçalho tem data, versão e audiência (Regras).
- [ ] Output padrão preenchido, com `Localização` real no disco.
- [ ] Texto externo entregue como rascunho, com o pedido de aprovação humana explícito.
