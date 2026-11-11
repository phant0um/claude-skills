---
name: diagram-build-architecture-mode
kind: reference
type: skill
status: active
parent: "[diagram-build](../SKILL.md)"
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. assets/template.html existe (diagram-build/assets). Classes e regras de layout nao verificadas renderizando um SVG."
---

# Archify — Architecture Mode: SVG à mão (reference)

Ler só quando for desenhar SVG à mão: renderer indisponível (sem Node/ajv) ou skill sem shell. O renderer e o Cardinal Rule ficam no SKILL.

## Fallback à mão

Copie `assets/template.html` e posicione o SVG manualmente. Estude o diagrama trabalhado dentro do template para ver idiomas de coordenada, siga o Design System abaixo e rode o checklist mecânico antes de entregar.

Padrões de classe (sem cor inline):

```svg
<rect x="X" y="Y" width="W" height="H" rx="6" class="c-mask"/>
<rect x="X" y="Y" width="W" height="H" rx="6" class="c-backend" stroke-width="1.5"/>
<text x="CX" y="CY" class="t-primary" font-size="11" font-weight="600" text-anchor="middle">API Server</text>
<text x="CX" y="CY+16" class="t-muted" font-size="9" text-anchor="middle">FastAPI :8000</text>
```

## Design system

Preenchimentos de componente: `c-frontend` (clientes/UI), `c-backend` (serviços/APIs), `c-database` (stores/caches), `c-cloud` (infra gerenciada), `c-security` (auth/secrets), `c-messagebus` (Kafka/filas), `c-external` (terceiros). Acentos de texto: `t-<mesmo tipo>` mais neutros `t-primary` / `t-muted` / `t-dim`. Setas: `a-default`, `a-emphasis` (hot path), `a-security` (tracejada), `a-dashed` (async); sempre defina `stroke-width` e use `marker-end="url(#arrowhead[-variant])"` com a classe correspondente. Boundaries: `c-security-group` (rosa tracejado), `c-region` (âmbar tracejado), `c-lane` (swimlane). Tipografia: JetBrains Mono herdada do root; nomes 11–12px, sublabels 9px, anotações 8px, mínimos 7px.

## Hard layout rules

- **Dois retângulos**: `c-mask` opaco primeiro, `c-<tipo>` por cima; fill semitransparente deixa seta vazar.
- **Setas antes dos componentes** na ordem do documento (SVG pinta em ordem).
- **Empilhamento vertical**: ≥40px entre componentes; conectores de barramento (20px) ficam no gap, nunca sobre caixas.
- **Padding de boundary**: `y` = `y` interno − 30; `height` = `height` interno + 50; baseline do label 18px abaixo do topo.
- **Legenda**: fora de TODOS os boundaries, ≥20px abaixo do mais baixo; aumente o viewBox se preciso.

## Checklist mecânico (fallback)

1. `grep -E 'fill="(#|rgb)|stroke="(#|rgb)' out.html` dentro do SVG não retorna nada além das defs do template.
2. Todo `c-<tipo>` tem um `c-mask` de geometria idêntica logo antes.
3. Todas as setas (`<line>`/`<path>`) vêm antes de todos os retângulos de componente.
4. max(y + height) sobre todos os elementos SVG: viewBox excede em ≥20px; idem x/width.
5. Legenda com y abaixo de `y + height` de todo boundary.
6. `.toolbar`, blocos `<script>` e CSS `:root` / `[data-theme]` intocados (são o toggle de tema e o menu de export).
