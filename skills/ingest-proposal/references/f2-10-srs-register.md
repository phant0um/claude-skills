---
name: f2-10-srs-register
kind: reference
type: skill
status: active
parent: "[ingest-proposal](../SKILL.md)"
created: 2026-10-10
updated: 2026-10-10
reviewed: 2026-10-11
reviewed-by: claude-sonnet-5-5
reviewed-scope: "Lido inteiro em 2026-10-11 (W3 do plano drift-reorg-skills). Wikilinks e paths citados conferidos no disco por script. Corrigido o ponteiro `ingest-proposal.md` (inexistente apos a reorg) para `SKILL.md`; F2.10 esta em SKILL.md:73. Tracker 07-QUEUE/kanban/trackers/srs-sources-tracker.md e workflows/rotinas/srs-sources.md existem. Script bash nao executado."
---

# F2.10 SRS register (reflect: true only, superseded)

Condição de uso: a source já chega com `reflect: true` na ingestão (raro). Volta ao procedimento principal em `SKILL.md`, passo 2 (F2.10).

Sob o modelo binário, o tracker é populado por **srs-sources FASE 0** (sync de `reflect: true` do manifest), não mais por Score A no ingest. Este passo só age se a source já chega com `reflect: true`. Mantido idempotente (append-only, dedup por slug) para não duplicar o que a FASE 0 já insere.

```bash
TRACKER="07-QUEUE/kanban/trackers/srs-sources-tracker.md"
mkdir -p 07-QUEUE/kanban/trackers
# header é criado uma vez; se ausente, semear
[ -f "$TRACKER" ] || printf '%s\n' \
  '| Slug | Categoria | Interest | Ingested | Ultima Revisão | Próxima Revisão | Intervalo | Nota | Sessões |' \
  '|------|-----------|----------|----------|----------------|-----------------|-----------|------|---------|' > "$TRACKER"

# por source reflect:true: intervalo inicial 7 dias
TODAY=$(date -I)
NEXT=$(date -I -v+7d 2>/dev/null || date -I -d "+7 days")
# evitar duplicata se slug já no tracker
grep -qF "| $SLUG |" "$TRACKER" || \
  echo "| $SLUG | $CATEGORIA | core | $TODAY | $TODAY | $NEXT | 7 |  | 0 |" >> "$TRACKER"
```

**Guardrail**: só `reflect: true` (approved sem a flag não entra). Append-only, dedup por slug (srs-sources FASE 0 é a fonte primária).
