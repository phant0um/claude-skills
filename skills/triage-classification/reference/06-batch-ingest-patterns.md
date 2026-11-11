---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-06-batch-ingest-patterns
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 5/5 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 11 secoes, 234 linhas; drift R12: 2 achados resolvidos (A/B/F)"
reviewed-by: R13 (claude-sonnet; drift R12 corrigido)
reviewed: 2026-10-04
---
## Contents

- [Batch ingest programático (zero AI calls) — 2026-06-28](#batch-ingest-programático-zero-ai-calls-2026-06-28)
- [SKILL.md vs scripts/ synchronization rule](#skillmd-vs-scripts-synchronization-rule)
- [Pitfall: Archive-before-bump (2026-06-30)](#pitfall-archive-before-bump-2026-06-30)
- [Pitfall: Subagent wikilink path mismatch (2026-06-30)](#pitfall-subagent-wikilink-path-mismatch-2026-06-30)
- [Pitfall: batch_score.py /tmp/ hardcoded path (2026-06-30)](#pitfall-batch_scorepy-tmp-hardcoded-path-2026-06-30)
- [Pitfall: Self-improvement log grep verification fails on macOS (2026-06-30)](#pitfall-self-improvement-log-grep-verification-fails-on-macos-2026-06-30)
- [Pitfall: Reporting output must use binário terminology (approved/disapproved), not A/B/C/D — 2026-07-12](#pitfall-reporting-output-must-use-binário-terminology-approveddisapproved-not-abcd-2026-07-12)
- [Pitfall: Pipeline FASE 3 report path is 06-GENERATED/relatorios/, NOT 06-GENERATED/ingest-report/ — 2026-07-12](#pitfall-pipeline-fase-3-report-path-is-06-generatedrelatorios-not-06-generatedingest-report-2026-07-12)
- [Pitfall: adversarial_gate_v2.py reads hardcoded /tmp/ingest_results.json — 2026-07-12](#pitfall-adversarial_gate_v2py-reads-hardcoded-tmpingest_resultsjson-2026-07-12)
- [Pitfall: Daily-scan producer writes phantom paths to candidates_new.txt — 2026-07-12](#pitfall-daily-scan-producer-writes-phantom-paths-to-candidates_newtxt-2026-07-12)


> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: Batch ingest programático, SKILL.md vs scripts, phantom paths.

## Batch ingest programático (zero AI calls) — 2026-06-28

**Padrão**: para batches massivos (>100 files), `execute_code` Python é mais
eficiente que dispatch de subagentes paralelos. Processa 722 files em 1.2s
vs 5 subagentes que processariam ~5 files cada.

**Tradeoff**: batch programático cria source pages com tese central, seções,
wikilinks, mas F2.9 Minha Síntese fica como placeholder ("A ser analisado em
revisão manual"). F2.5 Concept Absorption não é feita (concepts linkados mas
sem evidência appended). Quality vem em passes posteriores (connection-finder,
revisão manual seletiva).

**Quando usar**:
- Batch >100 files onde scoring já foi feito (triagem complete)
- Source pages precisam ser criadas rapidamente (manifest update, archive move)
- Zero AI budget para ingest (apenas triagem)

**Quando NÃO usar**:
- Batch <20 files (subagentes com AI geram quality completa: F2.5+F2.9)
- Score A files que merecem reflection real (usar subagente com AI)
- Concept absorption é obrigatória no mesmo run

**Dívida técnica esperada**:
- F2.9 placeholders: ~70% das Score A pages terão placeholder
- Orphan rate varia por método: AI subagent ingest ~100% orphans (concepts
  não backlinkam); programmatic ingest (execute_code) ~11% orphans (105 sources,
  11/105 sem backlinks) — o script Python linka concepts existentes via keyword
  matching durante criação, gerando backlinks nativos. Connection-finder só
  preciso para orphans residuais.
- F2.5 pendente: concepts linkados sem evidência appended

---

## SKILL.md vs scripts/ synchronization rule

**Regra durável**: quando documentar um fix em SKILL.md, SEMPRE aplicar também
ao `scripts/` correspondente. SKILL.md é a especificação; scripts/ é a
implementação. Se divergirem, a skill documenta comportamento que o script
não reproduz.

**Check**: após patch de SKILL.md, `grep` no script pelo padrão antigo para
confirmar que não existe mais. Validar output do script contra um batch
conhecido antes de confiar.

---

## Pitfall: Archive-before-bump (2026-06-30)

**Sintoma**: `batch_score.py` auto-moved "Stop Writing Prompts. Design Loops That
Make AI Iterate Until It's Right." to `08-ARCHIVE/C/2026-06-30/` before Nexus
Manual Override could bump it C→B. Had to `mv` back from archive and re-approve.

**Causa**: Script had `shutil.move()` for C/D files inside `main()` running by
default. Nexus Manual Override (§ "Nexus Manual Override" above) happens AFTER
scoring, so any C file that should be bumped is already in archive.

**Fix aplicado**: C/D archive move disabled by default in `batch_score.py`. <!-- drift:ok: batch_score.py removido; registro histórico (R13) -->
Use `--move-cd` flag to re-enable auto-archive. Orchestrator should move C/D
AFTER Nexus Manual Override review.

**Prevenção**: sempre rodar `batch_score.py` sem `--move-cd`. Após Nexus Manual
Override (bumps aplicados), orchestrator move C/D restantes para archive.

## Pitfall: Subagent wikilink path mismatch (2026-06-30)

**Sintoma**: 46/141 wikilinks quebrados (32.6%) em 21 source pages criadas por
3 subagentes paralelos. Subagentes criaram concepts em `concepts/agent-systems/X.md`
e `concepts/agent-systems/X.md` mas linkaram como `X`
(sem subdiretório) nas source pages.

**Causa**: Subagentes recebem instrução de linkar `X` mas o vault
organiza concepts em subdiretórios (`ai-agents/`, `agent-systems/`, etc.).
Subagentes não conhecem a estrutura de subdiretórios e usam path flat.

**Fix programático**: Após ingest batch, rodar `scripts/fix_links.py` que: <!-- drift:ok: fix_links.py removido; registro histórico (R13) -->
1. Indexa todos concepts/entities recursivamente
2. Para cada link quebrado `X`, busca X em subdiretórios
3. Se encontra, reescreve link para `X`
4. Se não encontra, cria stub (concept ou entity mínimo)

**Prevenção**: instruir subagentes a usar path completo `X`
quando criar concepts. Mas mesmo com instrução, subagentes erram ~30% das vezes
— sempre rodar fix_links.py como passo pós-ingest obrigatório.

Ver `scripts/fix_links.py` para o script reusável.

## Pitfall: batch_score.py /tmp/ hardcoded path (2026-06-30)

**Sintoma**: Primeira execução leu 39 candidatos em vez de 23. O script tem
`--candidates` flag mas o default é `/tmp/candidates_new.txt` (hardcoded).

**Causa**: Pipeline escreve `06-GENERATED/tasks/candidates_new.txt` mas o script
lê `/tmp/candidates_new.txt`. Se /tmp/ tem dados de run anterior, conta errada.

**Fix**: Sempre copiar antes de rodar: `cp 06-GENERATED/tasks/candidates_new.txt
/tmp/candidates_new.txt`. Ou usar `--candidates 06-GENERATED/tasks/candidates_new.txt`.

## Pitfall: Self-improvement log grep verification fails on macOS (2026-06-30)

**Sintoma**: `grep -q "pipeline-semanal.*$(date -I)" lessons.md` retorna NO MATCH
mesmo quando a entrada foi appending corretamente.

**Causa**: `wc -l < file` no macOS (BSD) gera espaços de padding à esquerda
(ex: `       0`). O echo injeta esses espaços na linha, e o regex `pipeline-semanal.*2026-06-30`
não matcha porque os espaços extras entre "0 aprovados" e a data quebram o pattern.

**Fix**: Usar `tr -d ' '` no wc: `$(wc -l < file | tr -d ' ')`. Ou verificar com
fixed-string: `grep -qF "pipeline-semanal] 0 candidatos" lessons.md`.

## Pitfall: Reporting output must use binário terminology (approved/disapproved), not A/B/C/D — 2026-07-12

**Sintoma**: Pipeline reportou "70 aprovados (42A + 28B)" ao usuário e no hot.md. O usuário
corrigiu: FASE 1 não faz valoração em A/B/C/D desde v6.0 (BinEval). O score 0-10 e as
grades A/B/C/D do `batch_score.py` são **insumo interno dos gates**, não veredito.

**Causa**: `batch_score.py` ainda outputa `|A|` e `|B|` em `/tmp/triagem_scores.txt`
(legado). O orquestrador propagou essas grades para a triagem page e hot.md sem traduzir
para binário.

**Fix**: Toda comunicação externa (triagem page, hot.md, relatório, user-facing) DEVE usar
`approved`/`disapproved`. Se `batch_score.py` outputa grades, traduzir antes de reportar:
- A+B → `approved`
- C+D → `disapproved`
O arquivo `/tmp/triagem_scores.txt` com grades é interno — nunca aparece em artefatos vault.

**Prevenção**: após gerar triagem page e hot.md, grep por `|A|` ou `|B|` ou `grade` — se
encontrar, o output está usando terminology legada e precisa ser corrigido.

## Pitfall: Pipeline FASE 3 report path is 06-GENERATED/relatorios/, NOT 06-GENERATED/ingest-report/ — 2026-07-12

**Sintoma**: Subagente de relatório (FASE 3) salvou em `06-GENERATED/ingest-report/` em vez
de `06-GENERATED/relatorios/`. O usuário corrigiu: "não tem mais o ingest-report/relatorio".

**Causa**: `ingest-report` é um **agente core separado** (síntese semanal de sexta-feira,
`output_path: 06-GENERATED/ingest-report/`). O pipeline-semanal FASE 3 usa o `report-agent`
(nexus-agent-system), cujo output canônico é `06-GENERATED/relatorios/YYYY-MM-DD-relatorio-semanal.md`.
Conflito de nomes entre dois agentes diferentes com paths diferentes.

**Fix**: Pipeline FASE 3 reports vão para `06-GENERATED/relatorios/`. O path
`06-GENERATED/ingest-report/` é exclusivo do agente `@ingest-report` (síntese semanal
manual/scheduler sexta). Wikilinks no hot.md devem apontar para `...`.

**Prevenção**: ao despachar subagente de relatório FASE 3, especificar explicitamente:
"Save to 06-GENERATED/relatorios/YYYY-MM-DD-relatorio-semanal.md" no goal.

## Pitfall: adversarial_gate_v2.py reads hardcoded /tmp/ingest_results.json — 2026-07-12

**Sintoma**: F2.10 adversarial gate v2 rodou sobre o batch de 2026-07-11 (296 pages) em
vez do batch atual 2026-07-12 (70 pages). Veredito era inválido para o batch atual.

**Causa**: `04-SYSTEM/scripts/adversarial_gate_v2.py` lê hardcoded `/tmp/ingest_results.json`
sem flag `--batch-date` funcional. O arquivo continha dados do run anterior.

**Fix**: Antes de rodar `adversarial_gate_v2.py`, gerar `/tmp/ingest_results.json` fresco
para o batch atual:
```python
import json
results = []
for page_path in new_source_pages:
    content = (vault / page_path).read_text()[:1000]
    interest = "core"  # or parse from frontmatter
    results.append({"page": page_path, "interest": interest, "category": "ai-agents" if "ai-agents" in content else "articles"})
json.dump({"results": results, "batch_date": today}, open("/tmp/ingest_results.json", "w"), indent=2)
```
Depois rodar `python3 04-SYSTEM/scripts/adversarial_gate_v2.py`.

**Prevenção**: sempre verificar o `Batch YYYY-MM-DD` no output do script. Se a data não
bate com hoje, o `/tmp/ingest_results.json` é stale.

## Pitfall: Daily-scan producer writes phantom paths to candidates_new.txt — 2026-07-12

**Sintoma**: Pipeline-semanal F1.0 carrega `candidates_new.txt` (producido pelo
`daily-scan`). Evaporation guard dropou TODOS os 77 paths — nenhum existe no disco.
Recovery scan foi forçado, rerodando F1.0b completo desnecessariamente.

**Causa**: O `daily-scan` (produtor) escaneia diretórios que podem não existir no ambiente
atual. Neste caso, `.raw/articles/` foi removido/movido em run anterior, mas o `daily-scan`
ainda grava paths como `.raw/articles/X.md` no snapshot. O `f10b_scan.py` não valida
`[ -f "$f" ]` antes de escrever o path no arquivo de output.

**Diagnóstico**:
```bash
MISSING=0
while IFS= read -r f; do
  [ -f "$f" ] || MISSING=$((MISSING+1))
done < 06-GENERATED/tasks/candidates_new.txt
echo "Phantom paths: $MISSING / $(wc -l < 06-GENERATED/tasks/candidates_new.txt)"
# Se MISSING > 50% do total, o snapshot é unreliable — force recovery
```

**Fix (producer-side)**: `daily-scan` deve validar `[ -f "$f" ]` antes de escrever cada
path no snapshot. Paths inexistentes não devem entrar no arquivo. Alternativa: o
`f10b_scan.py` deve fazer `os.path.exists()` check antes de append ao output.

**Fix (consumer-side)**: O evaporation guard no pipeline-semanal F1.0b já dropa paths
inexistentes — isto é correto. Mas quando 100% dos paths são phantoms, o pipeline deve
logar isto como anomalia (não como normal evaporation) e flagar o `daily-scan` como bugado.

**Diferenciação**: evaporation normal = arquivos somem DEPOIS do scan (Readwise sync,
iCloud). Phantom paths = arquivos NUNCA existiram no momento do scan (diretório escaneado
não existe). Evaporation guard não distingue os dois — ambos são dropados silenciosamente.
Phantom paths indicam bug no produtor, evaporation indica race condition benigno.

**Evidência**: pipeline-semanal 2026-07-12, 77 paths no snapshot do daily-scan, todos
referenciando `.raw/articles/` (diretório inexistente). Recovery scan encontrou 126 files
reais em `.raw/` + `00-INBOX/clippings/`, 71 genuinely new.

