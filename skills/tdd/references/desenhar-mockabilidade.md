---
name: tdd-desenhar-mockabilidade
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/dev/tdd/SKILL.md
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Exemplos em TypeScript, ilustrativos; o vault nao tem TypeScript (forge.md: 0 .ts)."
---
**1. Dependency injection** — passe a dependência externa em vez de criá-la dentro.

```typescript
// fácil de mockar
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// difícil de mockar
function processPayment(order) {
  return new StripeClient(process.env.STRIPE_KEY).charge(order.total);
}
```

**2. Interface estilo SDK, não fetcher genérico** — uma função por operação externa, em vez
de uma função genérica com lógica condicional.

```typescript
// BOM: cada função mockável isoladamente
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// RUIM: mockar exige lógica condicional dentro do mock
const api = { fetch: (endpoint, options) => fetch(endpoint, options) };
```

SDK dá: um shape por mock, zero condicional no setup, visível quais endpoints o teste
exercita, type safety por endpoint.
