---
name: sintese-cruzada
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/pipeline/report-synthesis/SKILL.md
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Os wikilinks A, B, C sao placeholders do template, nao links. Destino 03-RESOURCES/concepts/dev-foundations existe."
---

## F3.8 Síntese Cruzada entre Domínios

**Princípio**: vault armazena por domínio mas raramente cruza domínios. Síntese
cruzada gera insight novo confrontando obras/conceitos de áreas distintas.

### Quando ativar
- Rodar 1×/semana (fechamento do pipeline-semanal), não diário.
- Mínimo 2 domínios com ≥1 concept novo na semana.

### Fluxo
1. Selecionar 2-3 concepts/entities de domínios diferentes (preferir os com mais
   backlinks novos na semana).
2. AI call: identificar tensão, convergência e analogia entre eles.
3. Adicionar seção **"Meu entendimento"** (síntese própria, 3-5 linhas,
   não resumo das fontes — interpretação).
4. Escrever nota em `03-RESOURCES/concepts/dev-foundations/sintese-$(date -I).md`
   com wikilinks para os concepts cruzados.

### Output
```markdown
---
title: "Síntese Cruzada <DATA>"
type: cross-domain
created: YYYY-MM-DD
links: A, B, C
---

## Tensão
[onde discordam]

## Convergência
[onde apontam pro mesmo lugar]

## Meu entendimento
[interpretação própria — não resumo]
```

### Regra
- **Domínios distintos obrigatório** — cruzar 2 do mesmo domínio não conta.
- **"Meu entendimento" é mandatório** — sem ele, é só resumo (vira ruído).
- **Skip se <2 domínios** com material novo.
