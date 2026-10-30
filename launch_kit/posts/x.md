# X（Twitter）线程文案 · @PingguYe 口吻

> 口吻设定：第一人称、直接、承认失败、不喊口号。英文用于国际开发者，中文两条线程分别讲「产品怎么用」和「我们为什么公开失败」。
> 所有帖子都带真实数字与 `crh demo` 命令；**不**写「guaranteed」「world's first」「100%」。
> 配图：社交预览图（1280×640）+ 1 张 `crh demo` 终端截图 / 15 秒录屏。

---

## 1. 英文线程（发布日 D0，接 HN 之后或同时）

**1/7**
```text
We rewound 30 real corporate crises to 72 hours before they broke.

Then an LLM swarm (journalists, investors, regulators, short sellers) rehearsed each one — using only what was public at that moment.

The rehearsal's top-3 risks matched the real outcome 82.2% of the time.

But only 17% of events reproduced exactly across 3 runs.

Both numbers are in the repo. 🧵
```

**2/7**
```text
How it works:

‣ 30 public crises, 2018–2026, each with a T-72h information pack (clean room: no post-event info)
‣ 7–12 persona agents simulate reactions for 2 rounds on a simulated feed
‣ an 8k-char rehearsal report comes out
‣ a fixed LLM judge scores its top-3 risks against the recorded real outcome

30 events × 3 repeats = 90 runs. Same seeds, same judge prompt, same thresholds.
```

**3/7**
```text
The headline, with its error bars:

82.2% top-3 risk hit rate
95% CI 78.5–85.9
event-mean graded score (0–3 per event), mean 2.47/3
n = 30 events, not 90 independent samples

It is a backtest against a fixed rubric. It is not a probability about the next crisis, and we don't sell it as one.
```

**4/7**
```text
The uncomfortable part, published too:

‣ only 5/30 events scored identically in all 3 runs
‣ within-event SD 0.26/3
‣ our own stability score is STA 58 — below our pass line of 60. Failed.
‣ dominant error mode: false escalation (legal/regulatory branches that never happened)

Failures + post-mortems: data/failures.md
```

**5/7**
```text
Try it in 60 seconds, offline, no API key:

pipx install git+https://github.com/yepinggu66/crisis-rehearsal
crh demo --out demo

It verifies the evidence pack (43 files, sha256), recomputes the published stats, and writes 4 self-contained HTML rehearsal dossiers. Runs in 0.16s on a laptop.

AGPL-3.0. Repo: https://github.com/yepinggu66/crisis-rehearsal
```

**6/7**
```text
Why this matters for enterprises/government:

‣ runs on your infrastructure (local graph adapter replaced the cloud graph dependency)
‣ self-contained HTML dossiers you can archive or send to a board
‣ scenario pack schema for sector-specific rehearsals
‣ compliance docs are requirement mappings — not certifications. No government/client case yet. We say so in the docs.
```

**7/7**
```text
What I want: hard feedback.

Is 30 events × 3 repeats a defensible unit of analysis for this claim?
Would you trust an LLM judge, and if not, what would change your mind?

Demo, evidence and failure notes are all public. Tell me what's wrong with it.

https://github.com/yepinggu66/crisis-rehearsal
```

**发布注意：** 7 条一次性连发；置顶第 1 条；发布后 2h 内回复每个技术性问题；不要买转发/点赞；不 @ 大 V 求转。

---

## 2. 中文线程 A：产品怎么用（D2 或 D12）

**1/6**
```text
我们把 30 起真实企业危机，倒回到事发前 72 小时。

只给模拟器当时「已经公开」的信息，让 7–12 个 AI 角色（记者、散户、监管、做空机构、竞争对手）在模拟信息流里反应两轮，产出一份 8k 字的预演报告，再拿报告的前三大风险去对真实结局打分。

30 起 × 3 次 = 90 次回测。
```

**2/6**
```text
数字我不修饰，全带区间：

前三大风险命中率 82.2%
95% 置信区间 78.5–85.9
这是 30 个事件的「事件均值打分」（0–3 分制，均值 2.47/3），不是 90 个独立样本，也不是对下一次危机的概率预测。

v0.1 单跑结果复现：配对差 −0.02/3（±0.18）。
```

**3/6**
```text
不好看的部分也一起发了：

‣ 只有 5/30 个事件在三次运行里完全一致（17%）
‣ 同一事件重复跑的组内标准差 0.26/3
‣ 我们自己的稳定性指标 STA 58，及格线 60 —— 不及格
‣ 最大的错误模式是「过度升级」：把没发生的法律/监管路径写进 Top-3

失败案例和复盘：仓库里的 data/failures.md。
```

**4/6**
```text
所以我们的交付规则是：同一事件跑 3–5 次，读共识，不看单次最好成绩。

单跑单事件的分数是噪声——这句话是我们先说的，不是别人替我们发现的。
```

**5/6**
```text
一条命令，60 秒内自己验证（离线、不用 API key、<10 秒）：

pipx install git+https://github.com/yepinggu66/crisis-rehearsal
crh demo --out demo
它会校验证据包 sha256、复算已发布统计、生成 4 份自包含 HTML 演练档案。
```

**6/6**
```text
企业 / 政府场景：可离线、数据不出域、报告可直接归档上会；场景包 schema 支持按行业/部门定制。

合规文档是「标准要求映射 + 缺口」，不是认证，也没有政府/客户案例——文档里写得很清楚。

仓库（AGPL-3.0）：https://github.com/yepinggu66/crisis-rehearsal
欢迎拍砖，尤其欢迎拿数据反驳我。
```

---

## 3. 中文线程 B：我们为什么把失败也开源（D4 或 T+1 周）

**1/6**
```text
大多数 AI 项目发布时只给你看最好看的那次结果。

我们把 90 次回测的原始评分、失败案例、以及「我们自己没及格」的稳定性分数一起开源了。

为什么？因为危机预演这东西，如果只展示成功，等于在骗要拿它上董事会的人。
```

**2/6**
```text
先说结论：

前三大风险命中率 82.2%（95% CI 78.5–85.9；30 个事件，每个 3 次重复）。

但只有 17% 的事件在三次运行里完全一致。同一事件重跑的波动（SD 0.26/3）几乎和不同事件之间的难度差（0.30/3）一样大。
```

**3/6**
```text
这意味着：如果你只跑一次、只看一个分数，你看到的大概率是噪声。

我们的稳定性指标 STA 58，没到自设的 60 及格线，更没到 75 的资金线。这个数字写在 README 里，也写在 data/repeat_v02/v02_summary.md 里。
```

**4/6**
```text
最值得说的失败模式是「过度升级」：模型很爱写「监管介入 / 法务追责 / 甩锅供应商」这类分支，听起来专业，但真实结局里没发生。

在表现最差的 5 个事件里，6 个零分 Top-3 席位中有 5 个是这类分支。
```

**5/6**
```text
对企业用户的实际建议：

把预演当「提前暴露分歧」的工具，不当「预测下一个危机」的工具。
报告的价值在时间线、利益相关方图、升级阶梯、决策日志——这些能直接上会讨论；82.2% 只是一个方向的证据。
```

**6/6**
```text
全部证据可离线复算（两条标准库脚本 / 一条 crh demo）：

https://github.com/yepinggu66/crisis-rehearsal

如果你在 PR/IR/风控/应急口，欢迎拿你们真实的事件来 challenge 这套方法。我们更想要被证伪，而不是被转发。
```

---

## 4. 发布注意（X 平台）

| 项 | 建议 |
|---|---|
| 时间 | 英文线程跟随 HN（北京 21:00–23:00）；中文线程北京 12:00–13:00 或 21:00–22:00 |
| 媒体 | 第 1 条带社交预览图；第 5 条带 15 秒 `crh demo` 录屏或终端截图 |
| 标签 | 英文：`#LLM #MultiAgent #OpenSource #AI`（≤2 个，多了像营销）；中文：`#AI #开源 #危机公关`（≤2 个） |
| 链接 | 链接放最后一条，避免首条被算法降权；或首条评论区补链接 |
| 互动 | 只回复技术问题；遇到「你这就是套壳」用 `posts/hn.md` §4 的答案，不吵 |
| 禁止 | 买赞/买转、互赞群、私信求转、「guaranteed accuracy」类措辞 |

**发布后：** 把线程最高赞的问题整理成一条 quote tweet 回复；一周后发一条「数据更新」短帖（views/clones/真实反馈），保持账号有后续，而不是发完就消失。
