---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: simplify-code
description: "Use when: unidade de trabalho de código fechou (antes de review, commit ou handoff) e o diff tem 10 ou mais linhas substantivas; refino em 3 eixos com verificação de comportamento. Rubrica 5E com veredito SHIP/REFACTOR é code-optimize; revisão de diff é code-review."
updated: 2026-11-10
disable-model-invocation: true
---

# Simplify Code

Refino de código no boundary. 3 reviewers paralelos + verificação que preserva comportamento. Corta complexidade sem quebrar nada.

## Quando rodar (completion-boundary)

Rodar quando **unidade coerente de trabalho fecha** — antes de review, commit, ou handoff. NÃO a cada edit (briga com trabalho em andamento).

**Hard-gates — PULAR (não é inferência, é regra):**
- Mudança só-docs / só-markdown
- Diff mecânico (format, lint, deps, lockfile)
- Arquivos gerados / vendored
- Código marcado explícito "keep as-is"
- < ~10 linhas substantivas de código (piso; 30 p/ mudanças grandes)

Se cair em gate → não rodar, dizer por quê em 1 linha.

## Steps

1. **Delimitar o diff.** Identificar só o código recém-alterado (git diff, ou escopo explícito). NÃO varrer o repo inteiro.

2. **3 reviewers em paralelo** (subagents — 1 por eixo, contexto isolado, retorno ≤ síntese curta):
   - **Reuse** — duplicação, código que já existe no projeto, abstração faltando
   - **Quality** — clareza, nomes, edge cases não tratados, complexidade acidental, **shallow modules** (deletion test: interface ~tão complexa quanto impl → deletar concentra ou só move complexidade? só move = candidato a deepening)
   - **Efficiency** — trabalho redundante, N+1, alocação desnecessária, hot-path
   Cada um retorna: findings ranqueados (critical/warning/nit) + fix concreto.

3. **Aplicar fixes** dos critical + warning. Nits só se baratos.

4. **Verificar preservação de comportamento** (obrigatório, por construção):
   - typecheck passa
   - lint passa
   - testes no escopo passam
   - NÃO enfraquecer testes/tipos, NÃO remover safety check pra "simplificar"
   Se verify falha → reverter o fix que quebrou, reportar.

## Output Format

```markdown
## Simplify — <escopo>

### Aplicado
- [arquivo:linha] [eixo] — <mudança> → <por quê>

### Verify (proof — saída real, não afirmação)
- `<comando rodado>` → `<saída: N passed / 0 errors>` (cita resultado real do comando, nunca "✅" sem ter rodado)
- typecheck / lint / testes no escopo

### Não aplicado (proposto, decisão tua)
- [arquivo:linha] — <sugestão> (motivo de não aplicar auto)
```

## Modo report (diagnóstico sem aplicar)

Invocação `simplify-code --report` (ou chamada por outra skill pedindo diagnóstico): rodar **só passos 1-2** (delimitar diff + 3 reviewers paralelos). NÃO aplicar fixes (pula 3-4), NÃO rodar verify. Retorna findings ranqueados (critical/warning/nit) por eixo, cada um com fix **proposto** — quem chamou decide aplicar. Usado por `pipeline-ads` etapa 3 (review report-only, apply fica na etapa 4).

## Constraints

- NÃO rodar a cada edit — só em boundary (unidade fechada).
- NÃO refatorar fora do diff recente. Escopo = mudança, não repo.
- NÃO enfraquecer testes ou tipos pra passar verify. Preservação de comportamento é invariante.
- NÃO remover safety checks, validações, ou tratamento de erro em nome de "simplicidade".
- NÃO rodar se cair em hard-gate. Reportar o gate.
- Verify SEMPRE antes de declarar pronto (Karpathy #4). Sem verify = incompleto.
- Verify-proof cita saída real do comando (verifier-setup: artefato de prova > afirmação). "Passou ✅" sem output rodado é alegação, não verificação.
- Modo default: **oferecer antes** de rodar. Auto-run só se usuário pedir explícito.

## Anti-racionalização (não pular verify por desculpa)

| Desculpa comum | Contra |
|---|---|
| "código já roda, não precisa verify" | Rodar ≠ comportamento preservado após refactor. Verify é invariante (Karpathy #4). |
| "sem tempo pra testar" | Sem verify = incompleto, não "pronto sem testes". Reporta cobertura parcial, não pula. |
| "esse fix é óbvio/seguro" | Fix óbvio quebra teste tanto quanto fix complexo. Roda typecheck+lint mesmo assim. |
| "enfraquecer o teste simplifica" | Nunca. Enfraquecer teste/tipo pra passar é violação de invariante, não simplificação. |

## Edge Cases

- **Sem suite de testes:** rodar typecheck+lint; avisar que cobertura comportamental é parcial.
- **Diff enorme (>30 arquivos):** subir piso, focar nos arquivos com mais lógica nova, avisar escopo reduzido.
- **Projeto FIAP/Java:** encaixa como etapa do `pipeline-ads` (refatoração cirúrgica). Pode ser chamada standalone ou dentro do pipeline.

## Linhagem

- **Upstream:** `ce-simplify-code` (Every Inc / compound-engineering) — completion-boundary automation + 3 reviewers paralelos + verify by construction.
- **Original (vault):** hard-gates (docs/mecânico/gerado/<10 ln), piso adaptativo por tamanho de diff, deletion-test no eixo quality (Pocock), tabela anti-racionalização (addyosmani/agent-skills), verify-proof (AI-Builder-Club/verifier-setup: artefato de prova), modo "oferecer antes".
- **Critério:** mecanismo > autor. Fonte rastreável, não privilegiada. Alinhado a Karpathy 4P.
