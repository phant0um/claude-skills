---
origin: native
type: skill
status: active
updated: 2026-11-10
kind: skill-proc
resolver-status: exposed
name: decisions
skill: decisions
version: 1.0
trigger: ['/decisions', '@decisions [decisão]', 'log decision', '/migrate', 'minerar ADRs']
effort: low
tags: [architecture, decisions, audit-trail, patterns, documentation]
source: "agents-md-essencial-codex-thread"
output: "04-SYSTEM/system/decisions/decisions.md | 04-SYSTEM/system/decisions/adr/ | 04-SYSTEM/system/decisions/adr-index.md"
description: "Use when: /decisions — SKILL CANÔNICA para registrar decisão arquitetural (justificativa, alternativas, consequências), publicar no ledger decisions.md e produzir/atualizar ADR quando aplicável. Vizinhos: audit-logging registra trilha append-only de eventos; core/domain-modeling resolve termos de domínio e não publica decisões."
reads:
  - 04-SYSTEM/system/decisions/decisions.md
  - 04-SYSTEM/system/decisions/adr/
writes:
  - 04-SYSTEM/system/decisions/decisions.md
  - 04-SYSTEM/system/decisions/adr/
  - 04-SYSTEM/system/decisions/adr-index.md
triggers:
  positive:
    - "/decisions"
    - "registrar decisão arquitetural"
    - "publicar no ledger decisions.md"
    - "produzir ADR"
    - "registrar decisão"
    - "ADR entry"
  negative:
    - "decisão trivial sem alternativas"
    - "registro de evento (audit-logging)"
    - "resolução de termo de domínio (domain-modeling)"
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7+W8: corpo completo lido pelo shield (opus, somente leitura); W7a: migrate segue roteamento 2 e ramo 5B; W8/W8b: perfil economy, guard de registro e grep em adr-index; checks frontmatter/lint/evals verdes; 247 linhas, 12 secoes"
---
# Skill: Decisions

## Propósito

Registrar toda decisão arquitetural do vault em `04-SYSTEM/system/decisions/decisions.md` com justificativa baseada em padrões — independente de pedido explícito do usuário. Cria trilha de auditoria automática que responde "por que o vault funciona assim?" sem depender de memória de sessão.

**Por que importa:** agentes que decidem sem registrar forçam re-derivação de contexto em sessões futuras. DECISIONS.md elimina esse custo — cada nova sessão encontra o vault com decisões documentadas, não apenas o estado resultante.

---

## Quando NÃO usar

- **Trilha append-only de eventos/progress/receipts** → `audit-logging` (infraestrutura de registro; pode ser chamada por esta skill, sem autoridade arquitetural).
- **Termos/linguagem de domínio ambígua** → `meta/domain-modeling` (resolve vocabulário; não é destino primário de decisões arquiteturais).
- **Decisão trivial reversível** (naming, formato) — registrar toda linha vira ruído; ADR é para decisão com custo de reversão.
- **Decisão já registrada** — duplicar entrada corrompe a trilha; verificar decisions.md antes.
- **Edição em histórico** (04-SYSTEM/record/**) — histórico é imutável; correção vai para gerador ou HUMAN_DECISION.

Disambiguation: `decisions` registra decisões arquiteturais (trilha de auditoria) e, quando a decisão passa nos 3 critérios, cria o ADR individual em `adr/` (ver Fronteira ADR abaixo); verificar conformidade fica fora desta skill — decisions escreve, quem audita só lê.


## Condições de Ativação

Ativar automaticamente (Nexus deve chamar) quando:
- Nova skill criada
- Agente modificado de forma não-trivial (novo model tier, tool adicionada, identidade alterada)
- Estrutura de diretório do vault alterada
- Routing do Nexus modificado
- CLAUDE.md alterado

Ativar manualmente:
- `/decisions` → abre log para entrada manual
- `@decisions [descrição]` → registra decisão descrita

NÃO ativar para: edições mecânicas (frontmatter update, wikilink fix, typo); ingest de sources; hot.md updates.

---

## Modelo

Perfil `economy`: registro é estruturado, sem síntese complexa (perfis em `model-routing.json`).

---

## Protocolo

### 1. Identificar a Decisão

Extrair da sessão atual:
- **O que foi decidido** (fato concreto)
- **Alternativas consideradas** (o que foi descartado e por quê)
- **Padrão ou princípio** que fundamenta a decisão (ex: Karpathy simplicity-first, ECC constrained tools)
- **Contexto** que tornará a decisão compreensível meses depois

### 2. Roteamento (DS-12 2026-08-13 — autoridade de decisões)

Fronteira: **ADR** (arquivo próprio em `adr/adr-nx-NNN-<slug>.md` + entrada em
`adr-index.md`) quando a decisão passa nos **3 critérios**; **decisions.md**
(entrada leve) caso contrário.

1. **Hard to reverse** — custo de mudar ideia depois é significativo
2. **Surprising sem contexto** — leitor futuro vai pensar "por que fizeram assim?"
3. **Real trade-off** — alternativas genuínas existiam e uma foi escolhida por razões específicas

Falhou qualquer critério → decisions.md (log raso, "por que funciona assim").
Passou nos 3 → ADR formal (contexto/decisão/alternativas/consequências) em
`adr/`, com número sequencial e slug; `adr-index.md` ganha linha apontando
para o arquivo. Nunca registrar a mesma decisão nos dois lugares.

### 3. Verificar Duplicata

```bash
grep -i "[palavra-chave da decisão]" 04-SYSTEM/system/decisions/decisions.md 04-SYSTEM/system/decisions/adr-index.md 2>/dev/null | head -5
```

Se decisão similar existir: atualizar entrada existente, não criar nova.

### 4. Formatar Entrada

```markdown
## [YYYY-MM-DD] — [Título da decisão em 1 linha]

**Decisão:** [o que foi decidido — 1-2 frases]

**Alternativas descartadas:**
- [alternativa A] — descartada porque [razão específica]
- [alternativa B] — descartada porque [razão específica]

**Fundamentação:** [padrão/princípio que guiou a decisão]
> Ex: "ECC constrained tools pattern — agentes com acesso irrestrito criam scope creep"
> Ex: "Karpathy simplicity-first — 1 página consolidada > múltiplos fragmentos"

**Contexto:** [o que estava acontecendo que tornou essa decisão necessária]

**Condição de revisão:** [quando esta decisão deveria ser reconsiderada]
```

### 5. Append em `04-SYSTEM/system/decisions/decisions.md`

Se arquivo não existir:
```markdown

# Vault Decisions Log

Decisões arquiteturais do vault-michel. Cada entrada responde: "por que funciona assim?"
Atualizado automaticamente pela skill `/decisions`.

---
```

Depois: append da entrada formatada.

### 5B. Ramo ADR — arquivo formal (quando a decisão passou nos 3 critérios)

NÃO executar o append em decisions.md. Em vez disso:

1. Próximo número sequencial: `ls 04-SYSTEM/system/decisions/adr/adr-nx-*.md` →
   maior `NNN` + 1.
2. Criar `04-SYSTEM/system/decisions/adr/adr-nx-NNN-<slug>.md` com frontmatter
   (title/date/status/agent/model-scope) e seções Contexto/Decisão/Alternativas
   rejeitadas/Consequências (template em `adr/0000-template.md`).
3. Adicionar entrada no `adr-index.md` (formato das seções `## adr-nx-NNN`:
   resumo + `→ Documento completo: ...adr-nx-NNN-slug`).
4. Confirmar: `"ADR adr-nx-NNN registrado + índice atualizado."`

### 6. Confirmar

`"Decisão registrada: [título]. Total: N entradas em decisions.md."`

---

## Completion

- [ ] Decisão tem trade-off real (não é óbvia — "usar markdown" não conta)
- [ ] Entrada tem: Contexto, Decisão, Fundamentação, Alternativas, Data, Condição de revisão
- [ ] Verificação de duplicação feita (grep antes de appendar)
- [ ] Máximo 50 entradas (se exceder: consolidar antes de adicionar)

## Failure modes

- **Obvious decision**: registrar "usar markdown" sem trade-off → só registrar se há alternativa real rejeitada
- **Missing fundamentação**: entrada sem "por que" → fundamentação é o campo mais valioso
- **Passive registration**: só registrar ADRs quando someone pede → modelar domínio ativamente (challenge terms, sharpen fuzzy language, cross-ref com código)
- **Batch capture**: acumular decisões para registrar depois → capturar inline no momento que cristaliza

---

## Migrate mode — brownfield ADR mining (`/migrate`)

Padrão govctl (`govctl-org/govctl`): decisões já existem no repo, só não estão documentadas. `/migrate` **descobre** ADRs implícitos em vez de esperar decisão nova cristalizar.

**Protocolo:**
1. **Varrer o git** por sinais de decisão não-registrada:
   ```bash
   git log --oneline -50 | grep -iE "migra|refactor|substitu|remov|adota|ADR|decisão|drop|switch"
   ```
   Também: comparar decisions.md vs realidade (arquivos que contradizem o que está — ou não — registrado).
2. **Filtrar pelos 3 critérios ADR** (hard-to-reverse · surprising-sem-contexto · trade-off real). Commit mecânico (typo, frontmatter) → skip.
3. **Para cada sobrevivente**, reconstruir o ADR retroativo: o que foi decidido, alternativa descartada (inferir do diff/mensagem), fundamentação. Marcar `retroativo` no contexto (data = data do commit, não hoje).
4. **Guard antes de registrar** (govctl completion gate — executável, não prosa): grep de duplicata + os 3 critérios verdadeiros. Falhou o guard → não registra.
5. Registrar pelo roteamento §2: todo sobrevivente do passo 2 passou nos 3 critérios, então vira ADR em `adr/` com linha em `adr-index.md` (ramo 5B), nunca append em `decisions.md`. Confirmar: `"Mineradas N decisões retroativas de M commits."`

> Guard = gate de completion **checável** (não "revisei"). Bate com Karpathy 4P verify e completion-criterion de [writing-for-agents](../writing-for-agents/SKILL.md). Ver `governance-as-artifact`.

## Domain Modeling Ativo (de domain-modeling)

Não apenas registre — modele ativamente o domínio:

### Challenge contra o glossary
Quando um termo conflita com decisions.md existente: "Sua decisão define 'cancellation' como X, mas você parece significar Y — qual é?"

### Sharpen fuzzy language
Quando user usa termo vago ou overloaded: "Você disse 'account' — quer dizer Customer ou User? São coisas diferentes."

### Discuss concrete scenarios
Quando relações de domínio são discutidas: stress-test com cenários específicos que probe edge cases e forçam precisão sobre boundaries.

### Cross-reference com código
Quando user afirma como algo funciona: checar se código concorda. Se contradição: "Seu código cancela Orders inteiras, mas você disse partial cancellation é possível — qual está certo?"

### Offer ADRs sparingly
Só oferecer ADR quando 3 critérios true:
1. **Hard to reverse** — custo de mudar ideia depois é significativo
2. **Surprising sem contexto** — reader futuro vai pensar "por que fizeram assim?"
3. **Real trade-off** — alternativas genuínas existiam e uma foi escolhida por razões específicas

Se qualquer um falta → skip ADR, não é decisão arquitetural.

> Decisions.md deve ser totalmente devoid de implementation details. É glossary + ADRs, nada mais.
- **Duplicate**: appendar decisão já registrada → grep antes de appendar

---

## Restrições

- NUNCA registrar decisões óbvias sem trade-off real (ex: "usar markdown" não é decisão arquitetural)
- NUNCA criar entrada sem "Fundamentação" — é o campo mais valioso
- NUNCA duplicar — verificar antes de appendar
- Máximo 50 entradas; se exceder → consolidar entradas do mesmo domínio antes de adicionar

---

## Relacionado

- decisions — o arquivo que esta skill mantém
- [codex-retrospective](../evolve/codex-retrospective.md) — retrospective lê decisions.md para entender por que o vault está como está
- spec — spec usa decisions.md como contexto antes de especificar
- nexus — Nexus chama decisions ao fim de qualquer mudança de roteamento
