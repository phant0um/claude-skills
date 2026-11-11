---
name: code-optimize-deep-modules
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/dev/code-optimize/SKILL
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Conteudo conceitual, sem path ou comando a conferir."
---

# Deep Modules (ref de code-optimize)

> Origem: improve-codebase-architecture. Leia só no PASSO 2.7 do SKILL.

## Deep Modules (de improve-codebase-architecture)

> **Leading word: deep.** Module com interface simples e implementação rica. O oposto de shallow (interface tão complexa quanto implementation).

### The Deletion Test
Para suspeito shallow module: "Deletar este module concentraria complexidade, ou só moveria?" Se "concentra" → deepening opportunity. Se "só move" → module é shallow, candidado a merge.

### Friction signals a procurar
- Entender 1 conceito requer bouncing entre muitos modules pequenos
- Shallow modules: interface quase tão complexa quanto implementation
- Pure functions extracted para testability, mas bugs reais vivem em como são chamadas (falta de locality)
- Modules tightly-coupled leaking across seams
- Código untested ou hard-to-test via interface atual

### Deepening opportunities
Transformar shallow → deep:
1. Combinar modules pequenos em um maior com interface simples
2. Mover complexidade para trás de interface menor
3. Reduzir número de seams (pontos de acoplamento) — ideal é 1 seam por feature

> Deep modules melhoram testability e AI-navigability: menos context switches para entender uma feature.

---
