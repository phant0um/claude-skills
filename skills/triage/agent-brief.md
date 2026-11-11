---
type: reference
status: active
version: "1.0.0"
kind: reference
name: agent-brief
parent: "[triage](SKILL.md)"
title: "Reference: Agent Brief"
source: mattpocock/skills (triage/AGENT-BRIEF.md — port R1 2026-08-09)
updated: 2026-08-09
reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 10 secoes, 179 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Princípios](#princípios)
- [Template](#template)
- [Exemplo bom — bug](#exemplo-bom-bug)
- [Exemplo bom — PR](#exemplo-bom-pr)
- [Exemplo ruim](#exemplo-ruim)


# Escrevendo Agent Briefs

Agent brief é o comentário estruturado postado na issue/PR quando ela vai para
`ready-for-agent`. É a **especificação autoritativa** de onde o agente AFK trabalha. O corpo
original e a discussão são contexto; o brief é o contrato.

O brief diz **o que o agente deve fazer**. Para issue: construir a mudança do zero. Para PR:
o que falta **no diff existente** — terminar, fechar lacunas, endereçar pontos de review.

## Princípios

### Durabilidade acima de precisão

A issue pode ficar em `ready-for-agent` por semanas. O codebase muda nesse meio-tempo.

- **Faça**: descrever interfaces, tipos e contratos de comportamento
- **Faça**: nomear tipos, assinaturas e shapes de config que o agente deve procurar/modificar
- **Não**: referenciar path de arquivo — envelhece
- **Não**: referenciar número de linha
- **Não**: assumir que a estrutura atual da implementação permanece

### Comportamental, não procedural

Descreva **o que** o sistema deve fazer, não **como** implementar. O agente explora o
codebase do zero e decide a implementação.

- **Bom:** "o tipo `SkillConfig` deve aceitar um campo opcional `schedule` do tipo `CronExpression`"
- **Ruim:** "abra src/types/skill.ts e adicione um campo schedule na linha 42"
- **Bom:** "ao rodar `/triage` sem argumentos, o user vê um sumário das issues que precisam de atenção"
- **Ruim:** "adicione um switch no handler principal"

### Acceptance criteria completos

O agente precisa saber quando terminou. Todo brief tem critérios concretos e testáveis, cada
um verificável de forma independente.

- **Bom:** "`gh issue list --label needs-triage` retorna issues que passaram por classificação inicial"
- **Ruim:** "triage deve funcionar corretamente"

### Fronteira de escopo explícita

Declare o que está fora. Evita gold-plating e suposição sobre features adjacentes.

## Template

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** descrição de uma linha do que precisa acontecer

**Current behavior:**
O que acontece hoje. Para bug, o comportamento quebrado.
Para enhancement, o status quo sobre o qual a feature se apoia.

**Desired behavior:**
O que deve acontecer depois do trabalho do agente.
Específico quanto a edge cases e condições de erro.

**Key interfaces:**
- `TypeName` — o que muda e por quê
- `functionName()` return type — o que retorna hoje vs. o que deve retornar
- Config shape — novas opções necessárias

**Acceptance criteria:**
- [ ] Critério específico e testável 1
- [ ] Critério específico e testável 2

**Out of scope:**
- Coisa que NÃO deve ser mudada nesta issue
- Feature adjacente que parece relacionada mas é separada
```

## Exemplo bom — bug

```markdown
## Agent Brief

**Category:** bug
**Summary:** truncamento de description corta no meio da palavra

**Current behavior:**
Description acima de 1024 chars é truncada em exatamente 1024, ignorando
fronteira de palavra — sai "Use when the user wants to confi".

**Desired behavior:**
Truncar na última fronteira de palavra antes de 1024 e anexar "...".

**Key interfaces:**
- campo `description` do tipo `SkillMetadata` — sem mudança de tipo, mas a
  lógica de validação/processamento que o popula precisa respeitar palavra
- qualquer função que lê frontmatter de SKILL.md e extrai description

**Acceptance criteria:**
- [ ] Description abaixo de 1024 chars fica inalterada
- [ ] Acima de 1024, trunca na última fronteira de palavra antes de 1024
- [ ] Truncada termina com "..."
- [ ] Comprimento total com "..." não passa de 1024

**Out of scope:**
- Mudar o limite de 1024
- Suporte a description multi-linha
```

## Exemplo bom — PR

Para PR, "Current behavior" descreve o estado do diff, e o brief pede para terminar/corrigir,
não construir do zero.

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** terminar a flag `--json` do contribuidor em `triage list`

**Current behavior:**
O PR adiciona `--json` que serializa a lista de issues. O happy path funciona
e o diff segue a estrutura de comandos do projeto. Faltam dois pontos: erros
ainda saem como texto humano (não JSON), e a flag não tem cobertura de teste.

**Desired behavior:**
Com `--json`, toda saída — inclusive erro — é JSON bem-formado no stdout, e os
exit codes ficam inalterados. Sem a flag, a saída humana fica intocada.

**Key interfaces:**
- o path de erro emite `{ "error": string }` sob `--json`
- reusar o serializer que o PR já adicionou; não introduzir um segundo

**Acceptance criteria:**
- [ ] `triage list --json` emite JSON válido em sucesso e em erro
- [ ] Exit codes batem com o comando não-JSON
- [ ] Um teste cobre a saída `--json` de sucesso e um caso de erro
- [ ] Saída default (não-JSON) byte-for-byte inalterada

**Out of scope:**
- Adicionar `--json` a outros comandos
- Mudar o shape do payload de sucesso que o PR já definiu
```

## Exemplo ruim

```markdown
## Agent Brief

**Summary:** Fix the triage bug

**What to do:**
The triage thing is broken. Look at the main file and fix it.
The function around line 150 has the issue.

**Files to change:**
- src/triage/handler.ts (line 150)
```

Por que é ruim: sem category · descrição vaga · referencia path e linha que envelhecem ·
sem acceptance criteria · sem fronteira de escopo · sem current vs. desired.
