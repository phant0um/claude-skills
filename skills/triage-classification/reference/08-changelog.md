---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-08-changelog
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 1/1 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 1 secoes, 93 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---

> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: Changelog de versões.

## Changelog

- v2.5 (2026-07-12): +4 pitfalls do pipeline-semanal re-exec. (1) **Reporting terminology** — output
  deve usar approved/disapproved (BinEval v2.1), NUNCA A/B/C/D. `batch_score.py` ainda outputa
  grades em `/tmp/triagem_scores.txt` (legado) — orquestrador deve traduzir antes de reportar.
  (2) **FASE 3 report path** — `06-GENERATED/relatorios/` (report-agent), NÃO
  `06-GENERATED/ingest-report/` (agente core separado `@ingest-report`). (3) **adversarial_gate_v2.py
  hardcoded /tmp/ingest_results.json** — script lê arquivo stale do run anterior sem flag
  --batch-date. Fix: gerar `/tmp/ingest_results.json` fresco antes de rodar. (4) **Daily-scan
  phantom paths** — snapshot continha 77 paths de `.raw/articles/` inexistente. Evaporation
  guard dropou todos. Fix consumer-side: se 100% evaporation = bug produtor, flagar anomalia.
- v2.4 (2026-07-11): **Bugfix sistêmico regex-quoting** — 71 regras bash `[[ "$v" =~ "a|b" ]]` tinham alternação MORTA (RHS quotado → `|` vira literal, nunca casa múltiplas alternativas). Reescritas p/ idioma de variável `_re="a|b"; [[ $v =~ $_re ]]` (única forma que preserva alternação + espaços). Mesma raiz do misroute 62-finance (regra de domínio) e do junk `10X`. Validado: 71 lines `bash -n` OK, alternação confirmada. Backup em /tmp.
- v2.3 (2026-07-11): +Pitfall `10X` regex — sem `\b` word boundary, matchava "10x lower cost" em tech content legítimo. Fix: `\b10X\b` no batch_score.py. Run 2026-07-11: 296 candidatos, 7 falsos positivos corrigidos. +Self-improvement log posicionamento: movido para APÓS F2.10 (antes de FASE 3) no pipeline-semanal.md v6.1 — garante lessons.md mesmo se max_turns estourar. +Adversarial gate v2 script persistido em 04-SYSTEM/scripts/ (estava em /tmp/).
- v2.2 (2026-07-06): **Bugfix `fix_broken_links.py` create_stub()** — usava `name` (subpath
  inteiro "ai-agents/X") como filename → paths aninhados duplicados (`ai-agents/ai-agents/X.md`).
  Agora extrai `parts[-1]` e strip `.md` se presente. +Novo script `normalize_stubs.py` para
  normalizar stubs legados em paths errados (move p/ canônico, strip .md.md, deleta empty-name,
  merge em targets existentes). +Novo pitfall: F2.10 false-positive broken links — Obsidian
  resolve wikilinks curtos por basename matching, não exige path completo. Quality gate check
  deve simular basename resolution antes de flagar broken. Evidência: 103 "broken" → 101
  resolved by basename, 1 truly broken. Veredito correto: PIPELINE OK.
- v2.1 (2026-07-05): +fix_broken_links.py --create-stubs duplicated nested paths + .md.md
  extension pitfall — 202 stubs criados em paths estruturalmente errados (concepts/agent-systems/
  ai-agents/X.md.md). Orquestrador precisa normalizar paths pós-criação. Script precisa de
  fix no path construction logic.
- v2.0 (2026-07-05): +Programmatic ingest Tese Central extracts raw frontmatter pitfall —
  script de ingest programático extrai primeiros 500 chars incluindo YAML frontmatter
  do Clipping. Fix: strip_frontmatter() antes de extrair Tese. +fix_links.py (report-only)
  vs fix_broken_links.py (fix+stubs) distinction — fix_links.py não aplica correções,
  apenas reporta. Sempre usar fix_broken_links.py --create-stubs para repair.
  Evidência: pipeline-semanal 2026-07-05, 306 source pages, 272 links fixed, 202 stubs.
- v1.9 (2026-06-30): +Orphan rate varies by ingest method (programmatic 11% vs
  AI subagent ~100%) — "Orphan rate 100%" era incorreto para batch programático.
  +fix_links.py false positives pitfall — links válidos reportados como quebrados
  quando concept existe no path linkado mas script assume path flat. Run 2026-06-30
  run 3: 105 candidatos, 105 aprovados (63A+42B), 105 source pages programáticos em
  0.4s, 11% orphan rate, PIPELINE OK.
- v1.8 (2026-06-30): +F1.0b inline bash → f10b_scan.py migration. 5 false negatives
  por em-dash/CJK/nomes genéricos. pipeline-semanal.md patcheado para usar script
  Python ao invés de inline bash norm/slug/grep. Fixes: em-dash→hyphen, CJK basename
  fallback, generic names <15 chars sem slug partial match.
- v1.7 (2026-06-28): +Script↔SKILL.md drift pitfall — batch_score.py ainda tinha
  concept path mismatch (46/141 broken links, 32.6%) +manifest boolean values
  TypeError +self-improvement log wc -l padding macOS +batch_score.py hardcoded
  /tmp paths. 5 novos pitfalls de pipeline-semanal 2026-06-30 run 2 (150
  candidatos, 21 aprovados).
- v1.7 (2026-06-28): +Script↔SKILL.md drift pitfall — batch_score.py ainda tinha
  v1.7 script, SKILL.md now documents it). +Subagent wikilink path mismatch
  (32.6% broken links, fix_links.py script added). +/tmp/ hardcoded path pitfall.
  +Self-improvement log grep verification fails on macOS (wc -l padding).
  Run 2026-06-30: 23 candidatos → 21 aprovados (11A+10B), 1 Nexus bump (Stop
  Writing Prompts C→B), 46 links fixed programaticamente.
- v1.7 (2026-06-28): +Script↔SKILL.md drift pitfall — batch_score.py ainda tinha
  read hardcoded /tmp/ instead (39 vs 23 candidates). Fix: accept --candidates,
  stdin, or /tmp fallback. (2) Archive-before-bump: C/D moved to archive before
  Nexus Manual Override could bump. Fix: --move-cd opt-in, default off. (3)
  "Design Loops" not recognized as loop engineering synonym. Fix: TITLE_POSITIVE
  expanded with design loop|loops that make ai. Script patches applied same-session.
- v1.7 (2026-06-28): +Script↔SKILL.md drift pitfall — batch_score.py ainda tinha
  `sum(v for kw, v ...)` apesar de v1.5 documentar `count//3`. Fix aplicado ao
  script. Lição: quando documentar fix em SKILL.md, SEMPRE aplicar também ao
  scripts/. +Approval rate 93.4% justificado (Readwise-curated AI/agent batch).
  +Domain tagging (T5 plano-melhorias) — triagem agora atribui domínio.
- v1.6 (2026-06-24): +Subagent manifest update failure pitfall — subagentes podem
  + slug() inline syntax error + Approval rate calibration. Achados: pipeline-semanal
  2026-06-24, 141 candidatos, 89.4% approval (justificado — Readwise-curated).
- v1.5 (2026-06-23): +Rescore borderline inflation (sum→count//3) + Bash -c blocked
  + Categorização false-positive concurso + Inline python3 -c corruption.
  Achado: pipeline-semanal 2026-06-23 run 2, 237 candidates, 97% approval (inflado).
- v1.4 (2026-06-23): +macOS declare -A failure + candidates_aprovados corruption
  + Python two-pass rescoring. Achado: 57 candidates, 18 approved.
- v1.3 (2026-06-22): +Extended Title Patterns (50+ regex) + Python scoring > bash
  for >50 files. Achado: 157 candidatos.
- v1.2 (2026-06-16): +File Evaporation Pattern + Nexus Manual Override expandido.
  Achado: 248 candidatos, 100% já ingeridos.
- v1.1 (2026-06-16): +macOS Compatibility Pitfalls (grep -P, aula/curso extraction).
  Achado: pipeline-diario quebrou em grep -P no macOS.
- v1.0 (2026-05-23): criado a partir de análise post-hoc dos 108 arquivos triados
  manualmente em 2026-05-23. Padrões extraídos dos rejeitados vs. aprovados.

## Movido do corpo de SKILL.md (2026-10-11)
> **O pin anterior violava a HR1.** `claude-haiku-4-5` sobre conteúdo externo
> não-confiável é exatamente o que a regra proíbe — *"trocar Sonnet por outro
> modelo continua banido de override"*. Não era pin desatualizado: era pin contra
> a hard rule, sobrevivendo porque nenhum gate lia o corpo.
