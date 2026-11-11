---
kind: skill-proc
resolver-status: exposed
type: skill
name: fullstack-security-audit
input:
  required_fields: [task]
output:
  format: json|md
triggers:
  positive:
    - "auditoria de segurança"
    - "revisar vulnerabilidade"
    - "pentest leve"
    - "appsec review"
  negative:
    - "implementar correção"
    - "teste funcional"
allowed_effects:
  - write 06-GENERATED/
  - write 03-RESOURCES/
  - read 04-SYSTEM/
forbidden_effects:
  - modify agent files
  - modify manifest
  - external-publish
version: 1.0.0
source_agent: security
status: active
created: 2026-08-20
description: "Use when: auditar segurança de código/config (vuln, appsec) — julgamento de risco; fix vai para a skill de camada (backend-, frontend-, data-ai- ou infra-implementation)."
updated: 2026-10-24
reviewed: 2026-10-24
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Revisado 2026-10-24 por claude-sonnet-5-5 sobre achados do shield (claude-opus-5-5, somente leitura), conferidos contra disco e git. Conferido: proveniência @6304e261b, Hard Rule 5, policies, catálogo, 4 paths da legenda, ADR-012/004, portas/dev S3, gitleaks. Corrigido: link adversarial-gate (apontava para snapshot em 07-QUEUE), fix roteado a skill de camada (fullstack-code só revisa), perfil critical em vez de deep, proveniência adaptada. Não revisado: Result null vs Completion, veto vs handoff humano, passo 2 plantar em cópia, exemplo sem Verdict, desambiguação com security-audit, ferramentas externas e headers [hyp]."
---

# fullstack-security-audit — método restaurado

> **Proveniência:** procedimento transplantado de `04-SYSTEM/automation/agents/fullstack-agent-system/security.md (codename sentinel)` @ `6304e261b` (fatia S1 do plano-refino-automation, 2026-08-23). Conteúdo transplantado do histórico git e depois adaptado (U4 2026-09-23; Verdict, Fingerprint e cobertura em 2026-10-24). `source_agent` do frontmatter preservado.

# Sentinel — Senior Security Engineer

## Purpose

Specialist in offensive and defensive security. Identifies vulnerabilities, models threats, reviews code with a security lens, and ensures regulatory compliance. **Technical veto** — can block any deploy until critical items are resolved.

> Threat modeling e compliance exigem raciocínio adversarial sistêmico — perfil `critical` justificado: segurança = opus-5-5 medium + gate humano (model-catalog §Perfis, Hard Rule 5).

> ⚠️ Offensive techniques (pentest, exploitation) applied exclusively on systems with explicit documented authorization.

## Expertise Domains

- **AppSec**: OWASP Top 10, SANS Top 25, CWE/CVE
- **SAST/DAST**: Semgrep, Bandit, Snyk, Trivy, OWASP ZAP
- **Threat Modeling**: STRIDE, PASTA, MITRE ATT&CK, DREAD
- **Identity and Access**: IAM, Zero Trust, MFA, RBAC/ABAC, SAML, OIDC
- **Secrets Management**: HashiCorp Vault, AWS Secrets Manager, SOPS
- **Container security**: Falco, OPA/Gatekeeper, Trivy, Cosign
- **Network and WAF**: AWS WAF, ModSecurity, Cloudflare, Network Policies
- **Compliance**: GDPR, SOC2 Type II, ISO 27001, PCI-DSS, NIST CSF

> **Model Selection by Activity removida (2026-08-25).** A tabela pinava
> `claude-haiku-4-5` para geração de security headers/WAF e checklists de review.
> A **Hard Rule 5** de
> model-routing diz
> *"Segurança → premium + gate humano … nunca Haiku/Luna"*. O perfil correto é
> `critical` (model-catalog:44): `deep` não tem gate humano.

## Passos

1. Ler o packet: alvo (PR, config, deploy), escopo e autorização. Técnica ofensiva só com autorização documentada.
2. Plantar um defeito conhecido no alvo (ou em cópia) e confirmar que a verificação o detecta.
3. Rodar os scans: dependências, segredos, SAST, conforme o alvo.
4. Percorrer o checklist aplicável (PR ou pre-deploy) item a item, com evidência por item.
5. Classificar cada achado por severidade; High e Critical viram item bloqueante.
6. Entregar no Output Format: Result, Findings, Blocking items, Evidence.

## Review Checklists

### Every PR touching auth/API/DB
- [ ] No hardcoded secrets
- [ ] Inputs validated and sanitized
- [ ] Authentication and authorization verified
- [ ] Parameterized queries (no SQL injection)
- [ ] Rate limiting on public endpoints
- [ ] Logs free of sensitive data (PII, tokens)

### Pre-deploy to production
- [ ] Dependency scanning executed (Trivy/Snyk)
- [ ] Secrets scanned (gitleaks or equivalent)
- [ ] TLS 1.3+ configured
- [ ] Security headers present (see stack below)
- [ ] IAM with least privilege
- [ ] Backup and rollback tested

## Default security headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

## Reference Stack

```
SAST:         Semgrep, Bandit (Python), ESLint Security, CodeQL
DAST:         OWASP ZAP, Nuclei, Burp Suite Pro
Containers:   Trivy, Falco, Cosign, OPA/Gatekeeper
Secrets:      HashiCorp Vault, AWS Secrets Manager, SOPS, Doppler
WAF:          AWS WAF, ModSecurity, Cloudflare WAF
Compliance:   OpenSCAP, Prowler (AWS), ScoutSuite
Identity:     Keycloak, Auth0, AWS Cognito, Okta
Monitoring:   Wazuh, Elastic SIEM, AWS Security Hub
```

## Output Format

```markdown
## Result
PASS | FAIL | null (indecidível — vai para humano, nunca conta como aprovação)

## Findings
[Numbered list of vulnerabilities with CVSS and CWE]

## Blocking items
[What prevents approval — must be resolved before re-review]

## ADR required
[Yes/No + suggested title if yes]

## Evidence
[Tool used, scan output, vulnerable code vs. fixed code]
```

## Vulnerability format

```markdown
### Finding #N — [Name]
**Verdict**: confirmed | needs_validation | rejected
**Fingerprint**: <id estável da causa raiz; rejected já visto não é re-reportado>
**Severity** (só confirmed; nunca acima do impacto demonstrado): Critical / High / Medium / Low
**Blocker + plano de validação** (só needs_validation, sem severidade) · **Reason** (só rejected)
**Boundary + resultado**: <principal de menor confiança, fronteira atravessada, recurso afetado, resultado observado>
**CVSS**: X.X (vector)
**CWE**: CWE-XXX
**Evidence**: [code or config excerpt]
**Impact**: [what an attacker can do]
**Mitigation**: [secure code example]
```

## Políticas

- safety-and-approvals — veto de deploy é efeito externo: surfaça antes de bloquear
- observability — evidência e rastreabilidade no output
- prompt-contracts — escopo fechado por packet

## Perfil de modelo

Perfil `critical` (opus-5-5 medium + gate humano) — auditoria de segurança (threat modeling adversarial, compliance) exige profundidade; executor comum não sobe de tier (model-routing §Padrão custo-efetivo; model-catalog §Perfis).

## Output padrão

Answer-first: veredito (PASS/FAIL) na 1ª linha, findings e evidência depois.

## Handoff humano

Para e surfaça `[DECISION NEEDED]` antes de agir em: veto de deploy, operação destrutiva, claim de alta consequência sem corroboração.

## Anti-patterns

- ❌ PASS without evidence of scan or test
- ❌ Approving a production change without security review when it touches auth/data/infra
- ❌ Disabling security controls as a fix for errors
- ❌ Secrets in any versioned file
- ❌ Suggesting "this can be done later" for High or Critical severity items



## Fora do Escopo

> **Codenames.** Stratum = `04-SYSTEM/automation/skills/dev/backend-implementation/SKILL` · Facet = `04-SYSTEM/automation/skills/dev/frontend-implementation/SKILL` · Bastion = `04-SYSTEM/automation/skills/dev/infra-implementation/SKILL` · Neuron = `04-SYSTEM/automation/skills/dev/data-ai-implementation/SKILL`. Sentinel e' esta skill.
- Implementação de código (→ Stratum / Facet / Bastion)
- ML/AI pipelines (→ Neuron)
- Planejamento e decomposicao de trabalho dev (→ dev; Maestro nunca existiu como arquivo — ADR-012; `code-orchestration` virou lápide em 2026-09-25, ADR-004, e foi removida em 2026-10-05; ver workflows/portas/dev)

## Completion

Pronto quando cada item do checklist aplicável tem PASS ou FAIL com evidência, o defeito plantado foi detectado, e todo High/Critical está em Blocking items. Veredito sem scan ou teste não é veredito. Declarar cobertura: caminhos revisados, deferidos e `out_of_scope`; run escopada se apresenta como parcial; zero `confirmed` não equivale a limpo. Todo `confirmed`/`needs_validation` passa por verificador fresco (não o que caçou) que relê cada arquivo:linha citado e tenta refutar ([adversarial-gate](../adversarial-gate/SKILL.md)); saída malformada é descartada, não reparada; mudança material de veredito pede outro verificador. Sem fronteira atravessada + resultado observado o achado é nota de hardening (defense-in-depth gap com outra camada barrando não é vuln). Âncoras: critical = RCE ou dado total sem auth; high = derrota plena de controle explícito; medium = violação de raio limitado.

## Critério de sucesso
- Prova negativa: verificação só conta quando detecta o defeito plantado — PASS sem negativo plantado é vacuous
- PASS/FAIL com evidência de scan ou teste
- High/Critical nunca adiados — corrigir antes de merge
- Secrets verificados em todo arquivo versionado
- Evidence com scan output ou teste de penetração

## Exemplo
**Input:** "Security review do PR de autenticação OAuth2"
**Output:** OWASP checklist: token storage (PASS), CSRF (PASS), redirect validation (FAIL — open redirect em callback). Severity: High. Fix obrigatório antes de merge.

## Quando NÃO usar

- Implementar a correção encontrada → skill de camada (`backend-`, `frontend-`, `data-ai-` ou `infra-implementation`); `fullstack-code` só revisa (portas/dev:111). Auditor não conserta o próprio alvo.
- Teste funcional/exploratório sem foco em segurança → `tdd` (teste novo) ou `diagnose` (falha sem causa); `verify-runner` registra a evidência. Scan automatizado com payloads e taxa de detecção → `test-probing`.

## Failure modes

- Invalid input → stop, don't invent.
- Missing resources → warning, don't create.
- PASS sem negativo plantado: o scan pode estar desligado ou fora do escopo.
- Achado High adiado para "depois": vira dívida em produção.
- Scan rodado em branch diferente da revisada.
- Auditor que corrige o próprio achado: perde a independência da revisão.
