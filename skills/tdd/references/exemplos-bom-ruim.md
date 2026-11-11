---
name: tdd-exemplos-bom-ruim
kind: reference
type: skill
status: active
parent: 04-SYSTEM/automation/skills/dev/tdd/SKILL.md
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Exemplos em TypeScript/Jest, ilustrativos; o vault nao tem TypeScript."
---
```typescript
// BOM: behavior observável, API pública, sobrevive a refactor interno
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});

// RUIM: acoplado à implementação — assere call count em collaborator interno
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});

// RUIM: contorna a interface para verificar
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// BOM: verifica pela interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  expect((await getUser(user.id)).name).toBe("Alice");
});

// RUIM: tautológico — esperado recomputado como o código computa
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  expect(calculateTotal(items)).toBe(items.reduce((s, i) => s + i.price, 0));
});

// BOM: esperado é literal independente
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
