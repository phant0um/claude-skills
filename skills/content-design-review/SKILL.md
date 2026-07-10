---
name: content-design-review
description: Validador estrito pareado ao content-design. Audita um texto contra as 5 regras (front-load, 1 ideia/frase, concreto, corte) e reprova com localização+fix por linha. Aplicar após redigir, antes de salvar.
trigger: ["revisa o texto", "esse doc tá bom?", "valida content design", "review da nota", "audita o resumo", "review this writing"]
---

<what-to-do>

Um domínio = skill que **gera** (content-design) + skill que **reprova** (esta). O agente não tem taste — regra explícita cataloga o erro típico e barra. Content-design molda; esta audita e devolve veredito acionável. Não reescreve — reporta.

## Quando usar

- Após redigir/editar qualquer texto persistido, antes de salvar.
- Companion de `content-design` — gera lá, valida aqui.
- NÃO usar em transcript cru nem captura de inbox.

## Erros típicos do agente (o que barrar)

| # | Erro | Sintoma detectável |
|---|------|--------------------|
| R1 | Aquecimento antes do ponto | Linha 1 = "Neste documento...", "Este artigo explora...", "Vamos ver..." |
| R2 | Veredito enterrado | Conclusão aparece no §3+, não na linha 1 |
| R3 | Frase multi-ideia | "e também", "além disso" carregando 2ª ideia na mesma frase |
| R4 | Abstração vaga | "uma gama de", "indo adiante", "de certa forma", "em termos de", "diversos aspectos" |
| R5 | Duplicata / filler | mesma ideia repetida em 2 parágrafos; frase sem conteúdo novo |

## Protocolo (bash-first, julgamento só onde precisa)

```bash
arquivo="$1"
# R1 — abertura de aquecimento
head -3 "$arquivo" | grep -niE "^(neste|nesta|este (artigo|documento|texto)|vamos (ver|explorar)|ao longo (deste|desta))" \
  && echo "R1 FAIL: abertura de aquecimento — cortar, começar do ponto"
# R4 — abstração vaga
grep -niE "uma gama de|indo adiante|de certa forma|em termos de|diversos aspectos|de alguma maneira" "$arquivo" \
  && echo "R4 WARN: vago — trocar por número/nome/data"
# R3 — frase multi-ideia (heurística)
grep -niE "\b(e também|além disso|ademais|bem como)\b" "$arquivo" \
  && echo "R3 WARN: possível 2ª ideia na frase — quebrar em duas"
```

**R2 (1 pergunta de julgamento):** "A linha 1 entrega a conclusão/veredito, ou é background?" — se background → FAIL, apontar qual parágrafo tem o ponto real p/ subir.

**R5 (opcional, doc >40 linhas):** "há parágrafo que repete ideia de outro?" → apontar par.

## Veredito

```
=== CONTENT-DESIGN-REVIEW | <arquivo> ===
R1 Abertura:      OK | FAIL: linha N aquecimento
R2 Front-load:    OK | FAIL: ponto real no §K, subir p/ linha 1
R3 1-ideia/frase: OK | WARN: linha N
R4 Concreto:      OK | WARN: linha N vago
R5 Sem duplicata: OK | WARN: §A ≈ §B | SKIP (<40 linhas)

VEREDITO: APROVADO | REVISAR (N ajustes) — [localização + fix por item]
```

- `APROVADO`: R1+R2 OK (WARN em R3/R4/R5 permitido).
- `REVISAR`: R1 ou R2 FAIL — veredito enterrado/aquecimento bloqueiam save.

## Exemplo

Input (`draft.md`):
> Neste relatório exploramos diversos aspectos da migração. A latência caiu.

Output:
```
R1 Abertura:   FAIL: linha 1 "Neste relatório exploramos" — aquecimento
R2 Front-load: FAIL: ponto real ("latência caiu") na linha 2, subir p/ linha 1
R4 Concreto:   WARN: linha 1 "diversos aspectos" — dar o número
VEREDITO: REVISAR (3) — abrir com "Latência caiu X→Y após migração"
```

## Restrições

- NUNCA reescrever o arquivo — só reportar localização + fix. Autor aplica.
- R1/R2 são FAIL (estruturais); R3/R4/R5 são WARN (estilo — julgamento pode divergir).

## Par gerador

**content-design** (skill irmã) — a que gera. Esta reprova. Ordem: content-design ao redigir → content-design-review antes de salvar.

</what-to-do>
