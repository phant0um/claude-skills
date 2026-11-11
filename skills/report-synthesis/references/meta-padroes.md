---
name: meta-padroes
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/pipeline/report-synthesis/SKILL.md
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. A secao 'Perfil de modelo' citada existe em report-synthesis/SKILL.md."
---

## F3.6 Meta-padrões Semanais

**Princípio**: pipeline semanal acumula sources de 7 dias. Padrões que emergem
entre clusters são invisíveis source-a-source. F3.6 é a camada de síntese
que faz knowledge compounding visível.

### Quando ativar

- **Mínimo 3 sources** no run para identificar meta-padrão
- <3 sources → skip F3.6 (não há volume para padrão)
- F3.6 roda após F3.1/F3.2 (consome clusters + cross-connections)

### Fluxo

Modelo pelo perfil declarado no §Perfil de modelo — o pin local `Opus 4.8 · low` foi removido em 2026-08-31: contradizia a propria frase "esta skill nao mantem pins locais por fase", e o model-catalog registra que o Opus 5 domina o 4.8 ao mesmo preco.

AI call com F3.1 clusters + F3.2 cross-connections do run atual. Identifica:

1. **Meta-padrões**: temas em 3+ sources com ângulos diferentes (não repetição —
   evolução do conceito)
2. **Convergências**: 2+ sources concordam (citação dupla obrigatória)
3. **Contradições persistentes**: contradições que persistem entre clusters
4. **Gaps acumulados**: tópicos que apareceram mas não foram aprofundados
5. **Top 3 insights da semana**: o que mudou no vault que não era óbvio
   source-a-source

### Output integrado ao relatório semanal

```markdown
## F3.6 Meta-padrões semanais

| Padrão | Sources | Evolução |
|--------|---------|----------|
| <tema> | A, B, C | <como evoluiu> |

### Top 3 insights da semana
1. <insight não-óbvio>
2. ...
3. ...
```

### Regra

- **Mín 3 sources** para identificar padrão — 2 sources = convergência, não padrão
- **Convergências com citação dupla** — 2+ sources concordando com referência
- **Sem inventar** — se não há padrão claro, reportar "nenhum meta-padrão significativo"
- **Top 3 insights** — obrigatório mesmo se curtos
