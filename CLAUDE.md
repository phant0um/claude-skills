# claude-skills — router

Skills genéricas p/ Claude Code. Este arquivo mapeia qual skill usa quando. Claude lê no boot; carrega a SKILL.md só quando o trigger casa.

## Regra de escopo (o que entra aqui)

Skill entra em `claude-skills` só se **serve fora do vault de origem**. Teste: "outra pessoa, em outro projeto, ganharia com isso?" Sim → entra. Acoplada a domínio (finança/concurso/agente específico) → fica privada.

## Mapa

### writing/ — escrita de artefato

| Skill | Trigger | Função |
|-------|---------|--------|
| content-design | ao salvar artefato | 5 regras front-load (pirâmide invertida, 1 ideia/frase, concreto) |
| content-design-review | após redigir, antes de salvar | Validador estrito pareado: audita as 5 regras, veredito por linha, não reescreve |
| writing-fragments | "@fragments", explorar material cru | Minerar fragmentos, sem estrutura ainda |
| writing-shape | "@shape", moldar rascunho | Material → artigo, parágrafo a parágrafo |
| writing-beats | "@beats", montar narrativa | Jornada de beats, cada termo fundamentado antes de usar |
| writing-great-skills | criar/revisar SKILL.md | Vocabulário + princípios p/ skill previsível |

### reasoning/ — deliberação, diagnóstico

| Skill | Trigger | Função |
|-------|---------|--------|
| council | "@council", decisão multi-dimensional | 5 advisors debatem + revisão cega → veredicto |
| debate | "@debate", trade-off arquitetural | Confronto formal 2 perspectivas + arbitragem |
| pre-mortem | "@pre-mortem", plano de alto risco | Prospective hindsight: "o plano já falhou, como?" |
| office-hours | "@office-hours", pressionar ideia | 6 forcing-questions estilo YC |
| grill-me | "grill me", antes de codar | Perguntas duras, uma por vez |
| doubt-driven-development | "@doubt", validar premissas | Enumera + classifica premissas por risco |
| diagnose | "diagnose", bug resistente | Loop disciplinado, fix só com hipótese confirmada |
| trace | "@trace", output inesperado de agente | Reverse-engineer qual parte do agent file causou |

### core/ — dev, meta, gates genéricos

_(vazio — migrar tdd/implement/code-optimize quando de-vaultadas)_

## Manutenção

- Nova skill genérica no vault → avaliar migração p/ cá (regra de escopo acima).
- Skill que ganha acoplamento a domínio → sai daqui, volta pro sistema-pai.
- Versionar: bump `plugin.json` version no merge (semver: feat=minor, fix=patch).
