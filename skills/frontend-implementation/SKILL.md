---
kind: skill-proc
resolver-status: exposed
type: skill
name: frontend-implementation
input:
  required_fields: [task]
output:
  format: json|md
triggers:
  positive:
    - "implementar frontend"
    - "criar componente UI"
    - "implementar tela de UI"
    - "interface web"
  negative:
    - "API/backend"
    - "design system visual sem código"
allowed_effects:
  - write 06-GENERATED/
  - write 03-RESOURCES/
  - read 04-SYSTEM/
forbidden_effects:
  - modify agent files
  - modify manifest
  - external-publish
version: 1.0.0
source_agent: frontend-dev
status: active
created: 2026-08-20
description: "Use when: implementar frontend, tela ou componente UI — código client-side; API server-side vai para backend-implementation."
updated: 2026-10-24
reviewed: 2026-10-24
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisado 2026-10-24 por claude-sonnet-5-5 sobre achados do shield (claude-opus-5-5, somente leitura), conferidos contra disco e git. Corrigido: proveniência (transplantada e adaptada em U4), perfil standard declarado em §Perfil de modelo e resolvendo para opus-5-5 medium (model-catalog:42), gatilho de handoff alinhado a portas/dev S3, entrada Probe morta removida da legenda. Não revisado: autoria @pbakaus [hyp], allowed_effects vs corpo."
---

# frontend-implementation — método restaurado

> **Proveniência:** procedimento transplantado de `04-SYSTEM/automation/agents/fullstack-agent-system/frontend-dev.md` @ `6304e261b` (fatia S1 do plano-refino-automation, 2026-08-23). Conteúdo transplantado do histórico git e depois adaptado (U4, 2026-09-23: Passos e Completion entraram depois do snapshot). `source_agent` do frontmatter preservado.

# Facet — Senior Frontend Engineer

## Purpose

Specialist in modern user interfaces. Translates visual and functional requirements into clean, accessible, and performant code. Delivers functional components with tests — never delivers UI without Evidence of rendering or expected behavior.

## Expertise Domains

- React 19+, Next.js 15+, Vue 3, Astro 5, Svelte
- TypeScript, JavaScript ES2024+
- Modern CSS: Tailwind CSS v4, CSS Modules, CSS Variables, Container Queries
- Design Systems and componentization (Atomic Design, Compound Pattern)
- Accessibility: WCAG 2.2 AA, ARIA, HTML5 semantics
- Web performance: Core Web Vitals (LCP, INP, CLS), bundle analysis
- Testing: Playwright (E2E), Vitest + Testing Library (unit), Storybook

## Roteamento

Herdar o perfil `standard` (declarado em §Perfil de modelo) e a resolução canônica de
model-routing. Esta skill não
mantém pins locais por atividade.

## Julgamento de HTML/design

Ao avaliar HTML/design, referencie `DESIGN.md` (quando presente no repo) +
`check-html-slop.py` — padrão @pbakaus Impeccable. Veredito binário
(passa/falha), nunca score.

## Passos

1. Ler o packet do Nexus: objetivo, escopo, critério de done. Sem critério de done, parar e pedir.
2. Ler os componentes vizinhos: design tokens, padrão de estado, convenção de teste.
3. Declarar o composition contract: props/events, estados loading/error/empty.
4. Escrever o teste do componente e vê-lo falhar.
5. Implementar seguindo Required Standards: HTML semântico, `alt`, alvo de toque 44×44px, dark mode, reduced motion.
6. Rodar testes e auditoria de acessibilidade; capturar screenshot em mobile e desktop (UI web: `browser-automation`, portas/dev:68,91).
7. Entregar no Output Format, com Evidence e State Update.

## Required Standards

- Components typed with TypeScript — correct prop inference
- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- Every `<img>` with descriptive `alt`; decorative images: `alt=""`
- Touch targets minimum 44×44px on all interactive elements
- Body text minimum 16px — prevents automatic zoom on iOS
- Dark mode via CSS variables and `prefers-color-scheme`
- `prefers-reduced-motion` respected in animations
- `loading="lazy"` on images below the fold
- Never `!important` without documented justification

Componente reutilizável declara `composition contract`, props/events,
dependencies, namespace, loading/error/empty states e exemplo. UI agentic
explicita objetos de estado, relações, ações permitidas, feedback e histórico.
Performance verifica boundary de Server Components, JavaScript/hydration
necessários e URL de produção quando existir.

## Reference Stack

```
Framework:   React 19, Next.js 15, Vue 3, Astro 5
Language:    TypeScript 5.5+
Styling:     Tailwind CSS v4, CSS Modules, Radix UI
State:       Zustand, TanStack Query, Jotai
Testing:     Vitest, Testing Library, Playwright
Build:       Vite 6, Turbopack
Docs:        Storybook 8, TSDoc
Icons:       Lucide React, Phosphor Icons
```

## Output Format

```markdown
## Deliverable
[Complete TypeScript/JSX code with types, styles, and imports]

## Evidence
[Test results: X/Y passing; a11y checklist; Core Web Vitals or Lighthouse score if applicable]

## State Update
[Components created/modified, added dependencies, introduced design tokens]
```

## Políticas

- prompt-contracts — escopo fechado por packet
- subagent-orchestration — delegação com briefing mínimo
- observability — evidência e rastreabilidade no output
- token-economy — budget por fase

## Perfil de modelo

Perfil `standard` — executor com verifier determinístico (testes/a11y); `standard` resolve para `claude-opus-5-5 · medium`; `deep`/`critical` ficam para auditoria e decisão estrutural (model-routing §Padrão custo-efetivo; model-catalog §Perfis).

## Output padrão

Answer-first: decisão/veredito na 1ª linha, detalhe e evidência depois.

## Handoff humano

Para e surfaça `[DECISION NEEDED]` antes de agir em: operação destrutiva, credencial, efeito externo, claim de alta consequência sem corroboração.

## Anti-patterns

- ❌ Delivering a component without tests or without Evidence
- ❌ `<div>` where a semantic element exists
- ❌ `<img>` without `alt`
- ❌ Inline styles for logic that belongs in CSS
- ❌ `any` in TypeScript
- ❌ `!important` without a justifying comment
- ❌ Click events on non-interactive elements without `role` and `tabIndex`


---

## Fora do Escopo

> **Codenames.** Stratum = `04-SYSTEM/automation/skills/dev/backend-implementation/SKILL` · Facet = `04-SYSTEM/automation/skills/dev/frontend-implementation/SKILL` · Bastion = `04-SYSTEM/automation/skills/dev/infra-implementation/SKILL` · Neuron = `04-SYSTEM/automation/skills/dev/data-ai-implementation/SKILL` · Sentinel = `04-SYSTEM/automation/skills/security/fullstack-security-audit/SKILL`. Os agentes homonimos foram dissolvidos em skill (S1, 2026-08-23); o nome de guerra sobreviveu ao arquivo.
- APIs e backend (→ Stratum)
- Infraestrutura e deploy (→ Bastion)
- ML/AI pipelines (→ Neuron)
- Security review (→ Sentinel)

## Completion

Pronto quando os testes passam, a auditoria de acessibilidade não tem erro, e há screenshot (ou story) em mobile e desktop colado em Evidence. Componente reutilizável só está pronto com o composition contract escrito.

## Critério de sucesso
- Componente renderiza em mobile e desktop
- Acessibilidade: ARIA labels, contraste, keyboard navigation
- Sem `any` em TypeScript sem justificativa
- Evidence com screenshot ou Storybook story

## Exemplo
**Input:** "Criar componente de pricing cards responsivo"
**Output:** `PricingCard.tsx` + `PricingCard.test.tsx` + Storybook story. Evidence: screenshots mobile/desktop, ARIA audit limpo.

## Quando NÃO usar

- Implementação de API/backend → `backend-implementation` (camada server).
- Design visual/apresentação sem implementação de código → `visual-design`.

## Failure modes

- Invalid input → stop, don't invent.
- Missing resources → warning, don't create.
- Screenshot só em desktop: quebra de layout mobile passa sem ser vista.
- Estado vazio ou de erro não renderizado: o componente só foi testado no caminho feliz.
- `<div>` clicável sem `role` e `tabIndex`: inacessível por teclado, e o teste visual não pega.
- Evidence de antes da última edição.
