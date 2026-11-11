---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-05-dominio-extend
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 1 secoes, 47 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---

> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: Regra de domínio (extend).

## Regra de domínio (extend)

Classificar candidato em domínio via keyword bash-first (mesmo motor de scoring),
alimentando o campo frontmatter `dominios:` (T5). Domínios:

- **finance** — preço, ETF, FII, Selic, DARF, ticker, mercado, ações
- **evolucao** — hábito, rotina, produtividade, meta, reflexão
- **empreend** — startup, MVP, launch, negócio, produto
- **ai-agents** — agent, LLM, Claude, Hermes, skill, harness, loop
- **fiap** — FIAP, ADS, semestre, apostila, MVC, Fintech
- **concurso** — CESPE, FCC, FGV, edital, cargo, servidor público
- **geral** — fallback (nenhum match)

```bash
# BUG-FIX 2026-07-11: RHS de [[ =~ ]] NÃO pode ter aspas (aspas → | vira literal,
# alternância morre). E precisa elif+prioridade: ai-agents ganha de finance quando
# ambos casam (senão ML/robótica/quant-com-agent vaza p/ finance). Ordem: fiap >
# concurso > ai-agents > empreend > finance > evolucao > geral.
# Causa do misroute 62-finance (pipeline-semanal 07-11): script /tmp bugado sem esta regra.
domain="geral"
if   [[ $snippet =~ FIAP|ADS|apostila|MVC|Fintech\ FIAP ]]; then domain="fiap"
elif [[ $snippet =~ CESPE|FCC|FGV|edital|cargo\ público|servidor\ público ]]; then domain="concurso"
elif [[ $snippet =~ agent|LLM|Claude|Hermes|skill|harness|loop|prompt|GPT|model|robot|benchmark|inference|quantiz|LangChain|MCP|token|eval ]]; then domain="ai-agents"
elif [[ $snippet =~ startup|MVP|launch|negócio\ próprio|produto\ digital|B2B|go-to-market ]]; then domain="empreend"
elif [[ $snippet =~ preço|ETF|FII|Selic|DARF|ticker|ações|mercado\ financeiro|quant|trading|portfolio|market\ regime|invest ]]; then domain="finance"
elif [[ $snippet =~ hábito|rotina|produtividade|meta\ semanal|reflexão ]]; then domain="evolucao"
fi
```

> Se T5 já rodou, esta regra alimenta o mesmo campo `dominios:`. Não duplicar lógica.

---

