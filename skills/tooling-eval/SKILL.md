---
origin: native
type: skill
status: active
kind: skill-proc
resolver-status: exposed
name: tooling-eval
description: "Use when: avaliar adotar tool/MCP/skill externa — gera nota padronizada (encaixe no vault, overlap com existente, check de segurança fork/supply-chain, checklist de adoção humana). Diferente de analyzing-indicators-of-compromise (IoC de segurança); tooling-eval é adoção de ferramenta."
skill: tooling-eval
version: 1.0
trigger: "@tooling-eval [tool] · 'avaliar ferramenta' · 'vale adotar X?'"
effort: low
tags: [tooling, eval, scout, security, adoption]
attach: scout
updated: 2026-07-06
reads: []
writes:
  - 04-SYSTEM/record/wiki/
triggers:
  positive:
    - "@tooling-eval"
    - "avaliar ferramenta candidata"
    - "vale adotar tool/MCP/skill externa"
    - "check de segurança fork/supply-chain"
  negative:
    - "ferramenta já adotada"
    - "escolha reversível trivial"

reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=skill-proc, 6 secoes, 73 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
 Skill: tooling-eval

## Quando NÃO usar

- **Ferramenta já adotada** — nota é pré-adoção; re-avaliar sem mudança é ruído.
- **Overlap zero com vault** — sem encaixe, nota nem começa.
- **Escolha reversível trivial** (CLI pequena) — nota padronizada é para decisão material.

Disambiguation: `tooling-eval` gera nota de ferramenta-candidata; `repo-radar` compara repos; `skill-source-audit` não existe em automation — use `tooling-eval` para análise de ecossistema de skills. tooling-eval é específico de ferramenta.


## Propósito
Molde único p/ avaliar ferramenta candidata. Evita notas ad-hoc divergentes.

## Saída (nota em 04-SYSTEM/record/wiki/tooling-<nome>.md)
```yaml
title, type: tooling-eval, status: candidata, source, created
```
Seções fixas:
1. **O quê** — 1 linha do que é.
2. **Encaixe** — qual dor do vault resolve, qual agente/rotina consome.
3. **Overlap** — o que já existe que cobre parte disso (honesto).
4. **Check de segurança** — fonte oficial confirmada? supply-chain/fork malicioso?
   permissões pedidas? roda local ou manda dados fora?
5. **Antes de adotar (decisão humana)** — checklist `[ ]`.

## Regra
NUNCA instalar/adotar autonomamente. Skill só PRODUZ a nota. Adoção = humano.

## Completion

- [ ] Ferramenta avaliada contra critérios declarados antes da avaliação.
- [ ] Benchmark/uso real citado, não só docs.
- [ ] Veredito recomendado com custo e esforço de adoção.

## Failure modes

- **Adoção autônoma**: instalar ou adotar a ferramenta → proibido; a skill só produz a nota, adoção é humana.
- **Overlap omitido**: esconder o que já cobre parte da dor → declare o overlap com honestidade.
- **Segurança pulada**: nota sem checar fonte oficial, fork e fluxo de dados → a seção 4 é obrigatória.
- **Nota para escolha trivial**: avaliar CLI pequena e reversível → nota padronizada é para decisão material.
