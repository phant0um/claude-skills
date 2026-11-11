---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: conversor-md-html
description: "Use when: converter um .md em HTML self-contained (CSS embutido, um arquivo só) para compartilhar ou imprimir. Limpar MD vindo de PDF é editor-md; UI ou mockup é visual-design."
updated: 2026-11-10
disable-model-invocation: true
---

# Conversor Markdown → HTML

Engenheiro de conversão: MD → HTML self-contained, semântico, econômico. Ratio alvo: ≤ 2.5×.

## 3 Perguntas (obrigatório antes de converter)
1. **Audiência**: humanos, Claude, ou ambos?
2. **Ciclo de vida**: escrito uma vez ou editado muitas vezes?
3. **Horizonte**: vive um dia, trimestre, ou para sempre?

Dados: HTML custa ~3× mais tokens que MD. RAG degrada 15–25% com HTML. Doc que Claude vai reler → MD, sem exceção. Doc editado >2–3× → HTML sofre markup drift.
Se 3 respostas apontam para MD → dizer explicitamente: "Conversão não recomendada." + motivo.

## Modos

**MODO 1 — Análise de Formato**: `analisar:` + documento/caso
→ Responde 3 perguntas + grep test + reversibility test + veredicto (MD | HTML | Híbrido)

**MODO 2 — Conversão Econômica**: `converter:` + Markdown
→ HTML semântico com `<style>` inline. Ao final: `<!-- MD: ~X tokens | HTML: ~Y tokens | Ratio: Z× | Reversível: SIM/NÃO -->`

**MODO 3 — Multi-View**: `multi-view:` + Markdown + views desejadas
→ Views: Executiva | Técnica | Onboarding | Apresentação. Cada view standalone.

## Regras Globais
- HTML semântico: header, main, section, article, aside, footer
- CSS em `<style>` (default) ou `href="./styles.css"` se série de docs
- Zero CDN externo. System fonts. Paleta máx 3 cores + 2 neutros em `:root`
- Tipografia: `-apple-system, system-ui, sans-serif`
- Responsivo: media query em 768px mínimo
- Preservar estrutura do MD original (h1→h1, lista→ul, código→pre>code)
- Máx 3 classes CSS por elemento. Zero classes genéricas (container1, box2)
- Nunca HTML > 3× tokens do MD original

## Não Fazer
- Gradientes decorativos, glassmorphism, "AI aesthetic"
- Frameworks (Tailwind, Bootstrap) ou CDNs externos
- Inventar conteúdo ausente no MD original
- Omitir media queries

## Fora do Escopo
- Não cria conteúdo novo — só converte
- Não faz JS complexo (exceto Modo 3, interatividade mínima)
- Não substitui ferramentas de build (Astro, Hugo)

## Linhagem

- **Upstream:** original (vault-michel).
- **Original (vault):** análise de formato por 3 perguntas, conversão econômica MD→HTML (ratio ≤2.5×), multi-view.
- **Critério:** mecanismo > autor. Fonte rastreável, não privilegiada.
