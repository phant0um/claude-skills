---
status: active
type: standards
kind: doc
name: marketing-system-standards
title: "Marketing System — Standards"
version: 1.0.0
updated: 2026-08-17
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W4 do plano drift-reorg-skills). Aberto: signal, anchor e prism, citados como agentes ativos, nao existem em agents/active/; so ha copias em 08-ARCHIVE (Signal e Anchor em disapproved/, Prism e Folio em approved/). Conteudo nao alterado; candidato a arquivar. Voz, paleta e criterios de qualidade nao dependem dos agentes e seguem coerentes com canvas.md; os nomes de agente dentro dele herdam o problema acima."
---

# Padrões do Marketing System

## Voz de Michel (todos os agentes)

- **Tom:** direto, técnico-acessível, profundidade real
- **Nunca:** guru motivacional, frases de calendário, linguagem corporativa
- **Sempre:** dados concretos, exemplos reais, frameworks acionáveis
- **Idioma:** português brasileiro (prompts DALL-E: inglês)

## Paleta visual padrão

| Uso | Cor |
|---|---|
| Fundo principal | `#0d0d0d` ou `#111827` |
| Acento primário | `#3b82f6` (azul elétrico) ou `#14b8a6` (teal) |
| Texto principal | `#f9fafb` |
| Texto secundário | `#9ca3af` |
| Acento alternativo | `#f97316` (laranja tech — uso pontual) |

Tipografia: system fonts com fallback (`-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`)

## Critérios de qualidade por agente

### Anchor (modos Vox/Frame absorvidos)
- Hook para scroll em <10 palavras
- Thread: progressão lógica clara (cada tweet leva ao próximo)
- Post único: funciona standalone sem contexto
- Reply: humano, 1-3 linhas, não agressivo
- Vídeo (YouTube): roteiro com gancho nos primeiros 15s, CTA único

### Prism — modos SITE e DOCUMENTO (specs `canvas` e `folio`)
- HTML completo e funcional — zero placeholders sem exemplo
- Responsivo: 375px / 768px / 1280px
- Leitura do documento <90s (one-pager) ou <5s/slide (deck)
- Newsletter: inline CSS, largura máx. 600px

### Prism (modo Lens absorvido)
- Prompts DALL-E em inglês
- Prompt sempre inclui: subject + estilo + composição + paleta + mood + ratio + qualidade
- Série: DNA visual documentado e reutilizável
- Nunca depende de texto legível na imagem

## Anti-padrões

- ❌ Agentes criando estratégia — isso fica nos agentes de estratégia externos
- ❌ Conteúdo genérico sem contexto Michel
- ❌ HTML com dependências não declaradas
- ❌ Prompts DALL-E em português
- ❌ Posts sem hook
- ❌ ~~`progress.md` desatualizado por mais de 1 sessão~~ — doc arquivado em 2026-10-11 (`08-ARCHIVE/system/2026-10-11--marketing-docs/progress.md`)
