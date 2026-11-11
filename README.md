# claude-skills

Skills para Claude Code, espelhadas de um vault Obsidian que opera como sistema operacional de agentes de IA.

O vault é a fonte. Este repo é gerado por um script de export: toda skill com `status: active` vem para cá, sem paths absolutos e com os wikilinks do Obsidian convertidos em links Markdown relativos. Link para página do vault que não está publicada aqui vira texto puro.

## Instalar

```
/plugin marketplace add phant0um/claude-skills
/plugin install claude-skills
```

A skill carrega quando a `description` casa com a tarefa. Para invocar pelo nome, use `/<nome>`.

## O que tem aqui

[`skills/INDEX.md`](skills/INDEX.md) lista cada skill com o gatilho dela. Cada skill mora em `skills/<nome>/SKILL.md`, com references e scripts ao lado.

Muitas skills foram escritas para o vault (pipeline de ingest, rotinas, contratos de agente) e ainda citam paths como `04-SYSTEM/...`. Leia como exemplo trabalhado e adapte os paths antes de usar em outro projeto.

## Contribuir

Não edite arquivos aqui: o próximo export sobrescreve. Abra uma issue.

## Licença

MIT, ver [LICENSE](LICENSE). Skills adaptadas de outros autores mantêm a atribuição no próprio arquivo, e `skills/diagram-build/` mantém a LICENSE dela.
