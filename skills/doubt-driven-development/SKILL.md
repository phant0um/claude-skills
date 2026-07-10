---
name: doubt-driven-development
description: Sistematiza dúvida como ferramenta de design — enumera as premissas implícitas de um plano e as classifica por risco antes de construir, revelando requisitos ocultos.
trigger: "@doubt [feature/spec/ideia]" | "tenho dúvidas sobre X" | "não tenho certeza se Y" | "doubt this" | "challenge my assumptions" | "what could be wrong here"
---

# Skill: Doubt-Driven Development

## Propósito

Sistematizar dúvida como ferramenta de design. Antes de construir, enumerar tudo que poderia estar errado nas premissas — não como exercício defensivo, mas como descoberta ativa de requisitos ocultos.

Adaptado de addyosmani/agent-skills (github.com/addyosmani/agent-skills).

Diferença vs. skill `grill-me`: grill-me desafia um **plano** com perguntas duras. Doubt-driven desafia as **premissas** que o plano assume como verdade — é upstream do grill.

---

## Condições de Ativação

Ative esta skill quando:
- `@doubt [feature/spec/ideia]` for chamado
- Antes de escrever uma spec em feature com >3 premissas implícitas
- Quando o usuário disser "tenho dúvidas sobre X", "não tenho certeza se Y"
- Após grilling, antes de implementar — como segunda camada de verificação

NÃO ative para: bugs pontuais com causa raiz já identificada; tarefas mecânicas sem decisão de design; quando `grill-me` já rodou e não encontrou premissas frágeis.

---

## Protocolo de Execução

### ETAPA 1 — Enumerar Premissas

Liste todas as premissas implícitas no pedido/spec. Uma premissa é qualquer afirmação que precisa ser verdade para o design funcionar.

```
PREMISSAS — [título]

P1: [premissa] — fonte: [explícita | inferida | assumida]
P2: [premissa] — fonte: ...
...
```

**Tipos de premissa:**
- **Domínio** — "usuários têm email único" (regra de negócio)
- **Técnica** — "a API suporta paginação cursor-based" (constraint externa)
- **Comportamental** — "usuários vão usar isso semanalmente" (expectativa de uso)
- **Temporal** — "os dados estarão disponíveis até Q3" (deadline implícito)

### ETAPA 2 — Aplicar os 5 Tipos de Dúvida

Para cada premissa, aplicar **uma ou mais** dúvidas:

| # | Tipo de dúvida | Pergunta |
|---|----------------|----------|
| D1 | **Falsabilidade** | "Como provaríamos que esta premissa é falsa?" |
| D2 | **Condicional** | "Sob qual condição esta premissa deixa de valer?" |
| D3 | **Cascade** | "Se esta premissa for falsa, quais outras caem junto?" |
| D4 | **Temporal** | "Esta premissa é verdade hoje — será em 6 meses?" |
| D5 | **Proxy** | "Esta premissa é o que queremos saber, ou um proxy para outra coisa?" |

**Regra:** nem toda premissa precisa de todas as dúvidas. Priorizar premissas com fonte = `assumida` e premissas que aparecem em >1 cascata.

### ETAPA 3 — Classificar Risco

```
RISCO — [título]

| Premissa | Dúvida ativa | Veredito | Ação |
|----------|-------------|----------|------|
| P1 | D1 Falsabilidade | confirmada | prosseguir |
| P2 | D3 Cascade | frágil — derruba P5, P6 | verificar antes de build |
| P3 | D5 Proxy | é proxy de P7 | reescrever P3 em termos de P7 |
| P4 | D2 Condicional | condicional a X | adicionar X como requisito explícito |
```

**Vereditos:**
- `confirmada` — premissa verificada, prosseguir
- `frágil` — premissa não verificada, precisa validação antes de build
- `condicional` — premissa só vale sob condição X → X vira requisito
- `falsa` — premissa invalidada → redesign necessário
- `proxy` — premissa é stand-in para questão real → reescrever

### ETAPA 4 — Output

```markdown
## Doubt Analysis — [título]

### Premissas verificadas (confirmadas)
- [lista]

### Premissas frágeis (precisam validação)
- P[N]: [por que é frágil] → [como validar antes de build]

### Premissas condicionais
- P[N]: só vale se [X] → X adicionado como requisito

### Premissas invalidadas
- P[N]: [por que é falsa] → [impacto no design]

### Premissas proxy
- P[N] é proxy para P[M] → reescrever em termos de P[M]

### Próximo passo
[spec | grill-me | validação externa | redesign | descartar]
```

---

## Exemplo

**Pedido:** "Enviar um email de resumo semanal para cada usuário toda segunda de manhã."

```
PREMISSAS — email de resumo semanal

P1: cada usuário tem um email válido — fonte: assumida
P2: existe atividade suficiente numa semana para resumir — fonte: assumida
P3: "segunda de manhã" é bom para todos — fonte: assumida (fuso horário)
P4: o provedor de email aguenta o envio em lote — fonte: inferida

RISCO
| Premissa | Dúvida | Veredito | Ação |
|----------|--------|----------|------|
| P1 | D2 Condicional | condicional | usuários sem email → pular, não falhar o job |
| P2 | D1 Falsabilidade | frágil | usuário inativo recebe email vazio → definir mínimo de atividade |
| P3 | D5 Proxy | proxy de "quando o usuário lê email" | "segunda 9h" é proxy do fuso local; enviar no fuso de cada um |
| P4 | D4 Temporal | frágil | funciona com 100 users; e com 100k? verificar rate limit |
```

**Próximo passo:** P2 e P4 precisam validação antes de build; P3 vira requisito de fuso horário.

---

## Diferença vs. Grill-me

| Aspecto | Grill-me | Doubt-driven |
|---------|---------|--------------|
| Alvo | Plano (como fazer) | Premissas (o que assumimos) |
| Método | Perguntas duras iterativas | Enumeração + classificação sistemática |
| Output | Síntese de riscos + decisões | Tabela de premissas + vereditos |
| Quando | Antes de spec | Antes de grill (upstream) ou após grill (verificação) |
| Interação | Iterativo (uma pergunta por vez) | Batch (enumera tudo, depois classifica) |

**Pipeline ideal:** doubt-driven → grill-me → spec → build

---

## Completion

- [ ] Todas as premissas com fonte = `assumida` receberam pelo menos 1 dúvida
- [ ] Cascata (D3) executada para premissas frágeis
- [ ] Toda premissa `frágil` tem ação de validação específica
- [ ] Toda premissa `condicional` gerou requisito explícito
- [ ] Output indica próximo passo claro

## Failure modes

- **Dúvida cosmética**: aplicar dúvidas só nas premissas explícitas, ignorando as assumidas → o valor está nas assumidas
- **Dúvida sem ação**: classificar como `frágil` mas não especificar como validar → sempre incluir método de validação
- **Enumeração incompleta**: listar 3 premissas quando há 10 → forçar pelo menos 5, mesmo que pareçam óbvias
- **D3 Cascade ignorada**: não rastrear quais premissas caem junto → é onde redesign é necessário vs. ajuste pontual

---

## Referências

- Ver skill `grill-me` — desafia o plano (downstream).
- Uma spec emerge de premissas já verificadas.
- Princípio de fundo: pensar antes de agir.
