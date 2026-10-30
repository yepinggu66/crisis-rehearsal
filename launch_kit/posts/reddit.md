# Reddit 分版文案

> **通用规则（必须先读）：**
> 1. 每个版块的版规请以当日页面为准，发布前逐条打开核对：`https://www.reddit.com/r/<sub>/about/rules`。
> 2. Reddit 对 self-promotion 敏感：**每个版 30 天内最多 1 帖**；先参与 2–3 个别人的帖子再发自己的；必须 disclose「我是维护者」。
> 3. **不要 4 个版同一天发同一篇文案**——会被判定跨版 spam。间隔 ≥48h，且每版文案改写开头。
> 4. 不发纯链接（会被删）；用 text post，链接放正文中或评论区第一条。
> 5. 不买 upvote、不找朋友刷票（Reddit 反作弊会 shadowban）。

**发布顺序建议：** D6 r/MachineLearning → D8 r/LocalLLaMA → D10 r/riskmanagement →（可选）D12 r/China。

---

## 1. r/MachineLearning

**Flair：** `Project`（如版内提供 `[P]` 标签则标题加 `[P]`）。
**Title：**
`[P] An open backtest of 30 corporate crises with an LLM swarm simulator — 82.2% top-3 risk hit rate, but only 17% of events reproduce exactly`

**Body：**

```text
I'm the maintainer. Sharing a project + the parts that didn't work, because I think the failure modes are the interesting bit.

**What we did.** We took 30 publicly documented Chinese corporate crises (2018–2026), rewound each to 72 hours before it broke, and gave a swarm simulator only the public information available at that moment (7–12 persona agents: journalists, retail investors, regulators, short sellers, competitors; 2 rounds on a simulated feed). An LLM judge grades the report's top-3 risks against the recorded real outcome.

**Results (v0.2).** 30 events × 3 repeats = 90 runs, same seeds, same judge prompt, same thresholds.

- Top-3 risk hit rate: 82.2% (95% CI 78.5–85.9; event-mean graded score, mean 2.47/3; n=30 events, not 90 independent samples)
- Only 5/30 events (17%) scored identically across all three runs; within-event SD 0.26/3
- Internal stability STA 58, below our own pass line of 60 — we publish it as failed
- Paired per-event difference vs. the single-run v0.1: −0.02/3 (±0.18), so v0.1 reproduced
- Failures with post-mortems: data/failures.md. The dominant error is false escalation (legal pressure / blame-the-supplier branches that never happened).

**What's open.** Event library, T-72h seed packs, the local knowledge-graph adapter (replacing MiroFish's Zep Cloud dependency), the fixed judge prompt, all 90 judge records, CI/STA scripts (stdlib only), and the failure notes. AGPL-3.0.

**Try it offline (no API key, <10s):**

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo
It verifies the evidence pack by sha256, recomputes the published numbers, and writes self-contained HTML dossiers.

**What I'd like from this sub:** is 30 events × 3 repeats a defensible statistical unit for this kind of claim? The CI covers sampling + run randomness only — it does not include judge error, and the judge has not been human-calibrated yet. If you'd frame the uncertainty differently, I'd rather hear it now.

Repo: https://github.com/yepinggu66/crisis-rehearsal (AGPL-3.0). I sell rehearsal reports/workshops, not software; the engine is open. Happy to answer anything about the protocol.
```

**版规注意：** 项目帖通常要求 `[P]`/Project flair；**必须**附方法细节，纯宣传/纯链接会被删；不要在标题写「launch」。若版规不允许 self-promo 直接发帖，改发到版内的 monthly showcase 线程。

---

## 2. r/LocalLLaMA

**角度：** 离线、无云、无 API key 的 demo；本地知识图谱替代 Zep Cloud；模型可换 DeepSeek/Ollama/vLLM。
**Title：**
`A crisis-rehearsal engine that runs a 30-event backtest offline — "crh demo" needs no API key and finishes in <10s`

**Body：**

```text
Maintainer here. This sub is about running things locally, so I'll skip the pitch and give the local-first details.

The project rehearses a reputational crisis 72h before it breaks using an LLM swarm simulation (7–12 persona agents, 2 rounds). The full run needs an LLM endpoint (we used DeepSeek; any OpenAI-compatible endpoint works — Ollama/vLLM included). But the **evidence pack is fully offline**:

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo
`crh demo` = verify sha256 of the 90 judge records + recompute the published stats + generate 4 self-contained HTML dossiers. No API key, no network, <10s, stdlib only.

Why it's local: upstream MiroFish depends on Zep Cloud for its knowledge graph. We replaced that with a local JSON graph adapter (one patch, ~400 lines), so the pipeline runs with zero cloud graph service. Deployment notes for air-gapped setups: docs/deployment.md.

The numbers, with error bars: 30 events × 3 repeats, top-3 risk hit rate 82.2% (95% CI 78.5–85.9, event-mean graded score). Only 5/30 events reproduce exactly across runs, and our internal stability score is 58/100 vs a 60 pass line — published as failed. So treat single-run scores as noise.

Question for locals: if you were running this fully offline, would you rather (a) keep the LLM judge as a fixed local model and accept its bias, or (b) replace it with a human-scored rubric? We're leaning (a) for reproducibility + (b) as a calibration layer, but I'm curious what this sub would do.

Repo (AGPL-3.0): https://github.com/yepinggu66/crisis-rehearsal
```

**版规注意：** 与本地模型无关的纯宣传会被删——首段必须落在「本地/离线/模型可换」；不要在标题放外部产品链接；如果版内 `Show and tell` 类 flair 存在优先用。

---

## 3. r/riskmanagement

**角度：** 给风险/应急/合规从业者看方法论，不卖软件。
**Title：**
`We backtested a crisis-rehearsal method on 30 public corporate crises — here's what we'd want a risk team to challenge`

**Body：**

```text
I'm the maintainer of an open-source crisis rehearsal engine. Posting the method and the failure data, not a product link, because this sub is practitioners.

Setup: rewind a real reputational crisis to T-72h, restrict the simulator to information that was public at that moment (no hindsight), simulate stakeholder reactions (media, investors, regulators, competitors, customers), produce a rehearsal report, and score its top-3 risks against what actually happened. 30 events, 3 repeats each (90 runs).

What held: top-3 risk hit rate 82.2% (95% CI 78.5–85.9; event-mean graded score, n=30). v0.1 (single run) reproduced at −0.02/3 paired difference.

What didn't: only 17% of events produced identical scores across three runs; our internal stability score is 58 vs. a 60 pass line. The dominant error mode is **false escalation** — legal/regulatory branches that felt plausible but never happened (documented in the failures file). There is no human-analyst control condition, so this is not evidence the method beats an experienced team.

For a risk team, the practical read: the value is in the rehearsal artifact (timeline, stakeholder map, escalation ladder, decision log) and in surfacing disagreements before they're expensive — not in the headline rate. If you'd evaluate this in a pilot, what would your acceptance criteria be? I'm collecting exactly that (the pilot outline is docs/enterprise/overview.md).

If you want to inspect the evidence: data/repeat_v02/ (90 judge records) and data/failures.md in the repo; everything recomputable with two stdlib scripts. Repo: https://github.com/yepinggu66/crisis-rehearsal (AGPL-3.0). No customer/government cases — we don't have any yet, and I won't pretend otherwise.
```

**版规注意：** 从业者版通常允许方法论讨论，但**反感 vendor pitch**；正文不要放 CTA/价格；建议只把仓库链接放最后一行；若版规要求 flair，选 `Discussion`/`Methodology`。

---

## 4. r/China（**不建议首发；可选**）

> **风险：** 内容涉及中国企业的公开危机事件（含监管处罚），该版对商业推广与政治敏感话题执行严格，且转化极低。建议**跳过**，用中文渠道（知乎/公众号/即刻）代替。
> 如果仍要发：只谈方法与数据，不评论任何监管/政治背景，不贴价格、不招揽客户。

**Title（若发）：**
`An open, reproducible backtest of 30 Chinese corporate crises — and the cases where the method failed`

**Body（精简版）：**

```text
Maintainer here. We published a reproducible backtest of a crisis-rehearsal method on 30 publicly documented Chinese corporate crises (2018–2026), including the cases where it failed.

Method: rewind each event to 72h before it became public, restrict the simulator to public information at that moment, generate a rehearsal report, then score its top-3 risks against the actual outcome. 30 events × 3 repeats, all judge records and the failure post-mortems are in the repo.

Numbers: top-3 risk hit rate 82.2% (95% CI 78.5–85.9; event-mean graded score); only 5/30 events reproduce exactly across runs; stability score 58 vs. a 60 pass line. This is a rehearsal/backtest, not a forecast.

Everything is recomputable offline:

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo

Repo: https://github.com/yepinggu66/crisis-rehearsal (AGPL-3.0). I'm not posting to promote a product; the data and failure notes are public and I'd welcome methodological critique.
```

**版规注意：** 该版对 self-promotion 与「外链带商业目的」非常敏感；若版规禁止商业链接，**不要发**。
