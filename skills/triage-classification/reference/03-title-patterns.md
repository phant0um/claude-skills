---
status: active
parent: "[triage-scoring](../triage-scoring.md)"
kind: reference
name: triage-scoring-03-title-patterns
type: skill-reference
updated: 2026-07-16
reviewed-scope: "checagem mecanica + semantica: 2/2 wikilinks resolvem; 0/0 paths citados existem; 0 par modelo-effort invalido; drift semantico 0 (regras 1-6 R12); kind=reference, 2 secoes, 114 linhas"
reviewed-by: R12 (mimo-v2.6-pro lotes 1-5, claude-haiku lotes 6-12, varredura claude-opus-5-5)
reviewed: 2026-10-04
---
## Contents

- [Extended Title Patterns (2026-06-22 batch, 157 candidates)](#extended-title-patterns-2026-06-22-batch-157-candidates)


> Seção fatiada de [triage-scoring](../triage-scoring.md). Carregar sob demanda: Extended Title Patterns (2026-06-22).

## Extended Title Patterns (2026-06-22 batch, 157 candidates)

The base rules above cover ~60% of cases. For large weekly batches (100+),
extend with these domain-specific patterns discovered in pipeline-semanal runs:

### POSITIVE — AI Agent / Loop Engineering (+1 to +3)

```bash
_re1="loop engineering|autonomous loop|agent loop"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="hermes|telegram.*agent"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="agent.*design.*pattern|agent.*stack|agent.*optimization"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="skill.*steroid|skill.*claude|skill.*pydantic"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="self-improv|recursive.*self|RSI"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="agent.*oversight|oversight.*layer|OpenSigil"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="information-flow|IFC.*agent|secure.*autonomous"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="agent.*rereading|world model.*agent"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="agentic.*resource.*discovery"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="subagents.*web search|subagent.*claude code"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="benchmarking.*open.*model|agentic.*enough"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="REVIEWS.md|Memory.md.*code review"; [[ $title =~ $_re1 ]] && ((score+=2))
```

### POSITIVE — LLM Theory / Training (+1 to +3)

```bash
_re1="diffusion|transformer|matmul|triton|kernel|LoRA|fine-tun"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="sparser|sparse.*inference|TwELL"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="Doc-to-LoRA|Text-to-LoRA|instant.*LLM"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="Natural Language.*Autoencoder|Trinity.*Coordinator"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="positional.*embedding|extending.*context.*dropping"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="String Seed.*Thought|distribution-faithful"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="GGUF|MLX.*Apple Silicon|Ollama.*performance"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="decentralized.*inference"; [[ $title =~ $_re1 ]] && ((score+=1))
```

### POSITIVE — Financial / Trading Agents (+1 to +3)

```bash
_re1="polymarket|trading.*agent|quant.*framework|markov.*trade"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="IC3.*paper|on-chain.*trading|autonomous.*trading"; [[ $title =~ $_re1 ]] && ((score+=1))
```

### POSITIVE — Hermes / Vault-relevant (+2 to +3)

```bash
_re1="Hindsight.*Memory.*Provider|Hermes.*Flightplan"; [[ $title =~ $_re1 ]] && ((score+=3))
_re1="Hermes.*Telegram|Hermes.*agent"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="Claude Code Skills|system prompt layer|senior engineer"; [[ $title =~ $_re1 ]] && ((score+=2))
_re1="How to Build.*Claude Skill|build.*claude.*skill"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="agent.*decides.*where|tools.*actually.*run"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="durable asset.*loop.*own|OpenEnv.*protocol"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="first AI loop.*for yourself"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="Teaching Claude.*why"; [[ $title =~ $_re1 ]] && ((score+=1))
_re1="token.*theft|supply chain.*npm"; [[ $title =~ $_re1 ]] && ((score+=1))
```

### NEGATIVE — Clickbait / Marketing / Off-topic (-1 to -4)

```bash
# NB: RHS de [[ =~ ]] sem aspas (aspas → | vira literal). \b10X\b case-sensitive (bash regex default).
[[ $title =~ cheat\ code|millionaire|10.000.*month|\b10X\b|escape\ wage|mass\ replacement ]] && ((score-=3))
[[ $title =~ cold\ email|cold\ outreach|B2B.*lead|qualify.*B2B ]] && ((score-=2))
_re1="social worker|healthier|happiness"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="writer.*\\\$10|writing.*income|faster.*master.*5.*skill"; [[ $title =~ $_re1 ]] && ((score-=3))
_re1="content.*overrated|SaaS.*marketing"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="money does buy|tribute system|new world order"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="open loops|elite clarity"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="149-person|rise of.*company"; [[ $title =~ $_re1 ]] && ((score-=1))
_re1="AI needs more than intelligence.*needs humanity"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="AI amplifies creativity"; [[ $title =~ $_re1 ]] && ((score-=1))
_re1="How.*survive AI|YOU ARE NOT USING.*TRAINING"; [[ $title =~ $_re1 ]] && ((score-=3))
_re1="VPS.*private.*node|零成本|不花一分钱"; [[ $title =~ $_re1 ]] && ((score-=3))
_re1="What Is Git.*Beginner|What Is OAuth.*Explained"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="reimagining trade finance|collaborative proof"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="insurance company.*data hub|secure data hub"; [[ $title =~ $_re1 ]] && ((score-=2))
_re1="Frontier Transformation"; _re2="agent|AI.*agent"; [[ $title =~ $_re1 ]] && ! [[ $title =~ $_re2 ]] && ((score-=1))
```

### NEGATIVE — IDE Release Notes (low vault value)

```bash
_re1="JetBrains|DBeaver|DataGrip|PyCharm|CLion|YouTrack|Mellum"; [[ $title =~ $_re1 ]] && ((score-=1))
# Only bump back up if the IDE article is specifically about agent integration:
_re1="JetBrains Central|sistema aberto.*agentes"; [[ $title =~ $_re1 ]] && ((score+=1))
```

### Pitfall: Heurística não conta multi-match do mesmo domínio

A skill v1.2 já documenta isso no Nexus Manual Override, mas vale reforçar:
artigos sobre "loop engineering" podem matchar só uma vez ("loop") e pontuar 4-6
quando deveriam ser Score A. **Solução**: para core obsessions do vault
(agent loops, Hermes, Claude Skills, LLM training), aplicar bump manual de +2
após scoring automatizado se o título claramente cobre o domínio.

---

