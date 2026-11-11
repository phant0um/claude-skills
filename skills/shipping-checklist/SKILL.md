---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: shipping-checklist
skill: shipping-checklist
version: 1.0
author: Nexus Agent System
source: addyosmani/agent-skills
tags: [deploy, release, shipping, verification, go-live]
updated: 2026-07-06
description: "Use when: gate final antes de deploy/release — verifica que tudo que precisa estar pronto está pronto, não apenas 'funciona na minha máquina', mas pronto para produção com usuários reais. (Não é checklist de código já escrito — para refatoração use [code-optimize](../code-optimize/SKILL.md).)"
reads: []
writes: []
triggers:
  positive:
    - "/shipping-checklist"
    - "gate final antes de deploy/release"
    - "verificar pronto para produção"
  negative:
    - "feature em dev sem intenção de release"
    - "code review isolado"

reviewed-scope: "checagem mecanica + semantica: 5/5 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 8 secoes, 145 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
# Skill: Shipping Checklist

## Propósito

Gate final antes de deploy/release. Verifica que tudo que precisa estar pronto está pronto — não apenas "funciona na minha máquina", mas pronto para produção com usuários reais.

"Ship faster is safer" — quanto maior o lote, maior o risco. Ship pequeno e frequente.

---

## Quando NÃO usar

- **Mudança trivial reversível** (typo, config local) — checklist é overhead.
- **Draft/WIP sem intenção de ship** — checklist só no ponto de entrega.
- **Deploy automático com gates próprios** (CI com pipeline completo) — CI já é o checklist; não duplicar manualmente.

Disambiguation: `shipping-checklist` verifica prontidão de entrega; `code-optimize` revisa qualidade 5E; `spec-verify` valida contra spec — checklist é a última porta, não a revisão.


## Condições de Ativação

Ative esta skill quando:
- `@ship [feature/change]` for chamado
- Antes de qualquer deploy para produção
- Antes de merge de PR com impacto em produção
- Quando o usuário disser "fazer deploy", "publicar", "release", "ir para produção"

NÃO ative para: mudanças em docs-only; testes locais; branches de experimento.

---

## Checklist (12 itens)

### Código
- [ ] **S1 — Testes passando** — suite completa verde, incluindo integration tests
- [ ] **S2 — Sem TODO/FIXME em código shipping** — grep por `TODO|FIXME|HACK|XXX` nos arquivos modificados

### Segurança
- [ ] **S3 — Secrets verificados** — zero API keys, tokens, passwords no código ou git history
- [ ] **S4 — Dependências auditadas** — `npm audit` / `pip audit` / equivalente sem vulnerabilidades high/critical

### Compatibilidade
- [ ] **S5 — Migration script testado** — se há schema change, testado em staging com dados reais
- [ ] **S6 — Rollback plan definido** — como reverter se quebrar em produção (tempo estimado + responsável)

### Observabilidade
- [ ] **S7 — Logs configurados** — novos endpoints/components têm logging com correlation ID
- [ ] **S8 — Alertas configurados** — métricas críticas têm alertas (error rate, latency, uptime)

### Documentação
- [ ] **S9 — Changelog atualizado** — entrada descrevendo o que mudou, por quê, impacto para usuários
- [ ] **S10 — ADR registrado** — se decisão arquitetural foi tomada, ADR em `/decisions` (ver [decisions](../decisions/SKILL.md))

### Comunicação
- [ ] **S11 — Usuários/stakeholders notificados** — se mudança breaking ou visível, comunicado com antecedência
- [ ] **S12 — Window de deploy escolhido** — horário de baixo tráfego, evitar finais de semana/horários críticos

---

## Protocolo

### ETAPA 1 — Coletar contexto
```
O que está sendo shipped: [feature/fix/refactor]
Impacto: [breaking / non-breaking / internal]
Ambiente alvo: [staging / production]
Reversível sem dados: [sim / não]
```

### ETAPA 2 — Executar checklist
Rodar todos os 12 itens. Marcar ✅ / ❌ / N/A.

### ETAPA 3 — Veredito
```
SHIP GATE — [título]

Itens passando: [N/12]
Itens falhando: [lista com motivo]
Itens N/A: [lista]

Veredito: [SHIP / HOLD / BLOCK]
```

- **SHIP** — 0 itens falhando, todos os aplicáveis passando
- **HOLD** — 1-2 itens falhando não-críticos (S9, S11) → corrigir antes ou ship com nota
- **BLOCK** — qualquer item crítico falhando (S1, S3, S5, S6) → não shipar

### ETAPA 4 — Se SHIP
1. Executar deploy
2. Verificar health check pós-deploy (endpoint /health, smoke test)
3. Monitorar logs por 15 minutos
4. Se anomalia: executar rollback plan (S6)

---

## Completion

- [ ] Todos os 12 itens verificados (✅ / ❌ / N/A)
- [ ] Veredito explícito (SHIP / HOLD / BLOCK)
- [ ] Se BLOCK: motivo específico + ação para desbloquear
- [ ] Se SHIP: health check pós-deploy executado

## Failure modes

- **Checklist rubber-stamp**: marcar tudo ✅ sem verificar de fato → cada item precisa de evidência
- **SKIP em "é só um fix pequeno"**: fix pequeno quebra produção igual → sempre rodar, itens N/A são aceitáveis
- **Rollback plan vago**: "reverter o merge" não é rollback plan → precisa de passo-a-passo + tempo estimado
- **Deploy sem smoke test**: shipar e não verificar → sempre executar health check pós-deploy

---

## Referências

- review — review antes do ship gate
- [decisions](../decisions/SKILL.md) — ADR para decisões arquiteturais
- [fullstack-security-audit](../fullstack-security-audit/SKILL.md) — audit de segurança