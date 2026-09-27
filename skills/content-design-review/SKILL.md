---
name: content-design-review
description: "Use when: auditar artefato JÁ REDIGIDO contra as 5 regras de content-design (front-load, 1 ideia/frase, concreto, corte) antes de salvar ou commitar — devolve veredito com localização e fix por linha. NUNCA reescreve: valida e reprova. Escrever é `content-design`; voz é `voice-registers`."
trigger: ["revisa o texto", "esse doc tá bom?", "valida content design", "review da nota", "audita o resumo", "review this writing"]
---

<what-to-do>

Padrão emilkowalski/skills: um domínio = skill que **gera** (`content-design`) + skill que **reprova** (esta). Agente não tem taste — regra explícita cataloga o erro típico e barra. Content-design molda; content-design-review audita e devolve veredito acionável.

Rodar após redigir/editar qualquer artefato persistido, antes de salvar ou commitar.

</what-to-do>

<supporting-info>

## Quando NÃO usar

- **Texto ainda não redigido** — esta skill audita artefato existente; escrever é `content-design`.
- **Camada de voz** (tom, AI-slop, palavras-banidas) — `voice-registers` + `voice-lint.py`. Esta olha só estrutura.
- **Completeness de página de ingest** (frontmatter, wikilinks, tese) — `ingest-verify`. Ordem: esta (estrutura) → ingest-verify (completeness) → save.
- **Transcript cru** (`.raw/`) e **captura de inbox** — ficam crus até ingest.
- **Auditoria em massa de páginas antigas** — forward-only, só o artefato em edição.

## Erros típicos do agente (o que barrar)

| # | Erro | Sintoma detectável |
|---|------|--------------------|
| R1 | Aquecimento antes do ponto | Linha 1 = "Neste documento...", "Este artigo explora...", "Vamos ver..." |
| R2 | Veredito enterrado | Conclusão aparece no §3+, não na linha 1 |
| R3 | Frase multi-ideia | "e também", "além disso" carregando 2ª ideia na mesma frase |
| R4 | Abstração vaga | "uma gama de", "indo adiante", "de certa forma", "em termos de", "diversos aspectos" |
| R5 | Duplicata / filler | mesma ideia repetida em 2 parágrafos; frase sem conteúdo novo |

## Protocolo (bash-first, Haiku só p/ julgamento)

```bash
# R1 — abertura de aquecimento (zero tokens)
head -3 "$arquivo" | grep -niE "^(neste|nesta|este (artigo|documento|texto)|vamos (ver|explorar)|ao longo (deste|desta))" \
  && echo "R1 FAIL: abertura de aquecimento — cortar, começar do ponto"

# R4 — abstração vaga (zero tokens)
grep -niE "uma gama de|indo adiante|de certa forma|em termos de|diversos aspectos|de alguma maneira|no que diz respeito" "$arquivo" \
  && echo "R4 WARN: vago — trocar por número/nome/data"

# R3 — frase multi-ideia (heurística)
grep -niE "\b(e também|além disso|ademais|bem como)\b" "$arquivo" \
  && echo "R3 WARN: possível 2ª ideia na frase — quebrar em duas"
```

**R2 (Haiku, 1 pergunta):** "A linha 1 entrega a conclusão/veredito, ou é background?" — se background → FAIL, apontar qual parágrafo tem o ponto real p/ subir.

**R5 (Haiku, opcional):** só se doc >40 linhas — "há parágrafo que repete ideia de outro?" → apontar par.

## Veredito

```
=== CONTENT-DESIGN-REVIEW | <arquivo> ===
R1 Abertura:     OK | FAIL: linha N aquecimento
R2 Front-load:   OK | FAIL: ponto real no §K, subir p/ linha 1
R3 1-ideia/frase: OK | WARN: linha N
R4 Concreto:     OK | WARN: linha N vago
R5 Sem duplicata: OK | WARN: §A ≈ §B | SKIP (<40 linhas)

VEREDITO: APROVADO | REVISAR (N ajustes) — [localização + fix por item]
```

- `APROVADO`: R1+R2 OK (WARN em R3/R4/R5 permitido).
- `REVISAR`: R1 ou R2 FAIL — veredito enterrado/aquecimento bloqueiam save.

## Restrições

- **NUNCA reescrever o arquivo** — só reportar localização + fix sugerido (padrão review-skill: valida, não muta). Autor aplica. `writes: []` no contrato é literal.
- R1/R2 são FAIL (estruturais); R3/R4/R5 são WARN (estilo — julgamento pode divergir).
- Forward-only: não auditar páginas antigas em massa; só o artefato em edição.

## Liga a

- **content-design** (`content-design`) — a skill que gera; esta reprova. Par principle+review.
- **ingest-verify** C1–C11 — valida *presença/completeness*; esta valida *estrutura de leitura*. Ordem: content-design-review → ingest-verify → save.
- **voice-registers** — camada de voz, ortogonal a esta. Roda **depois** desta: estrutura primeiro, voz depois (voice-registers Procedimento passo 1). Abertura de aquecimento é R1 aqui e catálogo item 5 lá; reporte uma vez, como R1.
- **caveman** — comprime conversa; esta molda artefato salvo. Ortogonais.

</supporting-info>

## Completion

- [ ] Artefato alvo revisado contra todas as 5 regras de content-design.
- [ ] Cada violação citada com regra + trecho exato + correção sugerida.
- [ ] Veredito por regra (passa/falha) no relatório final.
- [ ] Arquivo alvo intocado — nenhuma escrita feita por esta skill.

## Failure modes

- **Reescrever o alvo**: aplicar o fix em vez de reportar → proibido; `writes: []` é literal, o autor aplica.
- **Severidade inflada**: tratar R3/R4/R5 como FAIL → só R1/R2 reprovam; os outros são WARN de estilo.
- **Auditoria em massa**: varrer páginas antigas → forward-only, só o artefato em edição.
- **Achado duplicado com voz**: abertura de aquecimento reportada aqui e no voice-registers → reporte uma vez, como R1.
