# Crisis Rehearsal Engine — 用群体智能把危机先演一遍

> **English TL;DR** — We run pre-mortems for reputation crises: feed 72 hours of pre-crisis public information into an open-source swarm-simulation engine (MiroFish), let hundreds of persona agents (media, retail investors, regulators, short sellers, competitors) react on a simulated social platform, then score the resulting forecast against what actually happened. In a backtest of 30 real, publicly documented Chinese corporate crises, the top-3 predicted risk types matched reality **83%** of the time (n=30, single run per event). Code, event library, and scoring protocol are open (AGPL-3.0). We sell rehearsal reports, not software.

**中文一句话**：用开源群体智能引擎做「危机预演」——只喂事发前 72 小时的公开信息，让几百个带人格的 Agent 先演一遍，再用真实结局回测。30 个真实历史危机事件，Top-3 风险命中率 **83%**。代码、事件库、评分协议全部开源（AGPL-3.0），我们卖的是预演报告与复演会。

---

## Why

A reputation crisis is irreversible once it starts: the first 24 hours are written into public memory, and most companies only buy **monitoring** — after the fact. The budget they already spend is on **crisis response** (in one documented public tender: ¥65k/year for "public-opinion monitoring" vs **¥429.5k per crisis** for "crisis PR"). We sell the rehearsal that happens *before* the crisis.

## What we built

1. **Pre-crisis information pack** — only what was publicly available 72h before the event (no hindsight).
2. **Local knowledge graph** — we replaced MiroFish's Zep Cloud dependency with a local JSON graph adapter (1 file, ~400 lines), so the whole pipeline runs without any cloud graph service.
3. **Swarm simulation** — 7–12 persona agents per event on a simulated Twitter/Reddit, 2 rounds, driven by DeepSeek (or any OpenAI-compatible model).
4. **Native report generation** — MiroFish's ReportAgent produces an 8k-character structured rehearsal report per event.
5. **Scoring** — an LLM judge compares the report's top-3 risks with the real outcome (event library contains ground truth), and we report hit rate + early-warning quality.

## Backtest results (30 events)

| Metric | Result |
|---|---|
| Events | 30 publicly documented Chinese corporate crises (2018–2026) |
| **Top-3 risk hit rate** | **83%** (mean 2.48/3) |
| Full 3/3 hits | 9 events |
| Zero hits | 0 events |
| Early-warning quality | 77/100 |
| Cost per event | ~$0.03 (DeepSeek API) |
| Time per event | ~4 minutes (graph → personas → 2-round simulation → report) |

**Honest limitations** (please read before quoting the number):
- Single run per event; the engine is stochastic, so the figure is directional, not a stable benchmark.
- Scoring is LLM-judged; we are calibrating it with human spot checks.
- 30 events is a small sample (±17pp at 95% CI). A 100+ event, 3–5 runs-per-event benchmark is the next milestone.
- Failures are included in the repo (`data/failures.md`) — we do not hide negative cases.

## Quick start

```bash
# 1. Clone
git clone https://github.com/yepinggu66/crisis-rehearsal && cd crisis-rehearsal

# 2. Install MiroFish (upstream, AGPL-3.0)
git clone https://github.com/666ghj/MiroFish
cd MiroFish && npm run setup:all && cp .env.example .env

# 3. Apply the local graph adapter (no Zep Cloud required)
cp ../patches/zep_local.py backend/app/utils/
# then apply the 7-line change to backend/app/utils/zep.py (see docs/patches.md)

# 4. Configure an OpenAI-compatible LLM in .env
LLM_API_KEY=sk-your-key-here   # DeepSeek / OpenAI / Qwen / local llama.cpp all work
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL_NAME=deepseek-chat
ZEP_LOCAL=1

# 5. Run the backtest
python scripts/backtest_runner.py --events data/events.csv --materials data/seeds --out output --limit 5
```

## Repository layout

```
data/events.csv        # 30 public crisis events with sources + outcomes
data/seeds/{id}.md     # pre-crisis (T-72h) information packs used as simulation seeds
patches/zep_local.py   # local Zep replacement (the key enabler)
scripts/backtest_runner.py  # headless pipeline: graph → simulation → report
scripts/score.py       # LLM judge with fixed protocol
docs/methodology.md    # hit definitions, information-clean-room rules, scoring protocol
docs/reports/{id}.md   # generated rehearsal reports (8k chars each)
data/failures.md       # events where we missed — with post-mortem notes
```

## License & commercial boundary

- **Code**: AGPL-3.0 (same as upstream MiroFish). You can run it, modify it, and offer it as a service — but if you modify and serve it, you must publish your source.
- **What we keep closed**: industry ontology (agent persona rules), client corpora, delivery playbooks. We sell **rehearsal reports and workshops**, not the engine.
- **No client data in this repo.** All events are public news; seeds are written by us from public sources only.

## Who it is for

- **PR / IR agencies** that want a white-label rehearsal engine (an alternative to enterprise suites from the big holding groups).
- **Listed companies and funds** that face reputation risk and want to rehearse before it happens.
- **Cross-border brands** (Chinese brands going global): we rehearse the two-way spillover between domestic and overseas opinion.

## Contact

Open an issue, or reach us at **yepinggu@outlook.com**. We can run a free 30-minute rehearsal of one real past event for your team.\n\nMaintainer: [@PingguYe](https://x.com/PingguYe) on X.

---

*This project builds on [MiroFish](https://github.com/666ghj/MiroFish) (81k+ stars, AGPL-3.0) and [OASIS](https://github.com/camel-ai/oasis) (Apache-2.0). We thank both teams.*

