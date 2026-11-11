---
type: reference
status: active
kind: reference
name: check-resolvable
description: "Spec do MODO ALVO = RESOLVER de [drift-review](SKILL.md). Não é skill invocável."
version: 1.3
author: Nexus Agent System
schedule: semanal (sexta-feira, pós-review)
scheduler_task: revisao-semanal
tags: [audit, resolver, drift, maintenance, governance]
updated: 2026-09-24
parent: "[drift-review](SKILL.md)"
mode: "ALVO = RESOLVER"
consolidated-by: R3
reviewed-scope: "checagem mecanica + semantica: 5/5 wikilinks resolvem; 5/5 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 11 secoes, 192 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Propósito](#propósito)
- [Condições de Ativação](#condições-de-ativação)
- [Quando NÃO Usar](#quando-não-usar)
- [Perfil de modelo](#perfil-de-modelo)
- [Protocolo de Execução](#protocolo-de-execução)
- [Restrições](#restrições)
- [Rename Guard (Quick-Check Mode)](#rename-guard-quick-check-mode)
- [Completion](#completion)
- [Failure modes](#failure-modes)
- [Pitfalls](#pitfalls)

> **Não é skill invocável.** MODO ALVO = RESOLVER de [drift-review](SKILL.md) — carregado por ela, não resolvido pelo router.



# Skill: Check Resolvable

## Propósito
Auditar se todos os agentes existentes no filesystem estão no roster canônico (`agent-registry.md`) e as skills em `moc-skills.md`, acessíveis por trigger. Detecta: agentes fantasmas (existem mas não são roteáveis), dead links (registrados mas não existem), triggers obsoletos.

> **Fonte do roster = `agent-registry`** (model/trigger/função). Roteamento (trigger→agente) = `AGENTS.md §Regras de Roteamento`. Skills = `moc-skills.md`. AGENTS.md não é mais parseado como inventário — é firmware+ponteiro (mudança 2026-07-02).

---

## Condições de Ativação
Ative esta skill quando:
- Semanalmente (sexta-feira, após drift-review)
- Após instalação de novo agente ou skill
- Após remoção/reorganização de `04-SYSTEM/automation/agents/`
- **Após qualquer rename de arquivo/diretório no vault** (quick-check mode — ver § Rename Guard)
- Usuário solicitar `@check-resolvable` ou "auditoria de resolver"

## Quando NÃO Usar
- Para verificar funcionalidade de agentes (use `@verify`)
- Para auditar segurança de agentes (use `@guard`)
- Após criar 1 agente já registrado em AGENTS.md — check-resolvable é para drift, não confirmação imediata
- Se AGENTS.md acabou de ser reescrito integralmente (diff será ruidoso)

---

## Perfil de modelo

Herda o perfil de [drift-review](SKILL.md). Mode spec nao declara perfil proprio:
e carregado por drift-review e roteia junto com ela — perfil local aqui
seria uma segunda fonte de verdade para a mesma execucao.

Resolucao canonica em model-routing.

## Protocolo de Execução

### PASSO 1 — Scan determinístico *(scripts, 0 tokens)*

Saída vai para `$TMPDIR` (ou o scratchpad da sessão), nunca `/tmp` fixo nem o vault.

```bash
# Agentes: agents/active/*.md vs runtime/agent-contracts.json, nos dois sentidos,
# mais instalação em ~/.claude/agents/ (AGENT_UNREGISTERED, AGENT_FILE_MISSING,
# AGENT_NOT_INSTALLED, AGENT_INSTALL_DIVERGES). Conferir `scanned.agents` antes de aceitar 0.
python3 04-SYSTEM/scripts/drift-structural.py > "$TMPDIR/drift-structural.json"

# Registry de agentes/skills/procedures: exit != 0 = registry defasado frente ao filesystem.
R=04-SYSTEM/automation/registry
python3 04-SYSTEM/scripts/build-agent-skill-registry.py --root . --scope-file $R/registry-scope.txt \
  --json-output $R/agent-registry.json --markdown-output $R/agent-registry.md \
  --procedures-json-output $R/procedures.json --check

# Links: wikilinks com path que não resolvem, já descontados os redirects governados.
python3 04-SYSTEM/scripts/check-links.py
```

### PASSO 2 — Fontes canônicas
- Agentes: `04-SYSTEM/automation/agents/nexus-system/runtime/agent-contracts.json` (`agents`) — é o que PASSO 1 compara com `agents/active/`.
- Roster roteável (model/trigger/função): `04-SYSTEM/automation/registry/agent-registry.md`, gerado pelo builder; nunca editar à mão.
- Skills: `04-SYSTEM/automation/agents/_index/moc-skills.md` + árvore `04-SYSTEM/automation/skills/`.
- Redirects e suppressions de link: `04-SYSTEM/system/governance/link-redirects.json`. Suppression é alvo inexistente real com owner; continua contando como quebrado no checker e deve bater 1:1 com o resto de PASSO 1.

### PASSO 3 — Diff

| Check | Condição de falha |
|-------|-------------------|
| **Agente fantasma** | Existe em `agents/active/`, não consta em `agent-contracts.json` (`AGENT_UNREGISTERED`) |
| **Dead link** | Consta em `agent-contracts.json`, não existe em `agents/active/` (`AGENT_FILE_MISSING`); ou wikilink quebrado sem redirect nem suppression |
| **Skill não registrada** | Existe em `04-SYSTEM/automation/skills/`, não consta em `moc-skills.md` nem no registry |
| **Skill usage orphan** | Registrada em `moc-skills.md` mas 0 referências em agentes/rotinas/wiki (ninguém invoca) |
| **Trigger órfão** | Trigger em "Regras de Roteamento" aponta para agente inexistente |
| **Sistema sem roteamento** | Pasta de sistema em `agents/` sem nenhuma entrada em "Regras de Roteamento" |

### PASSO 4 — Relatório

```
=== CHECK-RESOLVABLE REPORT | <timestamp> ===

FILESYSTEM:
  Agentes encontrados: N
  Skills encontradas: M

RESOLVER (agent-contracts.json + registry + moc-skills.md):
  Agentes registrados: X
  Skills registradas: Y
  Rotas definidas: Z

FINDINGS:
  🔴 Agentes fantasma (existem, não roteáveis): [lista]
  🔴 Dead links (registrados, não existem): [lista]
  🟡 Skills não registradas: [lista]
  🟡 Triggers órfãos: [lista]
  ⚪ Sistemas sem roteamento: [lista]

AÇÃO SUGERIDA:
  [para cada finding: fix específico]
```

---

## Restrições
- NUNCA modificar agent-registry.md / AGENTS.md automaticamente — apenas reportar
- Agentes ativos ficam em `04-SYSTEM/automation/agents/agents/`; sistemas de chat ficam em `04-SYSTEM/automation/chat-systems/` e não entram neste roster
- Rodar depois de drift-review (drift-review audita docs vs código; check-resolvable audita resolver vs filesystem)

---

## Rename Guard (Quick-Check Mode)

**Quando rodar:** Ao final de qualquer sessão que envolveu rename de arquivos/diretórios no vault. Não esperar o pipeline-diario ou a auditoria semanal — drift de wikilinks é mais barato de fixar na hora que dias depois.

### Protocolo Quick-Check

1. **Identificar renames da sessão** — listar arquivos/dirs renomeados
2. **Buscar wikilinks quebrados** — para cada rename, buscar `old-path` em todo o vault
3. **Reportar** — lista de arquivos com wikilinks apontando para o path antigo
4. **Fix ou reportar** — se poucos (<10), patchear; se muitos, logar em `04-SYSTEM/system/logs/errors.md` para batch fix

### Comando rápido

```bash
# Para cada arquivo renomeado de old-name para new-name:
grep -r "old-name" --include="*.md" . | grep "\[\["
```

### Critério de conclusão

- [ ] Zero wikilinks apontando para paths renomeados nesta sessão
- [ ] Ou: wikilinks quebrados logados em errors.md com contagem

---

## Completion

- [ ] Wikilinks path-style verificados (path existe no filesystem)
- [ ] Bare-name wikilinks resolvidos por filename lookup (single-match = inbound)
- [ ] Code blocks filtrados (não são refs reais)
- [ ] Dead-refs reais vs ambíguos distinguidos
- [ ] Zero wikilinks apontando para paths renomeados OU quebrados logados em errors.md

## Failure modes

- **Code block false positive**: ref-graph walk gera DEAD-REFs de code blocks → filtrar antes de reportar
- **Bare-name inflation**: scanner só conta path-style → bare names também são inbound válido
- **Skill v1 vs v2 não integrada**: skill com -v2 nunca integrada ao pipeline → flag como orphan de integração

---

## Pitfalls

1. **Ref-graph walk false positives de code blocks:** A função `refs_of()` que extrai paths de backtick-delimited code blocks (ex: `02-AREAS/fiap/fase-1/CONTENT\.md`) gera DEAD-REFs que não existem — são placeholders/exemplos em documentação, não refs reais. Antes de reportar dead-refs de um ref-graph walk, filtrar code blocks ou verificar se o path contém caracteres de escape (`\.`), placeholders (`YYYY`, `NN`, `$file`, `...`), ou segments de exemplo (`path/to`). Achado 2026-06-22: 375 arquivos no fecho CLAUDE.md prof.2, ~40 DEAD-REFs reportados, 0 reais após filtragem.

2. **Bare-name wikilinks resolvem no Obsidian:** Um wikilink `ai-agents` sem path resolve no Obsidian por fuzzy match de filename — mas um scanner que só conta path-style links (`file`) como inbound vai superestimar orphans. Para orphan scanning acurado, resolver bare names por filename lookup (single-match = inbound; multi-match = ambiguous = skip).

3. **Skill usage orphan vs skill não registrada:** Uma skill pode estar registrada em AGENTS.md (passa no diff filesystem↔resolver) mas ainda assim ser órfã de uso — nenhum agente, rotina, ou wiki a referencia. Achado 2026-06-24: `adversarial-gate-v2` registrada em 0 locais canônicos, única menção em relatório gerado. **Fix:** após o diff PASSO 3, rodar um passo extra de usage audit — para cada skill, grep por referências (wikilink, backtick, skill:name, @trigger) em `agents/`, `04-SYSTEM/automation/workflows/`, `wiki/`, `AGENTS.md`. Skills com 0 refs = usage orphans. Falsos positivos comuns: skills de nome genérico (`brief`, `trace`, `probe`, `council`) — palavra aparece como substantivo comum, não como referência à skill. Para essas, confirmar com pattern estrutural: `...skill-name`, `skill:name`, `skills/<path>/name`.

4. **Skill v1 vs v2 — versão não integrada:** Quando uma skill tem versões (v1, v2), a versão nova pode ser criada mas nunca integrada ao pipeline/rotina que a originou. Achado 2026-06-24: `adversarial-gate-v2` foi criada como evolução de v1 para batches de ingest >20, mas nunca foi referenciada na rotina `pipeline-semanal.md` nem no moc-skills. **Fix:** ao detectar skill com sufixo `-v2` (ou `-vN`), verificar se a versão anterior está ativa em rotinas/agentes. Se sim, confirmar que a nova versão também está integrada — ou flag como orphan de integração. **Resolved 2026-06-24:** `adversarial-gate-v2` integrada em `pipeline-semanal.md` v5.2 (F2.10 Batch Quality Gate), `AGENTS.md` v1.5, e `moc-skills.md`. v1 mantida para gate in-flight; v2 roda como gate pós-batch.
