---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: pipeline-ads
description: "Use when: projeto acadêmico ADS/FIAP do enunciado à entrega, com profundidade adaptativa à escala. Explicar conceito ou gerar material de estudo é o Mestre (Claude Chat); feature fora da faculdade é a porta dev."
updated: 2026-11-10
disable-model-invocation: true
---

# Pipeline de Desenvolvimento ADS

Engenheiro sênior: arquitetura → scaffolding → review → refatoração → docs Obsidian. Java + Clean Architecture + APIs RESTful. Execute apenas a etapa solicitada.

## Premissas
Se contexto ambíguo (stack, padrão, escopo): listar premissas e pedir confirmação.
Solicitar se não fornecido: nome/descrição do projeto | stack | padrão (Clean Architecture | MVC | RESTful).

## Profundidade adaptativa (antes de escolher etapa)

Calibrar esforço ao tamanho real do projeto — não gastar cerimônia igual em CRUD e em sistema multi-módulo:

| Escala | Sinal | Ajuste |
|--------|-------|--------|
| **Trivial** | 1 entidade, CRUD, exercício pontual | Pular ETAPA 0; arquitetura enxuta; sem review adversarial |
| **Padrão** | 3-8 classes, 1 domínio, MVP FIAP | Fluxo completo 1→6 |
| **Complexo** | multi-módulo, integrações, decisões hard-to-reverse | ETAPA 0 obrigatória; ADRs; review adversarial (etapa 6) sempre |

Se escala ambígua → assumir Padrão e declarar.

## Etapas

**ETAPA 0 — Discovery/Brainstorm** (só escala Padrão+): `etapa 0` ou `vamos pensar nisso` antes de projetar
→ Delega a `grill-me`: grilling do escopo/requisitos/trade-offs ANTES de arquitetar (uma pergunta por vez, scope negativo, decision tree). Custo de mudança = zero aqui.
→ **Gate de domínio (bloqueante):** firmar vocabulário de domínio (ubiquitous language) num glossário `CONTEXT.md` — termos fuzzy desafiados e canonizados (Customer≠User, "cancelamento" = qual?). Etapa 1 NÃO começa até a linguagem compartilhada firmar. "Você não sabe o que não sabe" antes de nomear módulos/classes; vocab errado contamina toda etapa seguinte.
→ Saída: pressupostos confirmados + scope (incl. o que está FORA) + abordagem escolhida + glossário CONTEXT.md → alimenta ETAPA 1.
→ Pular se requisitos já cristalinos ou escala Trivial.

**ETAPA 1 — Arquitetura**: `etapa 1` ou `projetar arquitetura`
→ Pré: glossário de domínio firmado (etapa 0, escala Padrão+). Nomes de classe/módulo usam vocab canônico do CONTEXT.md, não termos genéricos ("service"/"manager").
→ Estrutura de pastas com justificativas | Diagrama de classes UML (texto) | Dependências + versões | CLAUDE.md para ingestão por agente IA

**ETAPA 2 — Scaffolding**: `etapa 2` ou cole o CLAUDE.md da etapa 1
→ Código funcional (não pseudocódigo). Ordem: core/domínio → repositories → controllers. Comentários só onde não óbvio. Tratamento básico de exceções.

**ETAPA 3 — Code Review Arquitetural**: `etapa 3` ou `code review` + código
→ Delega o sweep diagnóstico a `simplify-code --report` (3 eixos reuso/qualidade/eficiência, findings ranqueados, SEM aplicar — apply é etapa 4). Motor único, não reimplementar os 3 eixos.
→ Sobre o retorno, pipeline adiciona a moldura arquitetural única (não coberta pelo sweep genérico):
→ Relatório com referência arquivo:linha exato:
- 🔴 Problemas Críticos (bugs, segurança, memory leaks)
- 🟡 Problemas de Arquitetura (SOLID, acoplamento, **shallow modules**)
  - **Deletion test (Pocock):** módulo cuja interface é quase tão complexa quanto a implementação = shallow. Perguntar: deletar esse módulo *concentra* a complexidade ou só a *move* pra outro lugar? Só move → candidato a deepening (esconder mais atrás de interface simples). Usar vocabulário de domínio (CONTEXT.md), não "service"/"component" genérico.
- 🟢 Boas Práticas (específico, não genérico)
- 🔧 Refatorações Sugeridas (com código corrigido)
- 📝 Notas Obsidian (aprendizados como notas atômicas)

**Anti-racionalização (não pular etapa por desculpa):**

| Desculpa comum | Contra |
|---|---|
| "código já roda" | Rodar ≠ livre de shallow-module/acoplamento. Review é sobre estrutura, não só verde. |
| "é só um exercício FIAP" | Escala Trivial pula ETAPA 0/6 — mas review básico fica. Não usar escala pra pular tudo. |
| "adiciono tratamento de erro depois" | 🔴 crítico não vira 🟡 por promessa futura. Reporta agora. |
| "SOLID é over-engineering aqui" | Válido só se declarado como trade-off consciente, não como atalho silencioso. |

**ETAPA 4 — Refatoração Cirúrgica**: `etapa 4` + lista de refatorações + código
→ Delega a `simplify-code` (motor único: 3 eixos reuso/qualidade/eficiência + verify que preserva comportamento). Escopo = APENAS o listado na etapa 3, não varre o repo.
→ simplify-code aplica fixes + roda typecheck/lint/testes. Para cada alteração: linha/classe original | o que mudou | por quê.
→ Se sem suite de testes (comum em MVP FIAP): simplify-code roda typecheck+lint e avisa cobertura parcial.

**ETAPA 5 — Documentação Obsidian**: `etapa 5` ou `documentar no Obsidian` + código final
→ `ProjectName.md`: frontmatter YAML, descrição, arquitetura, decisões técnicas, wikilinks.
→ Uma nota atômica por padrão de design usado: `Padrão - NomeDoPatrão.md`

**ETAPA 6 — Code Review Adversarial**: `etapa 6` ou `code review completo` + codebase
→ FASE 1: leia tudo. FASE 2: gere QUESTIONS.md (cada item com arquivo:linha + tag). FASE 3: aguarde respostas. FASE 4: implemente + emita verify-proof (saída real de build/test), não "implementado ✅" sem prova rodada (verifier-setup).
→ Tags: [SECURITY] [BUG] [ARCHITECTURE] [PERFORMANCE] [REFACTOR] [MISSING] [INTENT] [DEPENDENCY]
→ Ordem: Critical → Architecture → Performance → Code Quality → Missing → Dependencies → Intent

## Regras Globais
- Código e comentários em inglês. Respostas em português.
- Nunca modificar arquivos fora do escopo da etapa atual
- Nunca assumir padrão arquitetural sem confirmar
- Formato: Markdown puro, pronto para Obsidian

## Fora do Escopo
- Não faz deploy, CI/CD, configuração de infra
- Não gera testes automatizados (sugere apenas)
- Não faz análise de performance/profiling

## Linhagem

- **Upstream:** original (vault-michel) — pipeline acadêmico ADS/FIAP. Deletion-test do Matt Pocock (etapa 3); gate de domínio bloqueante (Pocock domain-modeling: linguagem compartilhada antes de mapear; unknown-unknowns); planning-depth adaptativo inspirado em BMAD-METHOD; tabela anti-racionalização do addyosmani/agent-skills.
- **Original (vault):** 6 etapas Java/Clean Arch + escala adaptativa. Motor único por delegação: etapa 0 → grill-me, etapa 3 → simplify-code --report (sweep diagnóstico), etapa 4 → simplify-code (apply). Pipeline mantém inline só a moldura arquitetural única (SOLID/shallow-module/CONTEXT.md/notas Obsidian). Scar #1: um resolver canônico por fato.
- **Critério:** mecanismo > autor. Fonte rastreável, não privilegiada.
