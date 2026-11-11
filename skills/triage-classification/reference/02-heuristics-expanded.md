---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-02-heuristics-expanded
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 2 secoes, 107 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Expanded Heuristics for Large Batches (2026-06-22)](#expanded-heuristics-for-large-batches-2026-06-22)


> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: Expanded Heuristics for Large Batches.

## Expanded Heuristics for Large Batches (2026-06-22)

When scoring >50 files, the base regex set captures ~60% but misses vault-specific
topics. Add these patterns (applied in Python, not bash — bash regex becomes
unwieldy at this scale):

### Positive signals (vault-specific)

```python
# Loop engineering / autonomous loops (core obsession)
if re.search(r'loop engineering|autonomous loop|agent loop', title, re.I): score += 2
# Hermes / Telegram agents
if re.search(r'hermes|telegram.*agent', title, re.I): score += 1
# Agent design patterns / agent stack
if re.search(r'agent.*design.*pattern|agent.*stack|agent.*optimization', title, re.I): score += 2
# Self-improvement / RSI
if re.search(r'self-improv|recursive.*self|RSI', title, re.I): score += 2
# LLM theory / training
if re.search(r'diffusion|transformer|matmul|triton|kernel|LoRA|fine-tun', title, re.I): score += 2
# Trading / quant
if re.search(r'polymarket|trading.*agent|quant.*framework|markov.*trade', title, re.I): score += 2
# Multi-agent / safety research
if re.search(r'Co-Scientist|multi-agent|safety.*research|MosaicLeaks', title, re.I): score += 2
# Agent security / oversight
if re.search(r'OpenSigil|Oversight.*Layer.*Agent|information-flow.*IFC', title, re.I): score += 2
# Claude Code skills / cowork
if re.search(r'Claude Code Skills|REVIEWS.md|Memory.md', title, re.I): score += 2
# Codex / sandbox / Responses API
if re.search(r'Codex.*sandbox|Responses API.*agente|Codex.*Symphony', title, re.I): score += 1
# Ollama / local inference
if re.search(r'Ollama.*MLX|GGUF|OpenJarvis', title, re.I): score += 1
```

### Negative signals (clickbait / off-topic)

```python
# Clickbait marketing
if re.search(r'cheat code|millionaire|10.000.*month|(?-i:\b10X\b)|escape wage|mass replacement', title, re.I): score -= 3
# B2B / cold outreach
if re.search(r'cold email|cold outreach|B2B.*lead|qualify.*B2B', title, re.I): score -= 2
# Generic self-help
if re.search(r'open loops|elite clarity|happiness|social worker|healthier', title, re.I): score -= 2
# Off-topic VPN/proxy (Chinese)
if re.search(r'零成本|不花一分钱|VPS.*private.*node|安全拿回', title, re.I): score -= 3
# JetBrains release notes (low vault value)
if re.search(r'JetBrains|DBeaver.*release|DataGrip.*2026|PyCharm.*2026|CLion.*2026', title, re.I): score -= 1
# Beginner tutorials
if re.search(r'What Is Git.*Beginner|What Is OAuth.*Explained', title, re.I): score -= 2
# Enterprise case studies (low reuse)
if re.search(r'reimagining trade finance|insurance company.*data hub|regulation intensifies', title, re.I): score -= 2
```

### Python scoring > bash for large batches

For >50 files, use Python instead of bash — regex is cleaner, string ops are
richer, and the whole scoring loop runs in <5s. Save results to JSON for
downstream pipeline consumption:

```python
results = []
for f in candidates:
    score = score_file(f)  # score é insumo dos gates (§Decisão Binária), não decisão
    results.append({"file": f, "score": score})
results.sort(key=lambda x: x["score"], reverse=True)
```

### macOS `shuf` not available

`shuf` (GNU coreutils) doesn't exist on macOS. For random sampling:

```python
# Instead of: shuf -n 3 file.txt
python3 -c "import sys,random; random.seed(42); [print(l) for l in random.sample(sys.stdin.read().strip().split('\n'), 3)]"
```

### File Evaporation Selectivity (2026-06-22 observation)

In a 157-candidate batch, 64 files evaporated between scan and processing.
**All 64 were Score C/D or borderline B — zero Score A files were lost.**

Hypothesis: Readwise sync purges older/less-recently-accessed clippings first.
High-value clippings (recently clipped, frequently accessed) survive sync cycles.

**Implication for pipeline:** evaporation acts as a natural quality filter.
Don't fight it — treat evaporated C/D files as "auto-rejected by sync" and
focus energy on the A/B files that survived.

---

