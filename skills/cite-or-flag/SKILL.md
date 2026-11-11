---
origin: native
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: cite-or-flag
description: "Use when: afirmação de alta consequência precisa de fonte · suspeita de citação inventada. Verificação de fato/citação — cita fonte real ou marca [não-verificado]. Anti-fabricação cross-system."
type: skill
created: 2026-06-27
updated: 2026-07-06
reads: []
writes: []
triggers:
  positive:
    - "afirmação de alta consequência precisa de fonte"
    - "suspeita de citação inventada"
    - "verificação de fato/citação"
  negative:
    - "afirmação trivial sem risco"
    - "fonte já verificada"

reviewed-scope: "checagem mecanica + semantica: 0/0 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 6 secoes, 66 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
 cite-or-flag — citar ou sinalizar

Aplica quando: agente afirma fato verificável (número, lei, norma, citação, data, preço).
Reusa o mecanismo citation-verify (T37/opendraft) generalizado p/ além de papers.

## Quando NÃO usar

- **Claim de baixa consequência** — verificação de fonte custa; reservar para alta consequência.
- **Conteúdo sem fonte declarada e irrelevante** — flag só o que pode virar norma; o resto é ingest normal.
- **Busca de fato geral** — cite-or-flag é para citação específica, não pesquisa.

Disambiguation: `cite-or-flag` verifica citação/fato de alta consequência; `connection-finder` conecta fontes; `grounded-citations` não existe — use `cite-or-flag` (com `connection-finder`) para fundamentação factual.


## Regra
1. Fato verificável → tem fonte? Sim: citar (autor/lei-art./URL/data).
2. Não tem fonte → marcar `[não-verificado]`, não afirmar como certo.
3. Texto normativo/citação literal → **verbatim**, nunca parafrasear (ver T41a).

## Systems de alto risco de fabricação (registrar disponível)
- **concurso-coach:** lei seca, súmula, jurisprudência.
- **finance:** preço, Selic, DARF, múltiplo, data de balanço.
- **tjam-Lex:** artigo/inciso/norma.
- Validação de fonte vault-wide vive **aqui** (`cite-or-flag`) — desde 2026-07-02, quando `source-validator` (knowledge) foi arquivado c/ a dissolução do Knowledge System.

## Liga a
hallucination-gate (T15/adversarial-gate), citation-verify (T37).

## Completion

- [ ] Fato de alta consequência SEM fonte foi flagado (nunca silenciado).
- [ ] Fonte citada (wikilink) para afirmação verificável.
- [ ] Quando não há fonte: `[não-verificado]` presente e visível.

## Failure modes

- **Fato sem fonte afirmado como certo**: claim verificável sai sem citação → marque `[não-verificado]`.
- **Paráfrase de texto normativo**: lei, súmula ou citação reescrita → cite verbatim.
- **Verificar tudo**: gastar verificação em claim de baixa consequência → reserve para o que pode virar norma.
- **Flag silenciado**: remover `[não-verificado]` sem fonte nova → a marca fica visível até haver fonte.
