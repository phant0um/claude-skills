---
type: reference
status: active
kind: reference
name: governance-audit
description: "Spec do MODO ALVO = AUTORIDADE/GOVERNANÇA de [drift-review](SKILL.md). Não é skill invocável. Evaluates Intent Boundary, Policy Layer, and Audit Layer — not security (guard) or a"
version: 1.1
tags: [audit, governance, intent-boundary, policy, audit-layer, agents]
source: "agent-governance-layers-src"
updated: 2026-08-09
parent: "[drift-review](SKILL.md)"
mode: "ALVO = AUTORIDADE/GOVERNANÇA"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 10/10 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 10 secoes, 238 linhas; drift R13/R14: 1 achados resolvidos (decisoes D1-D4 A / SKILL_REF)"
reviewed-by: R15 (claude-sonnet; decisoes D1-D4 A)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Perfil de modelo](#perfil-de-modelo)
- [As 3 Camadas](#as-3-camadas)
- [Protocolo](#protocolo)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Restrições## Restrições](#restrições-restrições)
- [Relacionado](#relacionado)

> **Não é skill invocável.** MODO ALVO = AUTORIDADE/GOVERNANÇA de [drift-review](SKILL.md) — carregado por ela, não resolvido pelo router.



# Skill: Governance Audit

## Propósito

Auditar um agente contra as 3 camadas de governança: Intent Boundary (mandato + fora-de-escopo + escalação), Policy Layer (regras operacionais), Audit Layer (logging para post-mortem).

**Princípio base:** Falhas em produção raramente são por modelo ruim — são por fronteiras de autoridade indefinidas. Capability × ambiguidade = potencial de dano.

**Diferença de `guard`:** guard audita por vulnerabilidades de segurança (OWASP LLM Top 10). governance-audit audita por *fronteiras de autoridade* — se o agente sabe o que pode, o que não pode, e quando pedir ajuda.

**Diferença de `12-factor-check`:** 12-factor avalia arquitetura de confiabilidade. governance-audit avalia estrutura de controle e accountability.

---

## Condições de Ativação

Ative quando:
- Agente novo com acesso a operações destrutivas (escrita, delete, push)
- Após incidente onde agente agiu fora do escopo esperado
- `system-audit` PARTE B2 (PB2-governance-12factor) detecta agente com ops de alto risco sem governance
- Revisão de agente antes de expansão de capabilities

NÃO ative para: agentes read-only sem ops destrutivas; skills (não são agentes); análise de segurança técnica (→ guard).

---

## Perfil de modelo

Herda o perfil de [drift-review](SKILL.md). Mode spec nao declara perfil proprio:
e carregado por drift-review e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## As 3 Camadas

### Layer 1 — Intent Boundary

Documento ou seção que define:
1. **Mandato** — o que o agente está autorizado a fazer
2. **Fora-de-escopo** — o que explicitamente não faz, mesmo que tecnicamente possível
3. **Escalation triggers** — condições que exigem intervenção humana antes de prosseguir

> No vault: seção "Identidade" + "Fora do Escopo" + "Restrições" constituem o Intent Boundary.

### Layer 2 — Policy Layer

Regras operacionais concretas que implementam o Intent Boundary:
- Cada regra deve mapear para um item do Intent Boundary
- Regras sem mapeamento: provavelmente não deveriam existir
- Exemplos: "nunca escrever sem confirmação", "notificar antes de delete >10 arquivos", "máximo 2 retries"

### Layer 3 — Audit Layer

Capacidade de reconstruir a cadeia de decisão após um incidente:
- Input que levou à ação
- Tool chamada com quais argumentos
- Resultado
- Se houve desvio do comportamento esperado

---

## Protocolo

### 0. Gate Executável (pré-flight, determinístico) *(bash, 0 tokens de modelo)*

Roda antes da leitura semântica. Findings objetivos que não exigem julgamento. Se o gate falha, o veredicto já parte de NON-COMPLIANT — a fase semântica só refina.

```bash
AGENT="04-SYSTEM/automation/procedures/core/${SLUG}.md"

# G1 — alvo existe (senão: pare, não fabrique findings)
test -f "$AGENT" || { echo "GATE-FAIL G1: alvo inexistente $AGENT"; exit 1; }

# G2 — ops destrutivas declaradas em tools:?
DESTRUCTIVE=$(sed -n '/^tools:/,/^[a-z_]*:/p' "$AGENT" | grep -cE 'write_file|bash|delete|push')

# G3 — Intent Boundary presente (Identidade+Restrições OU Propósito+Regras)?
grep -qE '^##+ (Identidade|Propósito)' "$AGENT"  && L1A=1 || L1A=0
grep -qE '^##+ (Restrições|Regras|Fora do Escopo)' "$AGENT" && L1B=1 || L1B=0

# G4 — escalation trigger p/ ops destrutivas? (só exigido se G2>0)
grep -qiE 'confirma|escala|human-gated|HITL|antes de (delete|push|sobrescrever)' "$AGENT" && ESC=1 || ESC=0

# Veredicto do gate
if [ "$DESTRUCTIVE" -gt 0 ] && [ "$ESC" -eq 0 ]; then
  echo "GATE-FAIL G4: ops destrutivas ($DESTRUCTIVE) sem escalation trigger → NON-COMPLIANT automático"
fi
[ "$L1A" -eq 1 ] && [ "$L1B" -eq 1 ] || echo "GATE-FAIL G3: Intent Boundary incompleto (Identidade/Propósito=$L1A, Restrições/Regras=$L1B)"
```

Mapeamento gate → Completion: G1↔alvo, G2↔ops destrutivas, G3↔Layer 1, G4↔escalation trigger. Gate cobre os itens mecânicos; a fase semântica cobre mandato/órfãs/cobertura.

### 1. Ler Agent File

Ler `04-SYSTEM/automation/procedures/core/<slug>.md` completo. Mapear:
- Seção "Identidade" → mandato declarado
- Seção "Fora do Escopo" → boundary declarado
- Seção "Restrições" → regras operacionais
- Ferramentas (`tools:`) → capabilities reais
- Model tier → escalação de modelo como proxy de HITL

### 2. Avaliar Layer 1 — Intent Boundary

```
Mandato declarado: [sim/não/parcial]
  → Evidência: [citação da seção Identidade]
  → Gap: [o que está implícito mas não declarado]

Fora-de-escopo declarado: [sim/não/parcial]
  → Evidência: [citação]
  → Gap: [casos de borda não cobertos]

Escalation triggers: [sim/não/parcial]
  → Evidência: [citação das Restrições que exigem confirmação]
  → Gap: [ops irreversíveis sem trigger de escalação]
```

### 3. Avaliar Layer 2 — Policy Layer

Para cada regra na seção "Restrições":
```
Regra: [texto da regra]
Mapeia para Intent Boundary: [sim/não]
Cobertura: cobre [quais casos] / lacuna: [quais casos não cobre]
```

Regras sem mapeamento = "regras órfãs" → flag.

### 4. Avaliar Layer 3 — Audit Layer

Verificar se agent file define:
- Output de relatório estruturado (rastreável)
- Logging de ações em arquivo de log
- Formato que permite reconstruir o que o agente fez

### 5. Output

```
GOVERNANCE AUDIT: <slug> v<versão>

━━━ LAYER 1: INTENT BOUNDARY ━━━
Mandato:            [DECLARADO / PARCIAL / AUSENTE]
Fora-de-escopo:     [DECLARADO / PARCIAL / AUSENTE]
Escalation triggers:[DECLARADO / PARCIAL / AUSENTE]

Gaps identificados:
  - [gap específico com localização]

━━━ LAYER 2: POLICY LAYER ━━━
Regras mapeadas:    N/M
Regras órfãs:       [lista]
Cobertura gaps:     [ops sem policy]

━━━ LAYER 3: AUDIT LAYER ━━━
Output rastreável:  [SIM / NÃO]
Log estruturado:    [SIM / NÃO]

━━━ VEREDICTO ━━━
COMPLIANT | PARTIAL | NON-COMPLIANT

Ações prioritárias:
  🔴 [crítico — ops irreversível sem trigger]
  🟡 [importante — gap de cobertura]
  ⚪ [melhoria — regra órfã]

PRÓXIMO PASSO:
  NON-COMPLIANT: @extend para adicionar triggers de escalação faltantes
  PARTIAL: adicionar seções declaradas ao Intent Boundary
  COMPLIANT: revisão em 60d
```

---

## Completion

- [ ] Gate Executável (step 0) rodado: G1-G4 — findings mecânicos capturados antes da fase semântica
- [ ] Layer 1 (Intent Boundary) verificada: ## Identidade + ## Fora do Escopo + ## Restrições OU ## Propósito + ## Regras
- [ ] Ops destrutivas identificadas (write_file, bash delete/push)
- [ ] Escalation trigger presente para ops destrutivas
- [ ] Veredito: COMPLIANT / NON-COMPLIANT com理由
- [ ] NON-COMPLIANT: correção via @extend recomendada

## Failure modes

- **String literal grep**: buscar "Layer 1" / "Intent Boundary" literalmente → checar por seções equivalentes (Identidade+Restrições ou Propósito+Regras)
- **COMPLIANT sem Layer 1**: marcar COMPLIANT sem Intent Boundary → NON-COMPLIANT automático
- **Auto-fix**: governance-audit corrige em vez de diagnosticar → apenas diagnostica, correção via @extend

---

## Restrições## Restrições

- Agente com ops destrutivas (`write_file`, `bash` com delete/push) sem escalation trigger = NON-COMPLIANT automático
- NUNCA marcar COMPLIANT se Layer 1 está AUSENTE
- Governance-audit não corrige — apenas diagnostica. Correção via @extend

---

## Relacionado

- guard — segurança técnica (OWASP); governance-audit = autoridade e accountability
- [12-factor-check](12-factor-check.md) — arquitetura de confiabilidade; governance-audit = controle de autoridade
- extend — aplica as correções identificadas pelo governance-audit
- system-audit — PARTE B2 roda governance-audit nos agentes críticos (1ª segunda do mês). `vault-audit` não faz scan de agentes desde 2026-08-09.
