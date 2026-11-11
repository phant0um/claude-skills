---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: reason-judge
description: "Use when: julgar qualidade de output por rubrica · caso borderline, de governança ou adversarial. Weigh output quality by rubric (score + justificativa), não check binário. Gate borderline / governança / adversarial."
version: 1
source: vault-michel
created: 2026-07-15
updated: 2026-07-25
tags: [skill, reasoning, evaluation, llm-as-a-judge, gate]
model-profile: deep
reads: []
writes: []
triggers:
  positive:
    - "julgar output por rubrica"
    - "caso borderline de governança ou adversarial"
  negative:
    - "check binário basta (core/verify)"
    - "invariante hard de segurança"
    - "1 passagem com pressa"
consumes: ["output", "rubric"]
tools: []
references:
  - 03-RESOURCES/concepts/llm-ml/llm-as-a-judge
verifier: ["Require rubrica ponderada, score com justificativa por ponto, mean+variance e >=2 passagens em borderline."]
human_gate: true
reviewed-scope: "checagem mecanica + semantica: 5/5 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 8 secoes, 115 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---


# judge

**Weigh** an output against a weighted rubric and emit a numeric score + justificativa — não um PASS/FAIL cego. Usar quando "bom o suficiente" é fuzzy (síntese, escrita pública) e um `verify` binário perde nuance.

Distingue de skills próximas:
- `verify` — trajectory review binário (fez o passo certo? sim/não). Judge dá **grau**.
- `council` — painel multi-modelo + juiz frontier sintetiza melhor versão. Judge é **1 juiz, 1 rubrica, 1 score**.
- Guards de segurança — invariantes hard (nunca "grau"). Judge não substitui gate crítico.

Conceito canônico: llm-as-a-judge.

## Mecânica

1. **Definir rubrica** — pontos avaliáveis `k` com peso `w_k` (Σw = 1). Ex. triagem: relevância 0.4 · profundidade 0.3 · fonte-confiável 0.2 · não-duplicado 0.1.
2. **Pontuar cada ponto** `e_k ∈ [0,1]` com 1 frase de justificativa por ponto.
3. **Score final** `s = Σ w_k · e_k` — calculado em código a partir dos `e_k` devolvidos, não pelo modelo.
4. **Determinismo via structured outputs + effort baixo** — `temperature`/`top_p`/`top_k` retornam 400 nos modelos em uso (Opus 4.7+, Sonnet 5, Fable); não setar. Determinismo vem do schema de saída fixo e da rubrica, não do sampling.
5. **Reportar mean + variance**, não 1 score solo. 1 passagem ≠ veredito (non-determinism). ≥2 passagens em borderline.

Saída padrão:
```
score: 0.72 (var 0.03)
- relevância 0.9: bate 2 áreas ativas do vault
- profundidade 0.5: síntese rasa, sem contradição explorada
- fonte 0.8: primária, datada
- dup 0.6: overlap parcial com nota-x
veredito: standard (0.60–0.80) → aceitar com flag
```

## Thresholds (tunáveis)

| Faixa | Ação |
|-------|------|
| `s ≥ 0.80` | aceitar |
| `0.60 ≤ s < 0.80` | aceitar com flag / revisar 1 ponto fraco |
| `s < 0.60` | rejeitar → escalar tier (`economy→standard`, regra 2 do router) ou humano |

## Cross-model (obrigatório em alta-consequência)

Juiz **≠** modelo que gerou. Self-preference: LLM favorece o próprio output (Panickssery 2024); self-enhancement: juiz é leniente consigo. Gerador `luna` → juiz `sol`/`opus`. Modelo A gera, modelo B (provedor distinto) julga = evita "grade sua própria homework". Runtime resolve via perfil `deep` (§ router).

## Onde plugar (gates existentes)

- **skill-audit PARTE A** — Pocock 0-8 já é rubrica; judge formaliza a régua + cross-model.
- **governance-audit** — score de aderência a intent-boundary por seção.

## Completion

- [ ] Rubrica explícita com pesos somando 1
- [ ] Cada `e_k` tem justificativa de 1 frase
- [ ] `s = Σ w_k·e_k` calculado
- [ ] sem override de sampling (400 em Sonnet 5); ≥2 passagens se borderline; variance reportada
- [ ] Juiz ≠ gerador quando alta-consequência
- [ ] Veredito mapeado a threshold + ação

## Failure modes

- ❌ **Score sem justificativa** — número solo não é auditável. Toda nota carrega 1 frase.
- ❌ **1 passagem = veredito** — non-determinism. Borderline exige mean+variance de ≥2 runs.
- ❌ **Juiz = gerador em alta-consequência** — self-preference infla. Cross-model.
- ❌ **Judge em constraint rígido** (numérico, procurement, segurança) — usar verificação formal/heurística, não juiz fuzzy. Judge é p/ qualidade fuzzy, não fato binário.
- ❌ **Rubrica sem pesos** — todo ponto igual esconde o que importa. Pesos explícitos.
- ❌ **Golden set não versionado** — sem baseline, mudança de rubrica = aposta cega (silent regression).

## Quando NÃO usar

- **Check binário basta** (PASS/FAIL objetivo, trajectory review) — usar um check binário determinístico; judge adiciona grau onde não há grau.
- **Invariante hard de segurança** — guards não recebem "score"; falha é falha, sem nuance.
- **1 passagem com pressa** — judge exige ≥2 passagens em borderline; sem budget para repetição, não usar.
- **Síntese/escrita de autoria** — julgar trabalho de terceiros com rubrica; não usar judge para produzir conteúdo.

Disambiguation: `reason-judge` pontua por rubrica (1 juiz, 1 score); um check binário determinístico complementa (fez o passo? sim/não); `council` é painel multi-modelo que sintetiza — judge é mais barato e determinístico que council quando não há disputa de versões.

## Relacionados

- llm-as-a-judge — teoria, vieses, meta-eval
- verify — review binário (complementar)
- [governance-audit](../drift-review/governance-audit.md) — gate de intent-boundary
- model-router — perfil `deep` p/ juiz cross-model
