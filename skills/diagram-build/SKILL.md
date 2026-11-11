---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: diagram-build
description: Create professional architecture, workflow, sequence, data-flow, and lifecycle/state diagrams as standalone HTML files with SVG graphics, a built-in dark/light theme toggle, and one-click export to PNG / JPEG / WebP / SVG. Accepts plain-language descriptions or pasted Mermaid code (flowchart, sequenceDiagram, stateDiagram) and lays the diagram out from scratch in diagram-build style. Use when the user asks for system architecture diagrams, infrastructure diagrams, security diagrams, network topology, technical workflows, approval flows, runbooks, CI/CD flows, API call sequences, request lifecycles, data pipelines, PII boundaries, data lineage, state machines, lifecycle diagrams, or asks to convert/beautify a Mermaid diagram.
license: MIT
metadata:
  version: "2.6"
  author: tt-a1i
  based_on: Cocoon-AI/architecture-diagram-generator (MIT, v1.0)
updated: 2026-09-24
reads: []
writes: []
triggers:
  positive:
    - "criar diagrama de arquitetura/workflow/sequência"
    - "diagrama HTML com SVG"
    - "data-flow ou state diagram standalone"
  negative:
    - "texto simples basta"
    - "diagrama em imagem estática"

reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 4/4 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 11 secoes, 310 linhas; drift R13/R14: 2 achados resolvidos (decisoes D1-D4 A / SKILL_REF)"
reviewed-by: R15 (claude-sonnet; decisoes D1-D4 A)
reviewed: 2026-10-04
---
 Archify Skill

Create professional technical diagrams as self-contained HTML files with inline SVG, a theme toggle, and a built-in image/SVG export menu.

Every diagram ships with a **dark/light theme toggle** (persists in `localStorage`, respects `prefers-color-scheme`), an **export menu** (copy PNG to clipboard; download PNG/JPEG/WebP rasterized natively at up to 4× resolution; download a **dual-theme SVG** that follows the embedding host's `prefers-color-scheme` — ideal for GitHub READMEs), and a **CSS-variable color system** that keeps both themes consistent.

## Quando NÃO usar

- **Diagrama simples embutido em nota** — Mermaid inline basta; diagram-build gera HTML standalone.
- **Rascunho rápido para discussão** — protótipo de diagrama não precisa de renderer.
- **Diagrama em doc de terceiros** — diagram-build é para artefatos do vault.

Disambiguation: `diagram-build` gera HTML standalone com SVG; `excalidraw` é ferramenta externa (hand-drawn JSON) — use `diagram-build` para diagramas no vault; Mermaid inline cobre casos simples — diagram-build para entregável.


## Setup (one-time, renderer modes only)

`renderers/`, `schemas/`, `assets/template.html`, `package*.json` e `LICENSE` são vendorizados de `tt-a1i/archify` @ `v2.6.0` (MIT), importados em 2026-09-24; `UPSTREAM.json` lista cada arquivo com o blob SHA da tag. Não editar à mão (o drift-structural acusa `VENDOR_MODIFIED`): atualizar reimportando de uma tag e reescrevendo o `UPSTREAM.json`. Os READMEs citam caminhos do repo upstream (`archify/...`).

The four typed renderers validate JSON against schemas via `ajv`. From this skill's folder:

```bash
npm install
```

Without it the renderers still run — they print a warning and skip schema validation, keeping their own layout checks. The **generated HTML never has dependencies**; only the renderers do.

If you have no shell access at all (e.g. the skill was added as project knowledge), fall back to architecture mode for every request: hand-place SVG into `assets/template.html`. Se for desenhar à mão, leia [architecture-mode](references/architecture-mode.md) antes (Design System, layout rules, checklist mecânico).

## Choosing a Diagram Type

| Type | Use for | How |
|------|---------|-----|
| `architecture` | System components, cloud resources, services, security boundaries, infrastructure | `renderers/architecture/render-architecture.mjs` + JSON (or hand-place SVG when renderers can't run) |
| `workflow` | Technical flows, approval gates, tool calls, runbooks, CI/CD, incident response | `renderers/workflow/render-workflow.mjs` + JSON |
| `sequence` | API call chains, request lifecycles, cache fallback, async traces, return paths | `renderers/sequence/render-sequence.mjs` + JSON |
| `dataflow` | Pipelines, ETL/ELT, PII isolation, lineage, warehouse sync, consumers | `renderers/dataflow/render-dataflow.mjs` + JSON |
| `lifecycle` | State machines, status transitions, wait states, retries, terminal states | `renderers/lifecycle/render-lifecycle.mjs` + JSON |

Trigger phrases: "architecture/system/cloud diagram" → `architecture` (unless clearly process-oriented). "workflow/flow/process/runbook/approval/CI-CD/incident" → `workflow`. "sequence/interaction/call chain/who calls whom" → `sequence`. "data flow/pipeline/ETL/lineage/PII/governance" → `dataflow`. "state/status/lifecycle/state machine/retry/terminal" → `lifecycle`.

## Mermaid as an Input Dialect

When the user pastes Mermaid code, do NOT try to render or parse it mechanically — read it for structure and **lay out from scratch** in the matching diagram-build mode:

| Mermaid | Archify mode | Mapping |
|---------|--------------|---------|
| `flowchart` / `graph` | `workflow` (or `architecture` if it's a component map) | `subgraph` → lane or region boundary; node shape `{}` (diamond) → decision/security node; `-->` labels → edge labels (use sparingly); `classDef`/`style` → nearest semantic type |
| `sequenceDiagram` | `sequence` | `participant` → participants (pick semantic `type` from the name); `->>` → message, `-->>` → `return` variant; `Note` → message `note`; `rect` blocks → segments |
| `stateDiagram` | `lifecycle` | states → states (pick `start`/`active`/`waiting`/`success`/`failure` from names); `[*]` start/end → `start` type / `terminal` lane; transition labels → event-like labels |

Drop Mermaid styling; keep only the topology and meaning. You choose grouping, lane order, and what deserves emphasis — that judgment is the product.

## Renderer Modes (workflow / sequence / dataflow / lifecycle)

All four modes follow the same loop:

1. **Read first**: the schema (`schemas/<type>.schema.json`) — copy its patterns instead of guessing field shapes.
2. Write `<name>.<type>.json`.
3. Render: `node renderers/<type>/render-<type>.mjs <input>.json <output>.html` (paths relative to this skill's folder).
4. If it fails, the error names the JSON path or the fix (thresholds, valid ranges, which knob to change). Fix the JSON and re-run; never edit the renderer.

Schema violations exit non-zero with path-prefixed messages like `/nodes/3 (id/label: "router") must NOT have additional properties`. The renderers additionally fail fast on layout problems: node/state overlap (including cross-lane), labels colliding with nodes or other labels, labels wider than their node, out-of-range columns/rows, too-short edges, and legends outside the viewBox. CJK text is measured at double width automatically.

### Workflow

```json
{
  "schema_version": 1,
  "diagram_type": "workflow",
  "meta": { "title": "Release Workflow", "subtitle": "PR to production", "output": "release.html" },
  "lanes": [ { "id": "dev", "label": "Developer" }, { "id": "ci", "label": "CI" } ],
  "nodes": [
    { "id": "pr", "lane": "dev", "col": 0, "type": "frontend", "label": "Open PR", "sublabel": "feature branch" },
    { "id": "build", "lane": "ci", "col": 1, "type": "backend", "label": "Build", "sublabel": "lint + test", "tag": "blocking" }
  ],
  "edges": [
    { "from": "pr", "to": "build", "label": "webhook", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop" }
  ],
  "cards": []
}
```

**Layout budget**: 6 columns (`col` 0–5) at fixed x positions `[88, 220, 300, 430, 500, 625]` — columns 1↔2 and 3↔4 are only 70–80px apart, so default-width (92px) nodes in those adjacent columns of the same lane overlap; skip a column or shrink `width`. Lane content width is 640px. Omit `meta.viewBox` — the renderer sizes height to the lane count automatically. Edge routes: `straight`, `drop` (bend between lanes; `bias` 0–1 picks where), `outside-right`, `return-left`, `bottom-channel`, `up-channel`, or explicit `via` points. Keep adjacent-step edges unlabeled; reserve labels for cross-lane transitions, approvals, async writes, and returns.

### Sequence

```json
{
  "schema_version": 1,
  "diagram_type": "sequence",
  "meta": { "title": "Cache Miss Request", "subtitle": "auth and cache fallback", "output": "cache-miss.html" },
  "participants": [
    { "id": "web", "type": "frontend", "label": "Web App", "sublabel": "React UI" },
    { "id": "api", "type": "backend", "label": "API", "sublabel": "handler" }
  ],
  "segments": [ { "from": 160, "to": 320, "label": "01 / AUTH" } ],
  "messages": [
    { "from": "web", "to": "api", "y": 200, "label": "GET /data", "variant": "emphasis" },
    { "from": "api", "to": "web", "y": 290, "label": "200 JSON", "variant": "return" }
  ],
  "activations": [ { "participant": "api", "from": 190, "to": 300, "type": "backend" } ],
  "cards": []
}
```

**Layout budget**: participants sit at x = 62 + index×108, so a 920-wide viewBox fits at most 8. Message `y` must stay within `[160, viewBox_height − 83]`; messages that share horizontal space need ≥28px vertical separation; arrows need ≥60px horizontal span. `segments[].from/to` and `activations[].from/to` are **y pixel coordinates**, not participant ids. A taller `meta.viewBox` (default `[920, 760]`) buys more timeline room. Keep labels short: "GET /path", "verify JWT", "cache miss", "200 JSON".

### Dataflow

```json
{
  "schema_version": 1,
  "diagram_type": "dataflow",
  "meta": { "title": "Product Analytics", "subtitle": "events to consumers", "output": "analytics.html" },
  "stages": [ { "label": "Sources" }, { "label": "Ingest" }, { "label": "Store" } ],
  "nodes": [
    { "id": "web", "type": "frontend", "label": "Web App", "stage": 0, "row": 0, "sublabel": "clickstream" },
    { "id": "kafka", "type": "messagebus", "label": "Kafka", "stage": 1, "row": 0, "tag": "accepted events" }
  ],
  "flows": [
    { "from": "web", "to": "kafka", "label": "events", "classification": "PII touch", "variant": "emphasis" }
  ],
  "cards": []
}
```

**Layout budget**: 2–5 stages at x = 100 + stage×215; 5 rows (`row` 0–4) at y `[128, 242, 356, 470, 584]`; default node 112×58. Default viewBox `[940, 720]`. Flow labels are mandatory and asset-like ("clickstream", "identity map", "feature vectors"); put sensitivity in `classification` ("PII touch", "approved only", "non-PII"). Variants: `emphasis` = primary path, `security` = PII/policy/consent, `dashed` = async/batch.

### Lifecycle

```json
{
  "schema_version": 1,
  "diagram_type": "lifecycle",
  "meta": { "title": "Agent Run Lifecycle", "subtitle": "states and terminal outcomes", "output": "agent-run.html" },
  "lanes": [
    { "id": "main", "label": "Lifecycle phases" },
    { "id": "waiting", "label": "Interruptions" },
    { "id": "terminal", "label": "Terminal exits" }
  ],
  "states": [
    { "id": "queued", "type": "start", "label": "Queued", "lane": "main", "col": 0, "step": "01" },
    { "id": "running", "type": "active", "label": "Executing", "lane": "main", "col": 2, "step": "02" },
    { "id": "approval", "type": "waiting", "label": "Needs Approval", "lane": "waiting", "col": 0 },
    { "id": "done", "type": "success", "label": "Completed", "lane": "terminal", "col": 2 }
  ],
  "transitions": [
    { "from": "queued", "to": "running", "variant": "emphasis" },
    { "from": "running", "to": "approval", "label": "needs approval", "variant": "security", "fromSide": "bottom", "toSide": "right" },
    { "from": "running", "to": "done", "label": "success", "variant": "emphasis", "fromSide": "bottom", "toSide": "top" }
  ],
  "cards": []
}
```

**Layout budget — lane ids are semantic and reserved**: `main` is required and maps to the top phase band (cols 0–4); `terminal` maps to the bottom outcome band (cols 0–2); **every other lane id shares the single middle event band** (cols 0–2) — separate same-band states with different `col` or `yOffset`. Band headers render from your lane labels. Default viewBox `[980, 660]`. Keep transition labels event-like and sparse ("retry", "timeout", "cancel"); prefer state `tag`s, `step` numbers, and summary cards over label-heavy arrows. Put terminal states in the `terminal` lane so endings are unambiguous.

### Per-mode deep guidance

Each renderer has a README with its full design language (route presets, semantic types, story guidance): `renderers/workflow/README.md`, `renderers/sequence/README.md`, `renderers/dataflow/README.md`, `renderers/lifecycle/README.md`. Read the matching one before your first diagram of that mode in a session.

## Architecture Mode

Mesmo loop de schema → JSON → render. Prefira o renderer; SVG à mão é fallback.

```json
{
  "schema_version": 1,
  "diagram_type": "architecture",
  "meta": { "title": "Sample Web App", "subtitle": "3-tier SaaS on AWS", "output": "web-app.html" },
  "components": [
    { "id": "users", "type": "external", "label": "Users", "sublabel": "Browser", "pos": [40, 300] },
    { "id": "api", "type": "backend", "label": "API Server", "sublabel": "FastAPI :8000", "pos": [460, 300] },
    { "id": "db", "type": "database", "label": "PostgreSQL", "sublabel": ":5432", "pos": [680, 300] }
  ],
  "boundaries": [
    { "kind": "region", "label": "AWS us-west-2", "wraps": ["api", "db"] }
  ],
  "connections": [
    { "from": "users", "to": "api", "label": "HTTPS", "variant": "emphasis" },
    { "from": "api", "to": "db", "label": "SQL" }
  ],
  "cards": []
}
```

Render: `node renderers/architecture/render-architecture.mjs <input>.json <output>.html`.

**O renderer faz o trabalho mecânico**; você escolhe coordenadas e significado:

- **Coordenadas livres** — `pos: [x, y]` é o canto superior esquerdo; `size: [w, h]` default `[120, 60]`. Sem grid de lane/stage. `meta.viewBox` é opcional (auto-ajustado).
- **Boundaries por `wraps`** — liste os ids que `region` (âmbar tracejado) ou `security-group` (rosa tracejado) envolve; o renderer calcula o box com padding 30/50.
- **Connections** roteiam como edges (`variant`, `fromSide`/`toSide`, `route: straight|orthogonal-h|orthogonal-v|auto`, `via`, `labelDx/labelDy/labelAt`). Label vertical: empurre com `labelDy`.
- Ele falha cedo em overlap de componente, componente/boundary fora do canvas, ids de `wraps`/connection desconhecidos, label sobre componente e coordenada não finita.

### The Cardinal Rule: CSS classes, not inline colors
Nunca use cores inline. Use classes CSS. `class="red"`, não `style="color:red"`. Isso vale para qualquer modo. Motivo: o toggle troca custom properties; `fill="rgba(...)"` ou `stroke="#22d3ee"` fixos não mudam com o tema.

## Output

Um `.html` autocontido (CSS e SVG inline, ~19KB de JS para tema e export). Export dual-theme: o SVG baixado segue `prefers-color-scheme`; override manual via `svg[data-theme="..."]`.

## Completion

- [ ] Diagrama gerado respeita o layout/opção escolhida.
- [ ] Tudo fora de escopo listado como sugestão, não aplicado.
- [ ] Só uma arquitetura renderizada — sem concorrência visual no mesmo output.


Criterio de sucesso: `render-<tipo>.mjs` sai com código 0 e o HTML abre sem falha de layout; no fallback à mão, todos os itens de `architecture-mode` passam.

## Failure modes

- **Cor inline**: `style="color:red"` no SVG → quebra o tema dark/light; use classe CSS (Cardinal Rule).
- **Escopo aplicado sem pedido**: item fora do pedido entra no diagrama → liste como sugestão, não renderize.
- **Concorrência visual**: duas arquiteturas no mesmo output → renderize só uma.
- **Renderer para caso simples**: HTML standalone onde Mermaid inline basta → use Mermaid na nota.

