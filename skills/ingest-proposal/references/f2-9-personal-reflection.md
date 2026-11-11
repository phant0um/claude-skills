---
name: f2-9-personal-reflection
kind: reference
type: skill
status: active
parent: "[ingest-proposal](../SKILL.md)"
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Corrigido o ponteiro `ingest-proposal.md` para `SKILL.md`; F2.9 esta em SKILL.md:72. migration-triagem-binary existe."
---

# F2.9 Personal Reflection (reflect: true only)

Condição de uso: a source chega com `reflect: true`. Volta ao procedimento principal em `SKILL.md`, passo 2 (F2.9).

**Princípio**: informação → conhecimento exige um passo de síntese pessoal. O gate é o marcador binário `reflect: true`: resposta "sim" à pergunta *"isso muda como eu trabalho?"* no gate de reflexão diário (srs-sources FASE 0.5). Ver migration-triagem-binary.

## Quando ativar

- **Só `reflect: true`**: approved sem a flag não recebe Minha Síntese (a maioria).
- Na 1ª ingestão a flag costuma estar ausente → skip; gerada em pipeline posterior, depois que o gate marcar `reflect: true`.
- **Só artigos/ai-agents**: FIAP é material de estudo (preservar, não refletir).
- Máximo 3 reflections por run (evitar fadiga).

## Template: seção adicionada ao final da source page

```markdown
## Minha Síntese

**O que muda:** <1-2 frases: como isto altera o que eu penso ou faço>

**Conexão pessoal:** <1 frase: como isto conecta com projeto/estudo/trabalho atual>

**Próximo passo:** <1 flag: ação concreta — ler X, testar Y, criar Z>
```

## Execução

Após gerar a source page `reflect: true`, uma chamada de IA adicional (mesmo modelo, mesmo contexto da source page) gera `## Minha Síntese`. **Sem bash**: é síntese, não extração. Custo marginal ~100 tokens/source (embutido na mesma chamada que gera a source page).

## Guardrails

- Não inventar ação se não há uma clara → "Nenhum próximo passo imediato".
- Conexão pessoal pode ser "sem conexão direta no momento".
- **Não condensar**: 3 campos obrigatórios, mesmo se curtos.
