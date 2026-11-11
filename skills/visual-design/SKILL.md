---
kind: skill-proc
resolver-status: exposed
type: skill
name: visual-design
input:
  required_fields: [design_type]
output:
  format: html|css|svg|md
triggers:
  positive:
    - "criar UI"
    - "design system"
    - "criar apresentação visual (slides)"
    - "mockup"
    - "componente visual"
  negative:
    - "copy de marketing"
    - "implementação frontend"
allowed_effects:
  - write 06-GENERATED/
  - write 03-RESOURCES/
forbidden_effects:
  - deploy production
  - credential-use
  - modify agent files
reads: ["**"]
writes: ["06-GENERATED/**", "03-RESOURCES/**"]
version: 1.2.0
source_agent: pixel
status: active
created: 2026-08-20
description: "Use when: produzir UI/mockup/design system/apresentação como artefato visual (HTML, SVG, CSS, tokens, diagrama). Código de produção vai para frontend-implementation; foto, vídeo e visual de peça de marca para marketing-content-design; texto para content-creation."
updated: 2026-10-31
reviewed: 2026-10-25
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisao 2026-10-25: proveniencia pixel corrigida (nexus-agent-system), agents/agents. Rotas e policies conferidas. NAO conferido: design system/tokens no vault, Storybook; sobreposicao diagrama/slide com diagram-build e canvas sem desambiguar."
---

# visual-design — UI, mockup e design system como artefato

> **Proveniência:** procedimento transplantado de `04-SYSTEM/automation/agents/nexus-agent-system/pixel.md` @ `e19ed10ce` (fatia S1 do plano-refino-automation, 2026-08-23). `source_agent` do frontmatter preservado. Em 2026-09-25 saiu a linha de modelo (skill não escolhe modelo) e o corpo parou de prometer código de produção: a description e §Quando NÃO usar já mandavam código para `frontend-implementation`. Em 2026-10-31 entrou o §Piso, regras reescritas a partir do Floor de nutlope-hallmark (MIT, commit `4f6a46c6dc`); sem waiver, sem sloplint, sem temas.

## Propósito
Transforma requisitos em interfaces coerentes. Trabalha com componentes,
design tokens e padrões visuais. Nunca inventa padrões — segue o design system
ou propõe um ADR para mudá-lo.

## Ao ser invocado

1. Entender o contexto: é novo componente, refactor ou apresentação de dados?
2. Verificar design tokens e componentes existentes antes de criar novos
3. Produzir o artefato visual (mockup HTML/SVG, CSS, tokens, diagrama) com
   acessibilidade (ARIA, contraste, responsividade). Código de produção é de
   `frontend-implementation`, que recebe este artefato como spec.
4. Para apresentações: estruturar informação antes de estilizar



## Regras

- Mobile-first sempre
- Sem CSS inline em componentes de produção
- Componentes são atômicos: um propósito, uma responsabilidade
- Nomes em inglês, semânticos (não `div1`, `containerWrapper`)
- Toda mudança de design system requer ADR
- **Passes limitados (anti-slop):** build fully, inspect once, fix in one batch, stop. Revisão única do artefato antes de entregar — sem iteração infinita de refinamento visual (padrão Impeccable, ver pbakaus-impeccable)

### Piso — só em artefato HTML/CSS de página (não vale para slide, diagrama nem Mermaid)

Sem waiver: regra de piso não se dispensa. Cada item abaixo evita um defeito que o modelo repete por default.

- Cor e fonte só por token declarado em `:root`; nenhum literal de cor ou `font-family` fora do bloco de tokens.
- Nunca `transition: all`; nunca animar `width`, `height`, `top` ou `left` (força layout a cada frame; use `transform`/`opacity`).
- Todo elemento interativo tem `:focus-visible` que aparece na hora, com contraste ≥ 3:1 contra o fundo.
- Toda animação tem fallback em `@media (prefers-reduced-motion: reduce)`; o conteúdo fica visível com script desligado.
- Nunca métrica, depoimento, logo wall ou contagem de caso inventados; sem fonte, escreva `[não-verificado]` ou remova.
- Nunca formulário que mostra sucesso sem enviar request (fake send): ou liga ao endpoint real ou declara "mockup sem envio".

## Políticas

- Telemetria e evidência: observability
- Contratos de packet e escopo: prompt-contracts

## Entregáveis possíveis

- Mockup de componente em HTML/SVG, com os estados que o Storybook vai precisar
- Diagrama de UI em Mermaid/ASCII para revisão rápida
- Design tokens atualizados
- Slide deck ou relatório visual (a redação vai para `content-synthesis`; Herald foi absorvido em skill)

## Output padrão

Answer-first: resposta na 1ª linha (decisão/veredito), detalhe depois.

Componente criado: [nome + localização]  
Design tokens usados: [lista]  
Acessibilidade: [checklist resumido]  
Requer ADR: [sim/não]

## Handoff humano

Para e surfa `[DECISION NEEDED]` ao Nexus antes de agir: operação destrutiva, contradição entre design tokens e brief, claim de alta consequência sem corroboração, erro inesperado. Formato: `[DECISION NEEDED]` + motivo + alternativa proposta.

## Fora do Escopo
- Lógica de negócio em componentes (→ Forge)
- UX research ou entrevistas (→ Scout)
- Copywriting para UI (→ `content-creation`)

## Critério de Qualidade
- Componente renderiza em mobile e desktop
- ARIA labels e contraste WCAG AA verificados
- Nenhum componente duplicado no design system

## Exemplo
**Input:** executar `visual-design` — card de preço para SaaS
**Output:** `pricing-card.html` (mockup com estados default/hover/destacado) + design tokens referenciados. Acessibilidade: contraste AA, aria-label em CTAs. O `.tsx` sai de `frontend-implementation` a partir deste mockup.

## Quando NÃO usar

- Copy/texto de marketing → `content-creation`.
- Foto, vídeo, thumbnail ou identidade visual de peça de marca → `marketing-content-design`.
- Implementar a UI em código → `frontend-implementation`.

## Failure modes

- `design_type` ausente ou desconhecido → pergunte; não escolha.
- Deploy solicitado → bloqueie (`forbidden_effects`).
- Componente criado sem checar os existentes → duplicata no design system.
- Contraste abaixo de WCAG AA entregue como pronto.
- Mais de um passe de refino visual (Regras: build, inspect once, fix, stop).
- Código de produção entregue por esta skill → era de `frontend-implementation`.

## Completion

Critério de aceite:

- [ ] Output padrão preenchido: artefato com path, tokens usados, checklist de acessibilidade, "Requer ADR".
- [ ] Contraste WCAG AA conferido em cada par texto/fundo do artefato.
- [ ] Artefato renderiza em largura mobile e desktop.
- [ ] Artefato de página: Piso conferido por inspeção (tokens em `:root`, sem `transition: all`, `:focus-visible`, fallback de reduced-motion, nada inventado, sem fake send).
- [ ] Mudança de design system acompanha proposta de ADR, ou "Requer ADR: não".
