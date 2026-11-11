---
origin: native
type: skill
status: active
version: "1.0.0"
kind: skill-proc
resolver-status: exposed
name: prompt-review
description: "Use when: revisar e melhorar um prompt para Claude (clareza, estrutura, exemplos). Documento que agente consome (SKILL.md, CLAUDE.md, policy) é writing-for-agents."
updated: 2026-11-10
disable-model-invocation: true
---

# Prompt Review

Avaliar o prompt e reescrever uma versão melhor. Seja direto e construtivo.

Fonte das regras: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
(Anthropic, lida em 2026-09-28). A página tem um guia por modelo. Se o prompt
mira um modelo específico, cheque o guia desse modelo antes de recomendar
ajuste de verbosidade, effort ou progress updates.

## Primeiro: classificar o alvo

- **Turno de chat** (pedido avulso): revisão leve. Cobrir só Task, Output e
  Ação vs sugestão. O modelo infere o resto.
- **Prompt persistido** (system prompt, agente, skill, CLAUDE.md, template de
  API): checklist completa. Aqui o custo de um prompt ruim se repete a cada
  execução.

## Checklist

1. **Task.** Claude sabe exatamente o que produzir? Teste do colega: alguém sem
   contexto conseguiria seguir o prompt?
2. **Input.** As informações necessárias estão presentes (tom, audiência,
   formato)?
3. **Output.** O formato esperado está especificado (markdown, JSON, prosa,
   tamanho)? A ordem dos passos está numerada quando importa?
4. **Motivação.** Cada regra traz o porquê? "NEVER use ellipses" rende menos
   que "o texto vai para TTS, que não pronuncia reticências". O modelo
   generaliza a partir da explicação.
5. **Instrução positiva.** O prompt diz o que fazer, não só o que evitar?
   Troque "não use markdown" por "escreva em parágrafos de prosa".
6. **Ênfase calibrada.** Há `CRITICAL`, `MUST`, `IMPORTANT` ou caixa alta?
   Em modelos recentes isso causa overtrigger. Troque por linguagem normal
   ("Use esta tool quando..."). Remova "se em dúvida, use X".
7. **Ação vs sugestão.** Se o autor quer mudança feita, o verbo é imperativo
   ("Mude esta função")? "Pode sugerir mudanças?" gera só sugestão.
8. **Estrutura.** Instruções, contexto, exemplos e input variável estão
   separados por tags XML consistentes (`<instructions>`, `<context>`,
   `<example>`)? Em contexto longo, os documentos vêm no topo e a pergunta
   no fim?
9. **Exemplos.** Few-shot é necessário? Se houver, são 3–5, relevantes,
   diversos e dentro de `<example>`? Exemplos parecidos demais viram padrão
   copiado.
10. **Estilo espelhado.** O estilo do prompt combina com o estilo desejado da
    saída? Prompt cheio de bullets tende a gerar saída cheia de bullets.
11. **Escopo e autonomia** (prompts agênticos). O prompt limita overengineering
    (arquivos extras, abstrações não pedidas)? Diz quais ações exigem
    confirmação (destrutivas, irreversíveis, visíveis a terceiros)? Diz quando
    usar subagentes e quando trabalhar direto?
12. **Grounding** (prompts agênticos). O prompt manda ler o arquivo antes de
    afirmar algo sobre ele? Manda resolver o problema em geral, não só passar
    no teste?
13. **Critério de sucesso.** Como saber que o resultado está correto?
14. **Contexto e memória.** O prompt inclui estado atual e decisões anteriores?
    Precisa carregar algo de sessões anteriores?

## Regras de avaliação

- Instrução imperativa ("Escreva...", "Liste...") rende mais que pergunta
  ("Você pode...?").
- Termos vagos ("bom", "detalhado", "profissional") devem virar critérios
  concretos.
- Cada palavra deve carregar peso. Corte filler.
- Se o prompt tenta fazer muita coisa, sugira dividir em etapas encadeadas
  (rascunho, revisão contra critérios, refinamento).
- Não adicione bloco de exemplo do doc só porque existe. Adicione só o que
  resolve um problema observado no prompt.

## Output Format

```
## Análise

Alvo: [turno de chat | prompt persistido]

### O que funciona
[Pontos fortes, específicos]

### Problemas
[Cada issue com o item da checklist e o porquê de prejudicar]

### Versão melhorada
[Prompt reescrito, pronto para usar]
```

## Constraints

- Aponte problemas reais. Não seja só elogioso.
- Explique o que mudou e por quê em toda reescrita.
- Não adicione complexidade que o prompt original não precisa.
- Se o prompt já está sólido, diga isso e foque em 1–2 refinamentos.
- Responda em PT-BR quando o usuário escreve em português.

## Linhagem

- **Upstream:** original (vault-michel).
- **Original (vault):** review de prompt por boas práticas de prompt engineering.
- **2026-09-28:** checklist alinhada ao guia oficial da Anthropic (itens 4–12
  e classificação de alvo).
- **Critério:** mecanismo > autor. Fonte rastreável, não privilegiada.
