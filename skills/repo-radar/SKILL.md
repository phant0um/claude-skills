---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: repo-radar
description: "Use when: usuário manda lista de URLs de repo GitHub para analisar/comparar — fetch metadata/README e emite tabela comparativa vs inventório do vault: Adotar/Adaptar/Investigar/Ignorar + prioridade P0–P4 + alvo. Diferente de [connection-finder](../connection-finder/SKILL.md) (conexões internas do vault); repo-radar é triagem de repo externo."
skill: repo-radar
version: 1.1
trigger: "@repo-radar [urls] · 'analise esses repos' · 'comparativo de repos'"
effort: low
tags: [discovery, scout, repos, comparativo, dedupe]
attach: scout
updated: 2026-08-11
reads:
  - 04-SYSTEM/AGENTS.md
  - 04-SYSTEM/automation/templates/repo-audit-template.md
writes:
  - 07-QUEUE/kanban/sources-pendentes.md
triggers:
  positive:
    - "lista de URLs de repo GitHub para triagem"
    - "tabela comparativa Adotar/Adaptar/Investigar/Ignorar"
    - "fetch metadata/README de repos"
  negative:
    - "repo único sem comparação"
    - "repo já adotado no vault"

reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 4/4 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 7 secoes, 92 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
 Skill: repo-radar

## Propósito
Transformar análise manual de repos em 1 passo determinístico. Separa
**observação** (fato lido, `[obs]`) de **interpretação** (`[interp]`) e
**ação** (destino + prioridade). Evita re-fazer à mão o que foi feito nos
Lotes 2-4 (50 repos).

## Quando NÃO usar

- **Lista de repos <3** — radar é comparativo; um repo vai para triagem direta.
- **Repo já avaliado e arquivado** — re-radar é duplicação; consultar a avaliação anterior.
- **Análise de código (não avaliação)** — radar avalia metadata/README; código vai para code review.

Disambiguation: `repo-radar` emite tabela comparativa Adotar/Adaptar/Ignorar; `github-repo-triage` não existe em automation — use `repo-radar` para triagem de repos; `skill-source-audit` analisa repos de skills — radar é o primeiro filtro.


## Protocolo
1. **Fetch (batch):** p/ cada URL:
   `gh api repos/<owner>/<repo> --jq '{desc,lang,stars,topics}'`
   README se preciso: `gh api repos/<owner>/<repo>/readme --jq '.content' | base64 -d`
2. **Inventário:** ler `04-SYSTEM/AGENTS.md` (agentes/skills atuais).
3. **Classificar** cada repo:
   - **Adotar** — aplicável imediatamente (citar alvo: agente/skill/rotina)
   - **Adaptar** — exige mudanças p/ se adequar ao ecossistema (citar o quê)
   - **Investigar** — interessante, sem evidência suficiente (qual evidência falta)
   - **Ignorar** — fora de escopo ou custo/risco desproporcional (citar por quê)
   Priorizar cada achado: **P0** crítico (segurança/perda de dados) · **P1**
   alto valor · **P2** experimento · **P3** referência · **P4** descartar.
4. **Emitir** tabela: Repo | Decisão | Prioridade | Alvo. + síntese acionável
   (alto valor primeiro). Para auditoria a fundo, usar o template
   `04-SYSTEM/automation/templates/repo-audit-template.md` (17 seções com
   `observação:`/`interpretação:`/`ação:` + matriz de destino).
5. **Dedupe:** marcar repos que duplicam veredito de outro (evitar bloat).

## Saída
Tabela markdown + bloco "Síntese acionável" + sugestão de tarefas (formato
FIND/REPLACE/VERIFY se for editar o vault). Refusals de ingest vão para
`07-QUEUE/kanban/sources-pendentes.md`.

## Anti-pattern
- Importar em massa. Sempre seletivo (alinha dedupe-rule do AGENTS.md).
- Classificar sem ler o inventário → falso "Adotar" do que já existe.
- Misturar observação com recomendação — fato e julgamento em campos separados.
- Reportar "nenhum problema" sem caso plantado (verifier-independence-check).

## Completion

- [ ] Lista de repositórios novos emitida com decisão (Adotar/Adaptar/Investigar/Ignorar) + prioridade P0–P4.
- [ ] Cada repo tem razão de inclusão (por que agora).
- [ ] Decisão de triagem explícita para cada entrada (aprovar/arquivar/duvidar).
- [ ] Auditoria a fundo usa o template de 17 seções com observação/interpretação/ação.

## Failure modes

- **Importação em massa**: adotar vários repos de uma vez → seja seletivo (dedupe-rule do AGENTS.md).
- **Classificar sem inventário**: "Adotar" algo que o vault já tem → leia `04-SYSTEM/AGENTS.md` antes de classificar.
- **Fato misturado com julgamento**: observação e recomendação no mesmo campo → separe `[obs]` de `[interp]`.
- **"Nenhum problema" sem caso plantado**: veredito limpo sem negativo → plante um caso antes de reportar limpo.
