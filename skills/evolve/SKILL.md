---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: evolve
description: "Use when: extrair padrões reutilizáveis da SESSÃO CORRENTE para cristalizar como novas skills — escaneia a conversa por técnicas que funcionaram e propõe criação de skill com confidence score. Diferente de [skillify](../skillify/SKILL.md) (que formaliza workflow MANUAL repetido 3+ vezes em skills no resolver); evolve opera sobre o que acabou de acontecer nesta sessão."
slug: evolve
version: 1.2
effort: low
trigger: "/evolve"
updated: 2026-11-10
consolidated-by: R3 (absorveu meta-learn, codex-retrospective como modos)
triggers:
  positive:
    - "extrair padrões reutilizáveis da sessão"
    - "cristalizar como nova skill"
    - "propor criação de skill com confidence score"
  negative:
    - "padrão único e efêmero"
    - "código de produção a refatorar"
reads:
  - 04-SYSTEM/automation/skills/
  - 04-SYSTEM/automation/agents/
writes:
  - 04-SYSTEM/automation/skills/**
  - 04-SYSTEM/system/state/context/hot.md
  - 06-GENERATED/tasks/lessons.md
  - 04-SYSTEM/automation/registry/skill-stubs.json
  - 04-SYSTEM/automation/registry/agent-registry.*
  - 04-SYSTEM/automation/agents/_index/moc-skills.md
  - 04-SYSTEM/scripts/run-skill-evals.py
  - 04-SYSTEM/automation/evals/fixtures/**
  - 04-SYSTEM/automation/workflows/portas/**
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7+W8: corpo completo lido pelo shield (opus, somente leitura); W3/W4b/W7b/W7c: Fase 4 alinhada ao PASSO 0 do skillify e writes; W8: Reportar de porta/rotina e Completion sem pin de modelo; checks frontmatter/lint/evals verdes; 227 linhas, 17 secoes"
---
# Skill: /evolve

Ao ser invocado com `/evolve`, executa:

## Fase 1 — Retrospectiva da Sessão

Varrer o contexto da conversa atual e identificar:

```
□ Padrões que funcionaram (abordagem que resolveu problema real)
□ Heurísticas descobertas (regra que se revelou útil, não óbvia)
□ Sequências de passos que não existiam como skill
□ Correções aplicadas que deveriam ser permanentes
□ Decisões recorrentes que poderiam ser automatizadas
```

**Filtro de qualidade:** só capturar se:
- Não é óbvio da documentação existente
- Resolveu um problema real (não teórico)
- Aplicável em sessões futuras (não apenas nesta)
- Não duplica skill existente em `04-SYSTEM/automation/skills/`

## Fase 2 — Draft da Nova Skill

Para cada padrão identificado, gerar draft aplicando **princípios Pocock de qualidade** (ver writing-great-skills-matt-pocock):

```markdown
***

# Skill: <Nome>

## Contexto
<Qual problema resolve e em que situações. Nomeie 1 leading word: termo curto que o modelo já conhece e que ancora o comportamento (ex.: ratchet, seam, tracer bullet), usado no lugar de uma frase descritiva.>

## Protocolo
<Passos concretos, não abstratos. Cada passo termina em completion criterion: checkable + exhaustive.>

## Completion
- [ ] <critério checkable>

## Failure modes
- **<modo>**: <sintoma> → <defesa>

## Quando NÃO usar

- Padrão único e efêmero — não vale cristalizar em skill.
- Código de produção a refatorar — use code-optimize.
- Técnica já coberta por skill existente — estender, não duplicar.

```

**Quality gate antes de apresentar ao usuário:**
- [ ] Leading word identificado (conceito compacto do pretraining)
- [ ] Completion criterion é checkable (agent distingue done de not-done)
- [ ] Failure modes documentados (mínimo 2)
- [ ] No-op test aplicado nas restrições (NUNCA que não muda comportamento = deletar)
- [ ] Se skill >80 linhas: considerar progressive disclosure (splitar reference em `references/`)

## Fase 3 — Triagem e Decisão

Apresentar ao usuário:

```
EVOLVE REPORT — <data>

Padrões candidatos: N

[1] <nome> — confiança: X.X
    Capturado de: <resumo do que aconteceu>
    Aplicável quando: <trigger>
    → Destino? [1 linha em porta | porta nova | rotina | skill | descartar]

[2] ...

Ação: confirme o destino de cada padrão; a Fase 3 mostra a recomendação do skillify PASSO 0 (o menor destino que resolve) e a Fase 4 executa o destino confirmado. Descartados ficam no log mas não viram nada.
```

## Fase 4 — Criação

evolve descobre; [skillify](../skillify/SKILL.md) materializa
(adr-nx-017). Para cada padrão aprovado na Fase 3:

1. Destino confirmado na Fase 3 (o PASSO 0 de skillify já o recomendou): 1 linha em porta existente: acrescentar a linha (skillify PASSO 0 item 1; `portas/` pede rebaseline humano); porta nova ou rotina: só destino e contrato, sem criar workflow (skillify PASSO 0 itens 2-3). Se for skill, executar os PASSOS 2-5: gerar o arquivo em
   `04-SYSTEM/automation/skills/<domínio>/<slug>/SKILL.md` (skills ficam por domínio:
   `dev/`, `meta/`, `reasoning/`, …), eval cross-modal, registro (skillify PASSO 4) e
   smoke test com o caso da sessão. O PASSO 1 (capturar o workflow) já está
   feito: é o draft da Fase 2.
2. Registrar em `04-SYSTEM/system/state/context/hot.md` se alta frequência esperada.
3. Reportar: "Skill `<slug>` criada. Trigger: `<quando usar>`. Smoke test: <resultado>." Para porta ou rotina: "Destino `<porta|rotina>` entregue: `<linha ou contrato>`. Rebaseline humano pendente."

Os triggers continuam separados: `/evolve` parte da sessão corrente, `skillify`
parte de um workflow manual repetido.

## Validation Gate (adotar só com evidência)

Mudança (skill nova, patch, upgrade) só é **adotada** — não apenas feita — com evidência de melhoria:

- **Evidência obrigatória (1+):** métrica de sessão (tempo/erros), benchmark/evals PASS/FAIL ou review humano explícito. Sem evidência, a mudança fica em staging.
- **Staging → adopt:** criar/editar em staging (rascunho + version bump) e promover ao caminho canônico só após a evidência — nada ao vivo sem adopt explícito.
- **Linha em `portas/` (Fase 4):** o rebaseline humano conta como review humano explícito e é o adopt; até ele, a linha está em staging.
- **Backup antes de mudar:** snapshot (git commit ou cópia) do estado anterior em toda edição — rollback sempre possível.
- **Redact antes de replay:** ao reaproveitar padrão de sessão antiga, remover dados sensíveis (tokens, paths pessoais, conteúdo privado) antes de reproduzir.
- **Snapshot + rollback:** se a evidência pós-adopt piorar (regressão), restaurar o snapshot e registrar no lessons log.

## Self-Improvement Loop Integration

When a sessão reveals that rotinas/agents/skills have most prerequisites of the autoresearch-loop pattern but are missing one (typically the **lessons log**), do NOT create a new skill — patch the existing rotina/agent/skill to close the loop.

The 5 prerequisites (from `autoresearch-loop` concept): fitness function, executor, keep-or-revert, lessons log, budget.

**Pattern:** add a bash-only `## Self-improvement log` block that appends 1 line of metrics to `06-GENERATED/tasks/lessons.md`. Zero AI cost.

**When NOT to patch:** rotinas that are output-only (daily-brief, x-thread-weekly) or one-shot (vault-backup) are not loops by design — forcing lessons log on them is over-engineering.

**Skill-to-rotina integration:** when auditing existing skills after upgrades, check if new/upgrade skills fit into existing rotinas as conditional triggers.

**Multi-component phase injection:** when an existing skill fills a gap in multiple components (skills, agents, rotinas), inject it as a new phase in each — with skip conditions per component. Inverse of skill-to-rotina: existing skill → find components.

**Community skill gap analysis:** when comparing external tool skills against vault agents, inject structured protocols into existing agents rather than creating new skills. Classify gaps as covered/partial/gap, inject protocol into the owning agent, divide labor between overlapping agents.

**Full-cycle community skill mapping:** when user asks about a batch of external skills, follow the full cycle: research → map (covered/partial/gap) → integrate partials → close gaps by extending agents → create rotina if structural gaps unmonitored → log.

**Gap → extend agent vs create skill:** when a gap maps to an agent's territory but the agent lacks the capability, extend the agent with a new phase rather than creating a standalone skill. Decision criterion: would a new skill duplicate the agent's routing? If yes → extend the agent. If no → create a skill.

**Vault sources as build blueprints:** when creating a study plan or career roadmap and the user asks about exploring existing vault sources as projects to build from scratch, map already-ingested source pages to constructible projects. Scan sources for architecture-describing content, extract reduced-scope MVP shape, integrate as "parallel projects" in study plan phases. This is the inverse of normal skill-source-audit (vault sources → learning goals, not external repos → vault). Session 2026-06-24: 7 projects mapped from vault sources (React Doctor, Knowledge Graph, Session Search CLI, Quant Loop, AI Scouting Agent, Security Auditor, Memory Layer) integrated into career-uplift 6-phase plan.

**Skill-authoring quality:** when drafting new skills in Fase 2, apply Matt Pocock's writing-great-skills principles — leading words, progressive disclosure, no-op pruning. See writing-great-skills-matt-pocock.

**Skill audit:** when auditing existing skills against Pocock principles (sprawl, completion criterion, no-op risk, failure modes), check each skill against those four dimensions.

**Orphan detection:** when user asks about unused skills or during monthly audit, list skills with no active reference (wikilink, resolver entry, `calls`) and decide per skill: integrate or archive.

**Bulk frontmatter insertion:** when N files need a frontmatter field added (`updated:`, `version:`), use Python line-insertion before closing `---`, not `sed` (breaks on BSD with emoji/variation-selector chars). For files without frontmatter, prepend minimal block.

**Rotina commit gates + gitignored paths:** vault `.gitignore` tracks only `04-SYSTEM/automation/agents/` and `04-SYSTEM/automation/skills/`. Commit gates referencing `04-SYSTEM/record/wiki/` or `06-GENERATED/` silently fail. Use `git add -u` for modified-only (not `git add -f <dir>` which sweeps untracked too).

## Session 2026-06-24 — Pocock Audit + Skill Creation Summary

This session applied Pocock's "writing-great-skills" framework to audit and upgrade the entire vault skill library:

- **37→43 skills** (6 created: tdd, implement, prototype, resolving-merge-conflicts, to-issues, triage)
- **Completion criterion: 4→41/43 (95%)** — added ## Completion to 35 skills (checkable + exhaustive)
- **Failure modes: 4→41/43 (95%)** — added ## Failure modes to 35 skills
- **No-op prune: 2 deleted** from code-optimize + meta-meta-prompt
- **6 skills upgraded** (P0-P5): diagnose v2 (tight loop), tdd (new), git-guardrails hook, grill-me (Doc Capture), decisions (domain modeling), code-optimize (deep modules)
- **14/14 Pocock skills covered** (6 upgrades + 5 created + 2 equivalents + 1 via CLAUDE.md)
- **8 leading words** (ratchet, gate, probe, tight, deep, tracer bullet, seam, throwaway)
- **3 rotina integrations**: revisao-semanal F3.4 (diagnose + grill-me), rotina-audit-mensal §6.8 (code-optimize)
- **5 agent integrations**: forge (deep modules), extend (tight loop), spec (Doc Capture), verify (diagnose), orchestrator (deep modules)

## Completion

- [ ] Fase 1 retrospectiva: padrões que funcionaram identificados (não teóricos)
- [ ] Fase 2 drafts gerados com frontmatter completo (name, version, trigger, confidence; sem pin de modelo, ver skillify)
- [ ] Fase 3 triagem apresentada ao usuário com confidence scores
- [ ] Fase 4: destino de cada padrão decidido (skillify PASSO 0); skills aprovadas criadas via PASSOS 2-5, em `04-SYSTEM/automation/skills/<domínio>/<slug>/SKILL.md`, com smoke test
- [ ] Skills não-duplicadas (verificado contra `04-SYSTEM/automation/skills/` existente)
- [ ] Máximo 3 novas skills por /evolve (priorização forçada)
- [ ] Hot.md atualizado se alta frequência esperada

## Failure modes

- **Confidence inflation**: padrão usado 1x marcado como confidence 0.8 → mínimo 2 usos para confidence > 0.6
- **Skill duplicada**: criar skill que já existe com outro nome → sempre grep `04-SYSTEM/automation/skills/` antes
- **Padrão teórico**: capturar padrão que não resolveu problema real → só capturar se resolveu algo concreto na sessão
- **Over-creation**: 5+ skills propostas num único /evolve → forçar priorização, máximo 3

***

## Restrições

- NUNCA criar skill para padrão usado apenas 1x nessa sessão sem justificativa
- NUNCA duplicar skill existente — verificar `04-SYSTEM/automation/skills/` antes
- Confidence < 0.6 → apresentar mas não recomendar criação
- Máximo 3 novas skills por `/evolve` — forçar priorização

## Exemplo

**Contexto:** sessão identificou que ao delegar para subagente sem injetar skills, o agente produzia outputs genéricos.

**Output:** Skill `skill-injection-at-delegation.md` criada. Conteúdo: protocolo de injetar skills no prompt do subagente antes de delegar. Trigger: qualquer delegação via Agent tool.

## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO META-LEARN** — [meta-learn](meta-learn.md)
- **MODO RETROSPECTIVA DE SESSÃO** — [codex-retrospective](codex-retrospective.md)
