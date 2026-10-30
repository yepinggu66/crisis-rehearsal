# Show HN 文案（Hacker News）

> 规则依据：HN 官方 Show HN Guidelines（已抓取核对，`https://news.ycombinator.com/showhn.html`，2026-10-31）。
> 核心要求：标题以 **`Show HN:`** 开头；必须是「别人能试玩/能跑」的东西；**不要**投票请求；发布者须在场讨论；新版本小更新不算 Show HN。

---

## 1. 发布时机

| 项 | 建议 |
|---|---|
| 日期 | 周二、周三或周四（避开周一（堆积）/周五（低流量）/美国假日） |
| 时间 | **美东 08:00–10:00**（冬令时 11 月后）= **北京 21:00–23:00**；欧陆读者也在线 |
| 发布后 | 作者必须在评论区在线 **3–4 小时**；前 30 分钟最关键 |
| 频率 | 整个 v0.3 周期只发 **1 次**；v0.4 大改版可再发 |

**发布日检查清单（全部为 ✅ 才发）：**
- [ ] 在**干净机器**（Windows + Linux 各一次）跑通：`pipx install git+https://github.com/yepinggu66/crisis-rehearsal && crh demo --out demo`（无 pipx 时用 clone + `pip install -e .`，见 README）
- [ ] README 前 40 行能独立说明「是什么 / 为什么现在 / 30 秒怎么跑」
- [ ] 社交预览图已上传，链接卡片可读
- [ ] `.github/ISSUE_TEMPLATE/` 已合并；`SECURITY.md` 可点
- [ ] 首评（§3）已写好并预演过
- [ ] 不向任何人请求 upvote/comment（HN 明令禁止 ring voting）

---

## 2. 提交内容

**Title（三选一，≤80 字符）：**

1. ✅ `Show HN: Open-source crisis rehearsal engine, 60-second offline demo`（68）
2. `Show HN: Crisis Rehearsal – backtesting 30 corporate crises with LLM swarm sim`（80）
3. `Show HN: Rehearse a reputational crisis 72 hours before it happens`（66）

**URL：** `https://github.com/yepinggu66/crisis-rehearsal`

**Text（可选，建议留空或 2 行）：**

```
Open-source crisis rehearsal engine (AGPL-3.0). Rewinds a real reputational crisis to 72h before it broke, runs an LLM swarm simulation on only the public information available then, and grades the rehearsal against what actually happened. 30 events, 3 repeats each. `crh demo` runs offline in under 10s, no API key.
```

> 不要写「upvote if…」「please share」；不要放 signup/newsletter。

---

## 3. 首评（作者自己发第一条；这是 HN 的核心转化位）

```text
Author here. A bit more context than the README.

What it is: we take 30 publicly documented Chinese corporate crises (2018–2026),
rewind to T-72h with only public information, run a swarm simulation (7–12 persona
agents: journalists, retail investors, regulators, short sellers, competitors) for
2 rounds, and generate an ~8k-character rehearsal report. An LLM judge then grades
the report's top-3 risks against the recorded real outcome.

The honest part is why I'm posting: our headline is a Top-3 risk hit rate of 82.2%
(95% CI 78.5–85.9, event-mean graded score, n=30 events × 3 runs) — and only 5/30
events scored identically on all three runs. Our internal stability score is 58,
below our own pass line of 60. We publish the failures too (data/failures.md).
So: useful as a rehearsal/backtest, not a forecast. Please hold us to that wording.

What's open: the 30-event library, the T-72h seed packs, the local knowledge-graph
adapter (MiroFish's Zep Cloud dependency replaced), the judge prompt, the 90 judge
records, and the failure notes. AGPL-3.0, same as upstream.

Try it (offline, no API key, <10s):

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo
It verifies the evidence pack by sha256 (43 files), recomputes the published statistics, and
writes 4 self-contained HTML rehearsal dossiers + an index. It finishes in 0.16s on a laptop.

What I'd most like feedback on: (1) is the "rehearsal vs. forecast" framing clear
enough, (2) is 30 events × 3 repeats a defensible unit of analysis, (3) would you
trust an LLM judge here, and if not, what would change your mind. I'll be around
for a few hours.
```

> 语气要求：不推销、不喊口号、主动说局限。HN 对「诚实 + 具体」的反馈远好于「revolutionary」。

---

## 4. 评论区 FAQ（预写答案，按需粘贴）

**Q：这不就是 MiroFish 套壳吗？**
> 不是。MiroFish 是上游（我们用它做群体模拟，AGPL 保持开源）。我们的工作在：把 Zep Cloud 知识图谱依赖换成本地 JSON adapter（一个 patch）、定义 T-72h 信息洁净室规则、30 事件库与真实结局、固定 judge 协议、90 次重复跑与统计（CI/方差/STA）、以及把报告做成可交付的自包含 HTML 档案。`docs/patches.md` 有逐条 patch 说明。

**Q：82.2% 是预测准确率吗？**
> 不是。它是 **event-mean graded score**（每个事件 0–3 分，30 个事件取均值），衡量「回测中 top-3 风险与真实结局的吻合度」，不是对未来事件的概率。二值口径下 30 个事件的区间约 ±17pp，所以我们不用二值口径。

**Q：只有 17% 完全复现，凭什么信？**
> 所以我们把交付规则写成「同一事件跑 3–5 次读共识」，不承诺「每次结论相同」。within-event SD 0.26/3 与 STA 58 都在 README 和 `data/repeat_v02/`。如果只跑一次单事件，那个分数就是噪声——这是我们自己先说的。

**Q：为什么只有中国市场事件？**
> 因为 T-72h 的公开信息最完整、可核验。Issue #3 是「加一个非中文市场事件」的 good first issue，欢迎带来源的 PR；非中文市场目前是我们明确的能力缺口。

**Q：judge 是 LLM，会自己给自己打分吧？**
> 是 LLM judge，固定 prompt、固定阈值、同一模型族，90 条原始记录都在仓库里。它**没有**人工校准（`data/judge_calibration.md` 是状态与模板，尚未执行），CI 也不包含 judge 误差。这是已知限制，不是隐瞒项。

**Q：离线能跑吗？要花多少钱？**
> `crh demo` 完全离线、无 API key、<10 秒。重新生成整个回测需要 LLM API：DeepSeek 约 $0.03/事件、~4 分钟/次，90 次约 6 小时墙钟。仓库给了 `docker-compose.yml` 的离线证据工作站形态；完整 MiroFish 重建路径在 README「Reproduce it」。

**Q：AGPL 商用可以吗？你们怎么赚钱？**
> 代码 AGPL-3.0：可以自部署、修改、对外提供服务，但修改后对外服务要开源。我们卖的是**演练报告与工作坊**，不是软件许可；行业本体（persona 规则）、客户语料、交付 playbook 不开源。没有 VC、没有融资故事。

**Q：有客户/政府案例吗？**
> 没有，不编。企业/政府版文档是设计说明（`docs/enterprise/*`、`docs/government.md`），明确写「未认证、未测评、无政府案例」。等保/ISO/SOC2 只做**要求映射与 gap**，不做认证宣称。

**Q：能用在网络安全 incident response 吗？**
> 方法论可以借（桌面演练、T-72h 信息包、事后评分），但当前 30 个事件是**声誉/舆情危机**，不是安全事件；不要把它当 SIEM/SOC 工具。

---

## 5. 规则注意（逐条核对官方）

| 规则 | 本方案如何满足 |
|---|---|
| 标题必须以 `Show HN` 开头 | ✅ 三版标题都满足 |
| 必须是「能试玩/能跑」的东西，不能是 landing page | ✅ `crh demo` 离线可跑；链接直达仓库，无注册 |
| 项目须是本人深度参与、非快速生成的一次性东西 | ✅ 90 次回测 + 90 条 judge 记录 + 失败文档在仓库 |
| 不要请求朋友 upvote/comment（ring voting） | ✅ 不发群、不私聊求投票；只在自己账号发 1 条 |
| 发布者需在场讨论 | ✅ 预留 3–4h 在线；首评先给方法/限制 |
| 小版本更新不算 Show HN | ✅ 只在 v0.3.0 发一次；v0.4 大改版才考虑 |
| 不要删帖重发刷曝光 | ✅ 不删不发；若被 flag，接受结果，改去 Reddit/知乎 |

**不要做的事：** 在 HN 评论区贴「求 star」「求 upvote」；用多个账号；把同一链接在 24h 内重复提交；标题写「We're building the future of crisis simulation」。

---

## 6. 发布后 24 小时动作

1. 前 60 分钟：只回复、不加新链接；每个问题都答「具体 + 承认限制」。
2. 2–3 小时：若帖沉了，不重发；把最高质量问答整理成 GitHub Discussion（`Show your rehearsal` 或 Q&A），后续知乎/X 引用。
3. 当天：把 HN 流量带来的 issue 按 `issue-triage.md` 处理；外部 issue 第一条回复要含 `crh --version` 与复现步骤。
4. 记录：HN 排名/评论数/带来的 views（GitHub traffic API 次日可见）；写入 `launch_kit/recon/measurements.md`。
