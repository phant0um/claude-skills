---
type: reference
status: active
version: "1.0.0"
kind: reference
name: out-of-scope-kb
parent: "[triage](SKILL.md)"
title: "Reference: Out-of-Scope KB"
source: mattpocock/skills (triage/OUT-OF-SCOPE.md — port R1 2026-08-09)
updated: 2026-08-09
reviewed-scope: "checagem mecanica + semantica: 1/1 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 8 secoes, 122 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Estrutura](#estrutura)
- [Formato](#formato)
- [Quando ler](#quando-ler)
- [Quando escrever](#quando-escrever)
- [Atualizar ou remover](#atualizar-ou-remover)


# Out-of-Scope Knowledge Base

O diretório `.out-of-scope/` guarda registro persistente de feature request **rejeitada**.
Serve a dois propósitos:

1. **Memória institucional** — por que foi rejeitada, para o raciocínio não morrer junto com a issue
2. **Deduplicação** — quando chega request igual, a skill mostra a decisão anterior em vez de relitigar

## Estrutura

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

Um arquivo por **conceito**, não por issue. Várias issues pedindo a mesma coisa ficam agrupadas.

## Formato

Escrito em estilo solto e legível — mais documento de design curto que registro de banco.
Parágrafos, exemplos e código para deixar o raciocínio claro para quem chega depois.

```markdown
# Dark Mode

Este projeto não suporta dark mode nem theming user-facing.

## Por que está fora de escopo

O pipeline de render assume uma paleta única definida em `ThemeConfig`.
Suportar múltiplos temas exigiria:

- Um theme context provider envolvendo toda a árvore de componentes
- Resolução de estilo theme-aware por componente
- Camada de persistência para preferência do usuário

Mudança arquitetural grande que não alinha com o foco do projeto em autoria de
conteúdo. Theming é problema de consumidor downstream que embute a saída.

## Prior requests

- #42 — "Add dark mode support"
- #87 — "Night theme for accessibility"
```

### Nome do arquivo

Kebab-case curto e descritivo do conceito: `dark-mode.md`, `plugin-system.md`. Reconhecível
o bastante para alguém entender o que foi rejeitado sem abrir.

### Escrevendo o motivo

Substantivo — não "não queremos isso", mas por quê. Motivos bons referenciam:

- Escopo ou filosofia do projeto ("o foco é X; theming é problema downstream")
- Restrição técnica ("exigiria Y, que conflita com a arquitetura Z")
- Decisão estratégica ("escolhemos A em vez de B porque...")

O motivo tem que ser durável. Evitar circunstância temporária ("estamos sem tempo agora") —
isso não é rejeição, é adiamento.

## Quando ler

No Gather Context (passo 2 do protocolo), ler todos os arquivos de `.out-of-scope/`.

- Checar se o request casa com conceito já rejeitado
- Casamento é por **similaridade de conceito**, não keyword — "night theme" casa com `dark-mode.md`
- Se casou, mostrar ao maintainer: "parecido com `.out-of-scope/dark-mode.md` — rejeitamos <!-- drift:ok: exemplo -->
  antes porque [motivo]. Ainda vale?"

O maintainer pode: **confirmar** (nova issue entra em "Prior requests", fecha) ·
**reconsiderar** (arquivo deletado/atualizado, issue segue triage normal) ·
**discordar** (relacionadas mas distintas, segue triage normal).

## Quando escrever

Só quando **enhancement** (não bug) é rejeitada como `wontfix`. Vale igual para PR de
enhancement — PR rejeitado é registrado aqui para o mesmo pedido não voltar como código novo.

**Não** escrever quando o `wontfix` é por **já estar implementado**. Isso é feature
construída, não rejeitada; registrar envenenaria o dedup com rejeição falsa. Nesse caso o
comentário de fechamento aponta onde a feature já vive.

Fluxo:

1. Maintainer decide que o request está fora de escopo
2. Checar se já existe arquivo do conceito
3. Se sim: anexar a issue em "Prior requests"
4. Se não: criar arquivo com conceito, decisão, motivo e primeiro prior request
5. Comentar na issue explicando e mencionando o arquivo
6. Fechar com label `wontfix`

## Atualizar ou remover

Se o maintainer muda de ideia sobre conceito rejeitado: deletar o arquivo. A skill não
reabre issues antigas — são registro histórico. A issue nova que provocou a reconsideração
segue triage normal.
