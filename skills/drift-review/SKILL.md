---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: drift-review
description: "Use when auditing docs vs code/config inconsistencies, before releases, after >500-line refactors, or weekly on Fridays. Scans for broken references, stale config, orphan agents — auto-fixes mechanical drift, flags semantic drift for human decision. shipping-checklist covers deploy readiness, not docs-vs-code consistency, so the pre-release drift audit is here; semantic drift with no human owner to decide it is out of scope."
skill: drift-review
version: 1.2
author: Nexus Agent System
tags: [review, drift, sync, docs, config, maintenance]
updated: 2026-09-24
consolidated-by: R3 (absorveu check-resolvable, score-drift, governance-audit, 12-factor-check como modos)
reads:
  - 04-SYSTEM/automation/agents/
  - 03-RESOURCES/wiki-index.md
writes: []
triggers:
  positive:
    - "auditar docs vs code/config"
    - "antes de release"
    - "após refactor >500 linhas"
    - "semanal sexta"
  negative:
    - "drift semântico sem dono humano"
    - "código recém-escrito sem baseline"

reviewed-scope: "checagem mecanica + semantica: 6/6 wikilinks resolvem; 2/2 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 13 secoes, 217 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
# Skill: Drift Review

## Propósito
Varrer o repositório em busca de inconsistências entre documentação, código e configuração — e corrigir mecanicamente o que for automático, sinalizando o que requer intervenção humana.

---

## Quando NÃO usar

- **Repo pequeno sem docs/config** — sem superfície de drift, não há o que auditar.
- **Mudança ativa em curso** (sessão editando os alvos) — drift-review em estado mutável dá falso-positivo; rodar em ponto estável.
- **Auditoria de segurança** — drift é consistência docs-código; segurança é `security/security-audit` (`security-review` não existe).

Disambiguation: `contradiction-sweep` varre claims contraditórios entre fontes — drift é sintaxe de consistência, sweep é semântica. Já `governance-audit` (autoridade/conformidade), `check-resolvable`, `score-drift` e `12-factor-check` **não são skills irmãs**: são ALVOs desta skill, selecionados no PASSO 0.


## Condições de Ativação
Ative esta skill quando:
- `@review` for chamado manualmente
- Antes de qualquer release ou deploy
- Após refatoração significativa (>500 linhas modificadas)
- Semanalmente (cron recomendado: toda sexta-feira)

NÃO ative durante: implementação ativa de feature (timing errado); emergências.

---

## Perfil de modelo

Perfil `deep` — o PASSO 2 é detecção de contradição, linha explícita do perfil
(model-routing §Padrão custo-efetivo;
model-catalog §Perfis).

Os PASSOS 1, 3 e 4 são `deterministic` — varredura de path, auto-fix mecânico e
geração de lista saem de bash/python, não de modelo. Esta skill não mantém pins
locais por etapa.

---

## Protocolo de Execução

### PASSO 0 — Selecionar ALVO (obrigatório antes do PASSO 1)

Leia o pedido e escolha **exatamente um** ALVO. Se o ALVO for diferente de
DOCS-VS-CÓDIGO, carregue o spec do modo em §Modos absorvidos e execute-o com
esta skill como base — não siga para o PASSO 1.

| Pedido menciona | ALVO | Ação |
|---|---|---|
| docs desatualizados, config obsoleta, referência quebrada, release, pós-refatoração, cron de sexta | **DOCS-VS-CÓDIGO** (default) | seguir PASSO 1 abaixo |
| link/wikilink quebrado, path que não resolve, dead-ref, capitalização, archive | **RESOLVER** | carregar `check-resolvable` |
| agente saiu do papel, identidade de agente, gates D1–D5, score de drift de agente | **IDENTIDADE/SCORE** | carregar `score-drift` |
| autoridade, conformidade de norma, policy layer, audit layer, intent boundary | **AUTORIDADE/GOVERNANÇA** | carregar `governance-audit` |
| confiabilidade de agente, produção, 12-factor | **12-FACTOR** | carregar `12-factor-check` |

Ambíguo entre dois ALVOs → rodar o default e citar no relatório qual outro ALVO
ficou de fora. Nunca rodar dois no mesmo passe.

### PASSO 1 — Varredura Estrutural `[script]`

```bash
python3 04-SYSTEM/scripts/drift-structural.py > "$TMPDIR/drift-structural.json"
```

Saída JSON: `counts`, `scanned` (denominadores: docs, scripts, agentes; conferir
antes de aceitar "0 findings") e `findings` (`code`, `path`, `detail`). Exit 1 =
há finding. Checagens:

| Código | O que pega |
|---|---|
| `AGENT_UNREGISTERED` / `AGENT_FILE_MISSING` | `agents/active/*.md` vs `runtime/agent-contracts.json`, nos dois sentidos |
| `AGENT_NOT_INSTALLED` / `AGENT_INSTALL_DIVERGES` | agente ativo sem `~/.claude/agents/<nome>.md` apontando para ele |
| `PATH_MISSING` | path em code span (`.py/.sh/.md/.json`) em agents/skills/workflows que não existe em lugar nenhum; wikilink fica com `check-links.py`. Histórico não conta: proveniência `x` @ `<sha>`, linha de changelog, `reviewed-scope:` e linha com `<!-- drift:ok: motivo -->` (caminho de outro projeto, exemplo, incidente passado) |
| `VENDOR_MISSING` / `VENDOR_MODIFIED` | arquivo listado num `UPSTREAM.json` sumiu ou não bate mais com o blob SHA da tag; vendorizado intacto fica isento de `PATH_MISSING` e do gate de frontmatter |
| `SCRIPT_NO_DOCSTRING` | `04-SYSTEM/scripts/*.py` sem docstring, `*.sh` sem comentário de cabeçalho |
| `NO-UPDATED` / `STALE` | `updated:` ausente, inválido ou mais velho que `--stale-days` (90). Nunca mtime: reseta em checkout/sync |

Env vars: não se aplica ao vault (sem `example.env`; as env vars dos scripts são
chaves internas de teste e hook). Fica com o modelo só o que exige leitura: se
o script **faz** o que a docstring diz vai para o PASSO 2.

### PASSO 2 — Detecção de Drift Semântico
Para cada agente, compare:
- Corpo de `agents/active/<slug>.md` (a instrução do agente) vs. descrição em
  `AGENTS.md` — divergem?
- Exemplo de uso na documentação vs. comportamento atual (baseado em evals recentes)?
- Skills referenciadas vs. skills existentes em `skills/`?

### PASSO 3 — Auto-Fix
Corrija automaticamente (sem perguntar):
- Arquivo renomeado mas não atualizado nas referências → atualiza referências
- Entrada faltando em `example.env` → adiciona com placeholder
- Agente faltando no diagrama de arquitetura → adiciona entrada
- Path quebrado em `.md` → marca como `[LINK QUEBRADO - <caminho-esperado>]`

### PASSO 4 — Relatório de Drift Não-Automático
Para cada item que requer decisão humana:
```markdown
## [DRIFT] <descrição curta>
**Arquivo**: <path>
**Problema**: <o que diverge>
**Impacto**: ALTO | MÉDIO | BAIXO
**Ação recomendada**: <próximo passo sugerido>
```

---

## Artefatos de Saída
- Correções inline nos arquivos afetados
- `DRIFT-REPORT-<timestamp>.md` — lista de itens pendentes de decisão humana

## Vocabulário de findings: specification-drift D1–D16

Cada finding do PASSO 4 recebe **exatamente um** label D. Taxonomia (fonte: PromptKit; distinta dos D1–D5 de score-drift, que são gates de identidade de agente):

- **D1** UNTRACED_REQUIREMENT — requisito existe mas nenhum doc de design referencia
- **D2** UNTESTED_REQUIREMENT — requisito sem caso de teste no plano de validação
- **D3** ORPHANED_DESIGN_DECISION — decisão de design sem requisito de origem (scope creep ou requisito faltando)
- **D4** ORPHANED_TEST_CASE — teste sem requisito mapeado (esforço fora de cobertura)
- **D5** ASSUMPTION_DRIFT — premissa contradita ou ausente entre documentos
- **D6** CONSTRAINT_VIOLATION — design viola restrição declarada do requisito
- **D7** ACCEPTANCE_CRITERIA_MISMATCH — teste não verifica os critérios de aceitação (cobertura ilusória; pior que D2)
- **D8** UNIMPLEMENTED_REQUIREMENT — requisito especificado sem implementação no código
- **D9** UNDOCUMENTED_BEHAVIOR — código implementa comportamento fora da spec (scope creep em código)
- **D10** CONSTRAINT_VIOLATION_IN_CODE — código viola restrição declarada (defeito concreto, não gap de planejamento)
- **D11** UNIMPLEMENTED_TEST_CASE — teste planejado sem implementação na suíte
- **D12** UNTESTED_ACCEPTANCE_CRITERION — teste implementado não assere critério(s) do requisito
- **D13** ASSERTION_MISMATCH — asserções do teste divergem do comportamento esperado no plano
- **D14** UNSPECIFIED_INTEGRATION_FLOW — fluxo de integração sem spec no componente envolvido
- **D15** INTERFACE_CONTRACT_MISMATCH — componentes descrevem a mesma interface de forma incompatível
- **D16** UNTESTED_INTEGRATION_PATH — fluxo/contrato de integração sem teste end-to-end

Exemplo de uso em finding:
```markdown
[DRIFT: D7_ACCEPTANCE_CRITERIA_MISMATCH]
Arquivo: <path>
Problema: TC-014 mapeia REQ-SEC-003 mas testa só happy-path; critério de erro 403 não é verificado
Impacto: ALTO (cobertura ilusória)
Ação recomendada: corrigir asserções do teste ou reescrever o critério
```

---

## Completion

- [ ] PASSO 1 varredura estrutural completa (paths, agents, env vars, staleness por frontmatter)
- [ ] PASSO 2 drift semântico comparado (corpo do agente vs AGENTS.md, skills refs vs skills/)
- [ ] PASSO 3 auto-fix aplicado apenas em drift mecânico (refs, paths, diagramas)
- [ ] PASSO 4 relatório de drift não-automático gerado com Impacto + Ação recomendada
- [ ] Staleness medido por `updated:` frontmatter, não mtime

## Failure modes

- **mtime como staleness**: mtime reseta em git checkout e mascara stale → sempre usar `updated:` do frontmatter
- **Orphan inflation**: scanner só conta path-style wikilinks, ignora bare-name → resolver bare names por filename lookup antes de reportar orphan count
- **Auto-fix em lógica**: drift review edita o corpo do agente em vez de só estrutura → apenas structure/config é auto-fix, lógica é human-gated

---

## Restrições
- NUNCA auto-fix em lógica de agente (corpo do `.md`) — apenas estrutura/config
- NUNCA delete arquivos durante o drift review — apenas sinaliza
- Se >20 items de drift forem encontrados: alerte antes de auto-fix (pode indicar problema maior)

## Pitfalls

1. **mtime menta para staleness:** `stat -f %m` (mtime) reseta em git checkout/sync e mostra arquivos stale como fresh. Sempre medir staleness por frontmatter `updated:` campo. Achado 2026-06-20: 6 governance files com `updated:` >30d apareciam fresh por mtime.

2. **Agent files são `.md` não `.py`:** Em vault-michel, agentes são markdown em `04-SYSTEM/automation/agents/`, não Python. Adaptar paths do PASSO 1 conforme projeto. Filtrar templates/READMEs/project-setup/docs — não são agentes reais.

3. **Ref-graph walk para fecho transitivo:** Para cobertura dinâmica de drift em docs estruturais, não depender só de lista hardcoded. Walk CLAUDE.md → refs → refs-das-refs (prof. 2) descobre referências novas automaticamente. Dead-refs do walk → rodar `check-resolvable` antes de reportar (distingue quebrado real de capitalização/archive).

4. **Orphan scan precisa bare-name resolution:** Scanner que só conta path-style wikilinks (`file`) como inbound superestima orphans — bare-name links (`filename`) também são inbound válido no Obsidian. Resolver bare names por filename lookup (single-match = inbound). Sem isso, orphan count inflaciona (ex: 67 reportados vs 64 reais, 2026-06-22).

5. **Wiki-index como remediação de orphans:** Quando orphan concepts forem altos (>50), adicionar path-style wikilinks de `03-RESOURCES/wiki-index.md` para os concepts centrais é a forma mais eficiente de reduzir orphans num único arquivo — 16 links adicionados reduziram 64→48 (25%) em 2026-06-22. Priorizar concepts de agent-systems e learning-cognition (centrais ao vault) sobre dev-foundations FIAP (folhas legítimas).


## Modos absorvidos (R3)

`kind: reference` — carregue o spec do modo pedido e execute-o com esta skill como base.

- **MODO ALVO = RESOLVER** — [check-resolvable](check-resolvable.md)
- **MODO ALVO = IDENTIDADE/SCORE** — [score-drift](score-drift.md)
- **MODO ALVO = AUTORIDADE/GOVERNANÇA** — [governance-audit](governance-audit.md)
- **MODO ALVO = 12-FACTOR** — [12-factor-check](12-factor-check.md)
