---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: skillify
description: "Use when: formalizar WORKFLOW MANUAL repetido (3+ sessões, ou user diz 'skillify') em skill registrada no resolver do Nexus. Diferente de [evolve](../evolve/SKILL.md) (que extrai padrão espontâneo da sessão corrente); skillify é para o loop de composição de skills estável, não descoberta pontual."
skill: skillify
version: 1.4
author: Nexus Agent System
tags: [skillify, meta, compounding, resolver, optimization]
updated: 2026-11-10
source: anthropics/skills (skill-creator) + openai/skills (plugin-creator) + agent-as-a-judge — scaffold, eval A/B, trajetória, packaging /plugin
reads: []
writes:
  - 04-SYSTEM/automation/skills/**
  - 04-SYSTEM/automation/registry/skill-stubs.json
  - 04-SYSTEM/automation/registry/agent-registry.*
  - 04-SYSTEM/automation/agents/_index/moc-skills.md
  - 04-SYSTEM/scripts/run-skill-evals.py
  - 04-SYSTEM/automation/evals/fixtures/**
  - 04-SYSTEM/automation/workflows/portas/**
triggers:
  positive:
    - "transformar workflow manual repetitivo em skill reutilizável"
    - "transformar workflow repetido em skill"
    - "registrar skill no resolver do Nexus"
    - "skills que constroem skills"
  negative:
    - "skill já registrada e estável (edição pontual)"
    - "transformação simples de 1 linha"
    - "sem exemplos concretos de uso"
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7+W8: corpo completo lido pelo shield (opus, somente leitura); W4/W4b/W4c/W4d/W7b/W7c: PASSO 4, template com contrato, writes e portas; W8: gatilho 3+, template com Use when, perfil de modelo e linha de porta; checks frontmatter/lint/evals verdes; 224 linhas, 17 secoes"
---
# Skill: Meta-Meta-Prompt (Skillify)

## Propósito
Transformar workflows manuais repetitivos em skills reutilizáveis e registradas no resolver do Nexus. "Skills que constroem skills" — o loop de composição que torna cada workflow futuro mais rápido.

---

## Quando NÃO usar

- **Skill já registrada e estável** — skillify é para criar/transformar, não editar pontualmente.
- **Transformação simples (typo, ajuste de 1 linha em arquivo que não é porta)** — edição direta basta. Linha nova em porta existente segue o PASSO 0 item 1.
- **Sem exemplos concretos de uso** — transformação sem casos reais vira especulação.

Chamador: a Fase 4 de [evolve](../evolve/SKILL.md) delega a criação ao PASSO 0 e aos PASSOS 2-5 daqui (adr-nx-017).

Disambiguation: `skillify` transforma workflows em skills; `writing-for-agents` melhora skills existentes; `spec-lifecycle` governa o ciclo — cada uma num estágio diferente.


## Condições de Ativação
Ative esta skill quando:
- O usuário executar um workflow manualmente pela 3ª vez
- O usuário solicitar `skillify [workflow descrito]`
- Nexus identificar um padrão repetitivo em 3+ sessões sem skill correspondente

NÃO ative para: workflows únicos; tarefas não-repetíveis; operações de emergência.

---

## Perfil de modelo

Perfil `standard` — autoria de skill é escrita bounded com verifier
(model-routing §Padrão custo-efetivo;
model-catalog §Perfis).
O PASSO 3 (cross-modal eval) é o ponto de escalada: subir effort ali exige
evidência de falha de raciocínio (Hard Rule 2), não antecipação. Esta skill não
mantém pins locais por etapa.

---

## Protocolo de Execução

### PASSO 0 — Escolher o destino

Antes de gerar qualquer arquivo, rode [anti-over-engineering](../anti-over-engineering/SKILL.md) e escolha o MENOR destino que resolve:

1. **1 linha em porta existente** — o caso cabe numa cadeia de `04-SYSTEM/automation/workflows/portas/` (dev, escrita, ...): acrescente a linha e pare (`portas/` está no authority-manifest: a mudança pede rebaseline humano).
2. **Porta manual nova** em `workflows/portas/` — decisão recorrente com cadeia própria. Forma: portas/dev (frontmatter `kind: workflow` e `workflow_contract: 2`; seções `## Cadeia` e `## O que este workflow NÃO decide`) e _contract-v2.
3. **Rotina agendada** — gatilho de tempo. O plano 2026-10-27--workflows-consolidation-plan propõe reduzir as rotinas de 16 para 10: só crie com prova de que nenhuma porta ou rotina existente cobre o caso.
4. **Skill** — procedimento disparado por frase do usuário. Siga os PASSOS 1-5.

Destino 2 ou 3 (workflow) só nasce com este registro preenchido: `Caso de uso recorrente | Porta/rotina existente testada | Por que não cobre | Critério de aceitação verificável | Teste negativo | Responsável pela aprovação`. Gates do destino: `rotina-lint.py`, `test-rotina-contract-v2.py` e verifier com teste negativo; mudar manifest ou registry pede rebaseline humano. Esta skill entrega o destino e o contrato, não o workflow completo. Os PASSOS 1-5 abaixo valem para destino skill.

### PASSO 1 — Capturar o Workflow
Pergunte ao usuário (ou analise o histórico de sessão):
1. Qual é o trigger? (o que inicia este workflow)
2. Qual é o output esperado?
3. Quais são os passos que você sempre segue?
4. Quais são os edge cases que já te surpreenderam?
5. O que nunca deve acontecer neste workflow?

Se analisando histórico automaticamente:
- Extraia sequência de ações recorrente
- Identifique inputs variáveis vs. constantes
- Mapeie os artefatos produzidos

### PASSO 2 — Gerar Skill File
Produza `04-SYSTEM/automation/skills/<categoria>/<nome-da-skill>/SKILL.md` (adr-nx-024: toda skill exposta é uma pasta com `SKILL.md`, e `name` = nome da pasta) seguindo **exatamente** esta estrutura, que é o template do corpo da skill; o contrato herdado é SKILL-BASE. Aplicar princípios Pocock de qualidade (ver writing-great-skills-matt-pocock):
```markdown
---
name: <nome>
description: "Use when: <gatilho em frase do usuário>"
skill: <nome>
version: 1.0
kind: skill-proc
origin: native
triggers:
  positive:
    - "<frase de gatilho positivo>"
  negative:
    - "<frase de gatilho negativo>"
---
# Skill: <Nome>

## Propósito
<1-2 frases com leading word — conceito compacto do pretraining que ancora comportamento>

## Condições de Ativação [quando usar]

## Quando NÃO usar

<casos fora do escopo; aponte a skill vizinha>

## Perfil de modelo [nome do perfil + porque; sem pin de modelo/effort —
a resolucao e da policy model-routing]

## Protocolo de Execução [passos numerados]
<Cada passo termina em completion criterion: checkable + exhaustive>

## Artefatos de Saída

## Completion
<checklist checkable e exhaustive>

## Failure modes
<mínimo 2 modos: sintoma → defesa>

## Restrições [o que NUNCA fazer]
<No-op test em cada NUNCA: "Muda comportamento vs default do modelo?" Se não, deletar.>
```

**Progressive disclosure**: se skill >80 linhas, splitar reference em `references/<topico>.md`.
**Leading word check**: conceito compacto do pretraining? Collapse restatements em single token.

**Anatomia de bundled resources** (skill-creator) — quando a skill precisa mais que o SKILL.md, use dirs padrão, carregados em 3 níveis (metadata sempre → body no trigger → bundled sob demanda):
```
<nome>/
├── SKILL.md          (obrigatório)
├── scripts/          código executável p/ tarefa determinística/repetitiva (roda sem carregar no contexto)
├── references/       docs consultados sob demanda (>300 linhas → incluir índice)
└── assets/           templates/ícones/fontes usados no output
```
Multi-domínio → organizar por variante em `references/` (ex: `aws.md`, `gcp.md`); o modelo lê só a relevante.

**Description "pushy"** (skill-creator) — Claude tende a *sub-disparar* skill. Além da leading word, a description deve nomear contextos explícitos de trigger ("use quando o user mencionar X, Y, ou Z — mesmo sem pedir a skill pelo nome"). Empurrar sem inflar: keywords, não prosa.

### PASSO 3 — Cross-Modal Eval
Avalie a skill em 7 dimensões (score 1–10, threshold 7) — 4 originais + 3 Pocock:
1. **Completude**: cobre todos os edge cases identificados?
2. **Ativação precisa**: as condições de ativação evitam falsos positivos?
3. **Perfil de modelo**: o perfil (sem pin de modelo) está declarado conforme a policy model-routing?
4. **Restrições sufficientes**: as cláusulas NUNCA cobrem os failure modes conhecidos? (passou no no-op test?)
5. **Leading word**: a skill tem um conceito compacto do pretraining que ancora comportamento?
6. **Completion criterion**: cada passo tem critério checkable + exhaustive? (resiste premature completion)
7. **Failure modes**: mínimo 2 modos documentados com sintoma → defesa?

Se qualquer dimensão <7: retorne ao PASSO 2 com os gaps identificados.

**Eval empírico A/B** (skill-creator) — auto-score é subjetivo. Se a skill tem **output objetivamente verificável** (transform de arquivo, extração de dados, geração de código, passos fixos), medir em vez de opinar:
1. Escrever 2-3 prompts de teste realistas (o que um user diria de verdade).
2. Rodar cada um em **2 subagents no mesmo turno**: um *com* a skill, um *baseline* (sem skill, ou versão antiga se estiver melhorando skill existente — snapshot antes de editar).
3. Comparar outputs + capturar `total_tokens`/`duration_ms` de cada run (só chega na notificação da task — salvar na hora).
4. Skill vence baseline nos casos objetivos? Aprova. Empata/perde → gap, volta ao PASSO 2.

Skills de output **subjetivo** (estilo de escrita, design) → pular A/B, ficar no auto-score qualitativo.

**Julgar trajetória** (agent-as-a-judge) — ao comparar runs, não olhar só o output final: a run *com* skill seguiu o processo previsto (steps na ordem, sem chute que acertou por sorte)? Skill que produz output certo por trajetória frágil não é ganho real. Decompor o critério em sub-checks binários > um verdict holístico.

### PASSO 4 — Registrar

1. Em `04-SYSTEM/automation/registry/skill-stubs.json`, adicione `"<nome>": {"desc": "...", "target": "<caminho absoluto>/SKILL.md", "origin": "vault"}`. Este `origin` é do stub; não é o `origin: native` do frontmatter.
2. Acrescente a skill em `04-SYSTEM/automation/agents/_index/moc-skills.md`. Isto a torna "chamada": sem isso o build gera stub sem auto-invocação, não o symlink. Use a linha `<nome>`; nome em texto puro não conta.
3. Rode `python3 04-SYSTEM/scripts/build-skill-stubs.py --plan-symlinks`: a skill deve aparecer como `LINK` (não `STUB` nem `NEEDS-FLAG`). Depois rode o build sem flag e confirme com `--check` (rc 0). Isso cria o symlink `~/.claude/skills/<nome>` (adr-nx-024).
4. Acrescente `"<nome>-<sufixo>": "<categoria>/<nome>"` ao dict `SKILLS` de `04-SYSTEM/scripts/run-skill-evals.py` e rode o script: os casos `<categoria>/<nome>/*` devem aparecer como PASS (o script não lê `evals/fixtures/` sozinho; criar só as fixtures não avalia a skill). As fixtures em `04-SYSTEM/automation/evals/fixtures/skill-<nome>/` (positive, negative, planted; `kind: eval-fixture`) documentam os casos. FAIL de proveniência em skill escrita no vault → `origin: native`; nunca acrescente linha `@` sem transplant real. O caso global `fixture/planted/trigger-duplicado-reprovado` também deve continuar PASS (um trigger positivo duplicado o derruba).
5. Regenere o registry com o escopo completo (um escopo menor trunca o registry): `python3 04-SYSTEM/scripts/build-agent-skill-registry.py --root . --scope 04-SYSTEM/automation --json-output 04-SYSTEM/automation/registry/agent-registry.json --markdown-output 04-SYSTEM/automation/registry/agent-registry.md --check`, e depois o mesmo comando sem `--check`. Mudança no manifest pede rebaseline humano.

**Packaging p/ `/plugin`** (plugin-creator) — só se a skill deve ser **instalável publicamente** (ex: repos `claude-skills`/`claude-agent-dev`). Registro no resolver ≠ distribuição; distribuição exige:
- **Manifest** `.claude-plugin/plugin.json`: `name` (= nome do dir), `version` (semver, bump a cada merge), `description`, `author`, `license`, `keywords`. <!-- drift:ok: caminho de outro projeto -->
- **Nome normalizado**: lower-case hyphen-case, ≤64 chars, `_`/espaço/pontuação → `-`, hífens consecutivos colapsados. Dir e `name` do manifest sempre iguais.
- **Marketplace entry** (`marketplace.json`): `append`, não reordenar; defaults `policy.installation: AVAILABLE`, `policy.authentication: ON_INSTALL`; incluir `category`.
- **De-vault antes de publicar**: sem `wikilinks`, sem paths `~`, sem identidade vault; atribuição correta; `## Exemplo` por skill.

### PASSO 5 — Smoke Test
Execute a skill recém-criada com o caso que a originou:
- Se produzir o mesmo output que o workflow manual: ✅ Aprovada
- Se divergir: identifique o gap, corrija a skill, re-execute

---

## Composição de Skills
Skills podem chamar outras skills. Ao escrever uma nova skill:
- Liste as sub-skills que ela chama em `## Dependências`
- Garanta que melhorias em uma sub-skill se propagam automaticamente
- Evite duplicação: se já existe uma skill para uma sub-tarefa, referencie-a

---

## Artefatos de Saída
- `04-SYSTEM/automation/skills/<categoria>/<nome>/SKILL.md` — a nova skill
- `skill-stubs.json`, fixtures e `moc-skills.md` — registro do PASSO 4
- `04-SYSTEM/automation/workflows/portas/*.md` — a linha acrescentada, quando o destino do PASSO 0 é o item 1

---

## Restrições
- NUNCA crie uma skill genérica demais (ex: "faça coisas") — uma skill deve ter um propósito único e verificável
- NUNCA sobrescreva uma skill existente sem versionar (bump version number)
- Se a skill tiver <3 usos esperados no próximo mês: documente como procedimento, não como skill
