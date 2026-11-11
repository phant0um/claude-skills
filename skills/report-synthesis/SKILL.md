---
kind: skill-proc
resolver-status: exposed
type: skill
name: report-synthesis
input:
  schema: 04-SYSTEM/system/rules/ingest/schema-report-packet-v2.json
  required_fields: [run_id, f1_receipt_path, f2_receipt_path]
output:
  schema: 04-SYSTEM/system/rules/ingest/schema-report-result-v2.json
  format: json
triggers:
  positive:
    - "sintetizar receipts"
    - "relatório F3"
    - "consolidar drain"
  negative:
    - "executar F1/F2"
    - "escrever hot.md"
allowed_effects:
  - write /tmp/pipeline-*.json
  - read 06-GENERATED/audits/pipeline-receipts/
  - read 03-RESOURCES/sources/
  - read 03-RESOURCES/concepts/
  - read 03-RESOURCES/entities/
forbidden_effects:
  - write hot.md
  - write manifest
  - write archive
  - call ledger
  - modify agent files
version: 2.0.0
source_agent: report-agent
status: active
created: 2026-08-20
description: "Use when: sintetizar receipts F1+F2 no relatório F3 do pipeline-drain — agregação JSON; fases vão para suas skills."
updated: 2026-10-24
reviewed: 2026-10-24
reviewed-by: claude-sonnet-5-5 (achados: shield claude-opus-5-5)
reviewed-scope: "Reescrita em 2026-10-24. Nao existe driver de F3 em scripts/; o contrato vivo e o workflow pipeline-drain/F3-relatorio.md, contra o qual a skill foi conferida (packet/result v2, limite de 3 itens por lista, evidence_refs, relatorio pipeline-drain-<data>.md, renderer pipeline-receipts.py). Removidos os passos que escreviam hot.md, register de contradicoes, kanban e chamavam audit-logging: contradiziam forbidden_effects e a regra de writer unico. Mantidos F3.1-F3.3 e o spot-check como metodo de analise. NAO conferido: references/ (templates-f3, meta-padroes, sintese-cruzada) e o reference-report-synthesis."
---

# report-synthesis — F3 (síntese semântica)

> **Contrato vivo:** F3-relatorio. Não há driver
> de F3 em `04-SYSTEM/scripts/`; o renderer determinístico é `pipeline-receipts.py render`. Se esta página divergir do
> workflow ou dos schemas, o workflow e os schemas valem.
> Procedimento histórico (escrevia `hot.md`, register e kanban): `git show 24cf4b348:04-SYSTEM/automation/skills/pipeline/report-synthesis/SKILL.md`.
>
> **Proveniência:** procedimento transplantado de `04-SYSTEM/agents/nexus-agent-system/report-agent.md` @ `b579a90cd` (S1, 2026-08-23); reescrito em 2026-10-24.

## Fronteira de autoridade

F3 é **adapter de análise**: recebe `schema-report-packet-v2.json` (receipts F1 e F2 verificados) e devolve
`schema-report-result-v2.json` com **só síntese semântica**. Quem escreve é o Nexus. Esta skill não escreve `hot.md`,
manifest, archive, `_contradiction-register.md` nem kanban, e não chama `audit-logging`. Contradição, impacto "alta" e
resultado vão como proposta no JSON; o Nexus materializa.

Contagens, métricas, distribuições e cobertura vêm do renderer, nunca do modelo.

## Perfil de modelo

`standard`: entrada é source page já materializada pela F2, não clipping cru. A HR1 é da F2
(model-routing · model-catalog §Perfis). Sem pin local por fase.

## Método

1. Ler os receipts do packet (F1 e F2). Receipt ausente: parar, não inventar.
2. **F3.1 por cluster:** resumo (2–3 frases), convergências (≥2 sources concordando), contradições (com citação),
   insights acionáveis, gaps. Agrupar por domínio, tópico central e tipo.
3. **F3.2 cross-connections:** conexões não óbvias entre clusters ou com o vault antigo; `wikilink` que resolve; razão em 1 linha.
4. **F3.3 vault impact:** priorizado, "alta" primeiro ([templates-f3](references/templates-f3.md)).
5. **F3.6** (≥3 sources): [meta-padroes](references/meta-padroes.md).
   **F3.8** (fechamento semanal): [sintese-cruzada](references/sintese-cruzada.md).
6. **F3.5 spot-check** de 3 source pages do run (tese central, informação preservada, wikilinks que resolvem).
   Falhou em ≥1: veredito `PIPELINE FAIL: <motivo>` no resumo; não bloqueie à espera do Nexus.

Menos de 2 sources no run: pule F3.1 e F3.2. Zero sources: sem síntese; declare no resumo.
O fire diário sem fechamento não roda F3: o relatório sai só com o núcleo v2 (ver workflow).

## Contrato do output

O JSON obedece `schema-report-result-v2.json`:

```json
{
  "schema_version": 2,
  "run_id": "{run_id}",
  "phase": "F3",
  "receipt_refs": [
    {"phase": "F1", "path": "{f1_receipt_path}", "record_digests": ["..."]},
    {"phase": "F2", "path": "{f2_receipt_path}", "record_digests": ["..."]}
  ],
  "semantic_synthesis": {
    "clusters": [{"text": "...", "evidence_refs": ["F1:item:N"]}],
    "cross_connections": [],
    "gaps": [],
    "implications": []
  }
}
```

Regras de síntese semântica: `clusters`, `cross_connections`, `gaps` e `implications` têm max 3 itens cada, de 1 a 3 `evidence_refs` (`F1:item:N`, `F2:item:N`). Afirmação sem receipt é invenção.
`unknown` continua `unknown`: não vira zero nem PASS.

Relatório do fire (escrito pelo Nexus): `06-GENERATED/ingest-report/pipeline-drain-<data>.md`. Projeções de máquina:
`pipeline-F1-<data>.md` e `pipeline-F2-<data>.md`.

## Quando NÃO usar

- Executar F1 ou F2 → `triage-classification` / `ingest-proposal`.
- Escrever `hot.md`, state, register ou kanban → Nexus.

## Failure modes

- Listar source por source, sem cruzar: relatório vira ruído.
- Convergência apoiada em uma source só.
- Tabela de impacto sem prioridade.
- Copiar contagens ou métricas para o output do modelo.
- Mais de 3 itens por lista (truncar) ou item sem `evidence_refs`.

## Referências

[reference-report-synthesis](reference-report-synthesis.md) ·
report-reference (histórico do report-agent).
