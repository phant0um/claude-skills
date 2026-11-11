---
origin: native
triggers:
  positive:
    - "otimizar código"
    - "rubrica 5E"
    - "SHIP ou REFACTOR"
    - "encontrar code smell"
    - "otimiza esse trecho: <código>"
  negative:
    - "código novo sem testes"
    - "mudança cosmética solicitada como refactor"
    - "exploração de design pré-código"
    - "deadline de merge com review já aprovado"
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: code-optimize
description: "Use when: pedido de otimizar, limpar ou melhorar código, tipo 'otimiza esse código', 'isso tá feio, melhora', 'tem code smell aqui?', 'dá pra simplificar esse trecho?'. Dispara mesmo com código colado na conversa; também para 'roda a 5E'. Veredito é SHIP ou REFACTOR. Revisão geral de diff é code-review."
version: 2.1
author: Forge / Vault SO
source: "mattpocock/skills v1.1 (code-review — two-axis parallel subagents + Fowler smell vocab) folded into 5E"
tags: [code-quality, refactoring, 5E, clean-code, review, SOLID, code-smells]
updated: 2026-11-10
reads: []
writes:
  - 06-GENERATED/tasks/lessons.md
reviewed: 2026-11-10
reviewed-by: "claude-sonnet-5-5 (achados: shield claude-opus-5-5)"
reviewed-scope: "2026-11-10 W7: corpo completo lido pelo shield (opus, somente leitura); W4/W4b: PASSO 4 e ponteiros para code-review; checks frontmatter/lint/evals verdes; 251 linhas, 12 secoes"
---

# Skill: Code Optimize

## Propósito

Revisar e otimizar código contra o **rubrica 5E** (Fluência, Eficiência, Eficácia, Economicidade, Efetividade). Cada dimensão é um **gate binário PASS/FAIL** (BinEval — sem score composto 0-100, que é opaco e enviesa). Findings são classificados **blocking** (correção/segurança/estrutural severo → força REFACTOR) vs **non-blocking** (style). Veredito final: **SHIP | REFACTOR**. Pode ser chamada standalone, pelo Nexus ou pela skill `implement`.

> Por que binário: score 0-100 esconde qual dimensão falhou e cria falsa precisão (78 vs 82 não é acionável). Ver binary-eval-statistics.

---

## Quando NÃO usar

- **Código novo sem testes/execução** — otimizar sem comportamento verificado é chute; TDD antes.
- **Mudança cosmética solicitada como refactor** — 5E é sobre qualidade estrutural; style-only vai para lint.
- **Deadline de merge imediato com review aprovado** — reabrir gate sem mudança nova é cerimônia.
- **Exploração de design (pré-código)** — design vai para `codebase-design`; optimize age no código existente.

Disambiguation: `code-optimize` revisa contra rubrica 5E (BinEval, SHIP|REFACTOR); `code-review` revisa um diff em dois eixos, Standards e Spec, com revisores shield, e não carrega a rubrica 5E; `reason-judge` pontua por rubrica genérica — optimize é específico de código e binário.

## Condições de Ativação

Ative esta skill quando:
- O usuário ou o Nexus pedir revisão 5E (SHIP|REFACTOR) de código de aplicação
- Gate de qualidade for exigido antes de merge
- Refactoring proativo for solicitado

NÃO ative para: arquivos de configuração pura (YAML, JSON de infra); migrações de banco (→ `fullstack-code`, Migration Review); arquivos gerados automaticamente.

---

## Perfil de modelo

Perfil `deep` (auditoria semântica: as 5 dimensões julgam design, não sintaxe). Modelo e effort resolvem na policy: model-routing §Padrão custo-efetivo; model-catalog §Perfis.

---

## Protocolo de Execução

### PASSO 1 — Receber artefato

Obtenha o código. Se não vier inline, leia o(s) arquivo(s) de `workspace/` ou o path dado; identifique linguagem, framework e contexto de uso.

### PASSO 1.5 — REVIEWS.md do repo (override dos defaults)

Se existir `REVIEWS.md` na raiz do repo revisado, **carregar e aplicar** antes da rubrica. Ele define o que é nitpick e o que é blocking *naquele* repo; seus standards **sobrepõem** os defaults 5E em conflito. A rubrica é fallback quando o arquivo não existe. Não é config compartilhada: cada repo tem o seu.

Review memory (feedback recorrente do usuário via `/meta-learn`) propõe update ao `REVIEWS.md`. Ref: reviews-md-pattern.

### PASSO 2 — Análise paralela por dimensão *(5 lentes simultâneas)*

Execute as 5 dimensões como lentes independentes. Cada uma retorna **PASS** (nenhum check falhou) ou **FAIL** (≥1 check falhou → gera finding):

**Fluência — PASS/FAIL**
- Nomes descrevem intenção sem comentário?
- Funções ≤20 linhas e fazem uma coisa?
- Sem duplas negativas, sem magic numbers, max 3 níveis de aninhamento — prefira early return
- Convenções consistentes no arquivo

**Eficiência — PASS/FAIL**
- Complexidade O(n²) onde O(n log n) ou O(n) existe?
- Queries dentro de loops (N+1)?
- Travessias redundantes que poderiam ser fundidas?
- Alocações desnecessárias em hot paths?
- Filtro sem índice sobre dataset grande?
- Bloqueio síncrono onde async é possível?

**Eficácia — PASS/FAIL**
- Implementação bate com a spec/contrato declarado?
- Edge cases cobertos: null, vazio, boundary, negativo?
- Erros explícitos — sem exceções silenciadas?
- Tipos validados nos boundaries do sistema?
- Cada teste cobre uma claim comportamental distinta?

**Economicidade — PASS/FAIL**
- Lógica duplicada que deveria ser extraída (DRY)?
- Código morto: branches inalcançáveis, imports não usados?
- Abstração prematura para um único uso (YAGNI)?
- Dependências pesadas para utilidade trivial (use stdlib)?
- Config que pertence ao ambiente, hardcoded no código?

**Efetividade — PASS/FAIL**
- SRP: cada módulo tem uma razão para mudar?
- OCP: extensível sem modificar código existente?
- LSP: subtipos substituíveis pelo tipo base?
- ISP: sem interfaces gordas que forçam implementação morta?
- DIP: depende de abstrações, não de concretions?
- Acoplamento baixo entre módulos, coesão alta dentro?

### PASSO 2.5 — Dois eixos em subagentes paralelos (Standards + Spec)

Com harness de subagentes, o par Standards/Spec (um shield por eixo, em paralelo) segue [code-review](../code-review/SKILL.md) §5 (use os briefs de lá, acrescidos dos checks 5E do eixo, PASSO 2); não é repetido aqui. Mapeamento 5E → eixo: **Standards** = Fluência + Economicidade + Efetividade; **Spec** = Eficácia (+ Eficiência onde a spec define SLA). Sem harness: rode as 5 lentes inline (PASSO 2); o mapeamento é o mesmo.

### PASSO 2.6 — Vocabulário de code smells (Fowler)

A lista de smells (Fowler, mais dois do Poteto) e a correção de cada um vivem em [code-review](../code-review/SKILL.md) §3; não são repetidas aqui. Ao avaliar Fluência, Economicidade e Efetividade, cite o smell pelo nome. Mapeamento para os gates 5E: Mysterious Name → Fluência; Duplicated Code e Speculative Generality → Economicidade; Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Divergent Change, Message Chains e Middle Man → Efetividade; os demais de §3 (Shotgun Surgery, Refused Bequest, Comentário-justificativa, Padrão contagioso) → Efetividade.

### PASSO 2.7 — Deepening (condicional)

Se encontrar shallow module, fricção de navegação ou código difícil de testar pela interface atual, leia [deep-modules](references/deep-modules.md) e aplique o Deletion Test antes de propor deepening.

### PASSO 3 — Classificar findings + veredito

Cada finding é **blocking** ou **non-blocking**:

| Dimensão | Finding é blocking quando… |
|----------|----------------------------|
| Eficácia | quase sempre — silent error, edge case não tratado, violação de contrato quebram correção → **blocking** |
| Efetividade | quando estrutural (acoplamento que impede mudança segura) → **blocking** |
| Eficiência | blocking só com antes/depois do mesmo workload (comando, tempo, saída equivalente) mostrando degradação real em hot path; micro-otimização ou sem medição → non-blocking; cache novo → `anti-over-engineering` ultra |
| Economicidade | non-blocking em geral; blocking só se a duplicação causa comportamento divergente |
| Fluência | **non-blocking** (style) — nunca bloqueia sozinha |

**Desempate.** Na dúvida entre blocking e non-blocking: se **roda errado ou perde dado** → blocking. Se só é feio → non-blocking.

**Veredito** (sem número):
- **SHIP** — 0 findings blocking (findings non-blocking podem existir, endereçar oportunisticamente)
- **REFACTOR** — ≥1 finding blocking → entregar versão refatorada

### PASSO 4 — Refactoring

Para cada finding:
1. Cite linha exata
2. Explique o problema em uma frase
3. Mostre before/after inline
4. Marque **[blocking]** ou **[non-blocking]**

Se veredito REFACTOR ou refactor explicitamente solicitado: entregue arquivo completo refatorado.

### PASSO 5 — Evidência e log

```markdown
## Veredito: SHIP | REFACTOR
| Dimensão | Gate | Findings (blocking / total) |
|----------|------|------------------------------|
| Fluência | PASS/FAIL | 0 / N |
| ... | ... | ... |
## Findings
[por dimensão, com linha, before/after, e [blocking]/[non-blocking]]
```

Entregue o resultado na resposta. Só em repositório externo que já tenha `docs/logs/quality.md`, faça append lá (nunca overwrite); este vault não tem esse arquivo e a skill não o cria. <!-- drift:ok: caminho de outro projeto -->

---

## Action Plan Execution Pattern

Quando o veredito é REFACTOR (≥1 finding blocking), execute o action plan em ordem: **P1** (Economicidade + Eficácia: extrair helpers DRY + testes faltantes) → **P2** (Fluência: split de funções >20 linhas, nomear magic numbers, reduzir nesting) → **P3** (Eficiência + Efetividade: regex compilado no lugar de N×str.count, read-once-decode-many, lazy import; só entra com ganho medido). Itens anteriores destravam os posteriores.

Pitfalls do action plan:
- **Semantics shift no split**: extrair função que levanta exceção quando original retornava status enum → except captura como ERRO em vez de IGNORADO. Solução: retornar `None` para casos não-suportados.
- **PYTHONPATH pollution**: venv do scheduler legado vaza para venv do projeto. Usar `PYTHONPATH="" .venv/bin/python -m pytest` para isolar.
- **Feature durante refactor**: implementar APÓS P1-P2 (beneficia da estrutura limpa) mas ANTES de P3 (otimizações podem cobrir o novo código).

---

## Completion

**Critério de sucesso:** veredito SHIP/REFACTOR emitido com tabela de gates; cada finding com linha exata, before/after e tag [blocking]/[non-blocking]; resultado entregue na resposta (append em `docs/logs/quality.md` só em repo externo que o tenha).

- [ ] 5 dimensões avaliadas como gate PASS/FAIL (Fluência, Eficiência, Eficácia, Economicidade, Efetividade)
- [ ] Se subagentes disponíveis: eixos Standards + Spec rodados em paralelo (senão inline)
- [ ] Code smells nomeados (Fowler) onde presentes — não descrição genérica
- [ ] Cada finding cita linha exata + before/after + [blocking]/[non-blocking]
- [ ] Veredito emitido: SHIP (0 blocking) | REFACTOR (≥1 blocking)
- [ ] Se REFACTOR: arquivo completo refatorado entregue
- [ ] Resultado entregue na resposta (append em `docs/logs/quality.md` só em repo externo que o tenha)

## Failure modes

- **Finding sem linha ou sem tag**: problema sem número de linha ou sem blocking/non-blocking → não conta para o veredito
- **Style blocking / score numérico**: Fluência nunca é blocking; score 0-100 ou composto é proibido (ver Regras Invariantes)
- **Partial refactor**: entregar refactor parcial → se entrega, entrega arquivo completo
- **Shallow module blindness**: não identificar module com interface tão complexa quanto implementation → deepening opportunity perdida
- **Semantics shift no split**: extrair sub-função que muda o tipo de retorno (raise vs return None) → except captura como erro em vez de status esperado
- **Hardcoded constant vs passed parameter**: função aceita parâmetro mas body usa constante do módulo → usuário passa valor mas função ignora. Sentinel/Forge detecta como funcional bug mesmo com tests passando (test usa valor que cai dentro do default hardcoded)

---

## Regras Invariantes

- NUNCA classificar finding de style (Fluência) como blocking — style nunca força REFACTOR sozinho
- NUNCA penalizar trade-offs documentados/aprovados (ex: denormalização intencional)
- NUNCA entregar refactor parcial — se entrega, entrega o arquivo completo
- NUNCA reintroduzir score numérico 0-100 ou composto — veredito é binário SHIP | REFACTOR
- NUNCA escalar modelo sem evidência de falha de raciocínio — Hard Rule 2 da
  model-routing; FAIL blocking em
  Eficácia/Efetividade é a evidência que autoriza a escalada

---

## Artefatos de Saída

- `docs/logs/quality.md` — histórico de vereditos por arquivo (só em repo externo que já o tenha) <!-- drift:ok: caminho de outro projeto -->
- Diff de refactor proposto na resposta (quando REFACTOR ou solicitado); aplicar é da skill de camada, não desta
- Veredito + tabela de gates inline na resposta


---

## Self-Improvement

Após cada execução:
1. Se dimensão FAIL recorrente (≥2× mesmo arquivo) → flag para `@harden forge` com dimensão persistente
2. Se refactor introduziu regressão → registrar padrão em `06-GENERATED/tasks/lessons.md`
3. Lições append: `- YYYY-MM-DD: [code-optimize] <arquivo> veredito=SHIP/REFACTOR, gate mais fraco=<dimensão FAIL>`

> Ver: [hill-climb](../hill-climb/SKILL.md) · autoresearch-loop

---

## Relacionado

- [fullstack-code](../fullstack-code/SKILL.md)
- [complexity-ratchet](../codebase-design/complexity-ratchet.md)
- parallel-agent-code-review
- [spec-verify](../spec-lifecycle/spec-verify.md) — eixo Spec standalone (fidelidade ao spec/ticket)
- [tdd](../tdd/SKILL.md) — refactor estrutural migrou do loop TDD: esta skill faz o refactor 5E; o `/code-review` (skill `code-review`) revisa o diff (Pocock v1.1)
- [implement](../implement/SKILL.md) — chama esta skill (/review) antes do commit
