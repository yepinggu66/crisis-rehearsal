# 企业 / 政府外联（冷邮件 + pilot 提案 + 会议议程）

> 读者：大集团 CRO / 公关与 IR 负责人；央企/政府信息化与应急部门；国际 PR/IR 机构与风险咨询。
> **只写仓库里真实存在的能力。** 未认证、无客户/政府案例、无 SLA，全部明说。价格与 SLA 只在 `docs/enterprise/procurement.md` 以「示例」出现。
> 合规提醒：B2B 冷邮件需遵守个人信息保护法（PIPL）与目标市场的反垃圾邮件法规；只联系公开的**工作邮箱**（公司官网/年报/公开采购公告），不购买个人邮箱库，不做大规模群发，每封都有一句话退出方式。中文邮件建议用 owner 本人邮箱 `yepinggu@outlook.com` 或企业邮箱单发。

---

## 1. 冷邮件（中文 1）：上市公司 · 董事会秘书 / 品牌与公关负责人

**主题（二选一）：**
- `把下一次危机提前 72 小时演一遍——一次 2 周的离线预演试点（附 60 秒可自行验证的 demo）`
- `关于贵司危机预案的一次预演试点建议（开源引擎，数据不出域）`

**正文（约 230 字）：**

```text
X 总，您好：

我是「危机预演」（Crisis Rehearsal）的维护者 yepinggu。冒昧来信，只谈一件具体的事。

我们做了一套可私有化部署的危机预演方法：把一起真实发生过的危机倒回到爆发前 72 小时，只喂给模拟器当时已经公开的信息，让记者、投资者、监管、竞争对手等角色在模拟信息流里反应，产出一份可上会讨论的预演报告；再用固定评分协议把报告的前三大风险与真实结局对照。

开源仓库里有 30 起公开企业危机的回测（每起跑 3 次）：前三大风险命中率 82.2%（95% CI 78.5–85.9）。同时我们也公开了不好看的部分——只有 17% 的事件三次跑完全一致，我们自己的稳定性指标 58 分，低于自设及格线 60。

您可以先让技术同事用一条命令、离线验证（不用 API key，10 秒内）：
pipx install git+https://github.com/yepinggu66/crisis-rehearsal
crh demo --out demo

如果这个方法对贵司董事会/公关团队有价值，我们建议先做一个 2 周的离线试点：用 3 个与贵司行业相近的公开历史事件，跑出 3 份预演报告 + 1 次 2 小时复盘会。试点不需要贵司提供任何非公开数据。

说明：我们没有客户案例、没有认证，也不做「预测下一次危机」的承诺。仓库与文档里写清了能力与限制。

如果方便，能否约 30 分钟线上沟通？我可以现场跑一遍 demo，再讨论是否值得试点。

此致
yepinggu
危机预演 · https://github.com/yepinggu66/crisis-rehearsal
如不希望再收到此类邮件，回复「退订」即可。

---

**附件/链接（任选 1–2 个，不要全塞）：**
- 60 秒 demo：`https://youtu.be/pj7PKonS2Ns`（v0.3.0 上线后替换为最新录屏）
- 企业概览（设计说明）：`docs/enterprise/overview.md`
- 采购应答：`docs/enterprise/procurement.md`
```

**发送注意：** 单发，不要密送；附件用 PDF（不要发 `.md`）；工作日 09:30–11:00 或 14:30–16:00；3 个工作日无回复可跟进一次，之后停止。

---

## 2. 冷邮件（中文 2）：央企 / 政府 · 信息化、宣传或应急管理部门

**主题（二选一）：**
- `危机预演引擎：可离线部署、数据不出域的演练方案（含等保/数据安全法要求映射与缺口）`
- `关于危机预演在政务舆情/应急演练中的一次离线试点建议`

**正文（约 260 字）：**

```text
X 处/主任，您好：

我是「危机预演」开源项目的维护者 yepinggu。来信目的很明确：申请一次 30 分钟的方案沟通，讨论是否值得做 2 周的离线试点。

我们做的是「危机预演」：把一起公开发生过的危机倒回 72 小时前，只用当时公开的信息，让媒体、公众、投资者、监管等角色在模拟信息流中反应，生成演练报告，再按固定协议与真实结局对照评分。整套方法可离线运行，演示命令不需要联网、不需要 API key。

针对贵单位的关切，仓库里已有三份说明（均为设计说明，非测评结论）：
1. docs/enterprise/security.md：数据流、信任边界、STRIDE 威胁模型，默认数据不出域；
2. docs/enterprise/compliance.md：等保 2.0 三级、数据安全法、个人信息保护法、GDPR、ISO 27001、SOC 2 的「要求映射 + 缺口」；
3. docs/government.md：分级分类、离线/涉密隔离、信创适配（roadmap）与现有舆情/应急系统对接方式。

必须说清楚：我们没有任何认证或测评，也没有政府案例；信创适配是 roadmap 而非已交付。所有能力边界都写在文档里，不会在汇报里夸大。

如果贵单位愿意评估，我们建议先做一个不接触任何内部数据的 2 周离线试点：用 3 个公开历史事件，交付 3 份演练档案 + 1 次复盘会 + 1 份能力/缺口说明。是否方便安排 30 分钟线上沟通？

此致
yepinggu
危机预演 · https://github.com/yepinggu66/crisis-rehearsal
如不希望再收到此类邮件，回复「退订」即可。
```

**发送注意：** 政府/央企场景忌讳「效果承诺」与「案例暗示」；**不要**写「已服务某部委/某央企」。优先通过公开的采购/合作邮箱或会议认识的人转发，而不是直接群发。

---

## 3. 冷邮件（英文）：Global PR/IR agency, risk consultancy, or CISO

**Subject options:**
- `An offline crisis-rehearsal engine for your clients — 30-event public backtest, 60-second demo`
- `White-label crisis rehearsal: agent-swarm simulation, runs on your infrastructure (AGPL-3.0, no client data needed)`

**Body (~160 words):**

```text
Hi [Name],

I'm the maintainer of Crisis Rehearsal, an open-source engine for rehearsing a reputational crisis 72 hours before it breaks.

How it works: we rewind a real crisis to T-72h, restrict the simulator to information that was public at that moment, run a swarm of 7–12 persona agents (journalists, investors, regulators, short sellers, competitors) for two rounds, and grade the resulting rehearsal report's top-3 risks against the recorded real outcome. The repo ships 30 public crises × 3 repeats (82.2% top-3 risk hit rate, 95% CI 78.5–85.9) — and the uncomfortable parts: only 17% of events reproduce exactly across runs, and our own stability score is 58 vs a 60 pass line. Failures are published.

It is AGPL-3.0, runs offline, and a demo takes under 10 seconds with no API key:

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo

For an agency, the useful path is a two-week offline pilot on public events relevant to one client sector: three rehearsal dossiers, one workshop, one capability/gap memo. No client data required; no certifications claimed; we're a solo maintainer, not a vendor with a sales team.

Would a 30-minute call be useful? I can run the demo live.

Best,
yepinggu
Crisis Rehearsal — https://github.com/yepinggu66/crisis-rehearsal
If you'd rather not hear from me again, reply "unsubscribe".
```

**发送注意（GDPR/PECR）：** EU 收件人需有合法利益基础（B2B 相关职责）；首封即给退出方式；保存来源记录（公开官网/会议名单）；不附大附件；不追踪像素（避免同意问题）。

---

## 4. 一页 pilot 提案大纲（PDF 单页，随邮件或会议后发）

**标题：** `Crisis Rehearsal — 2-week offline pilot (design, not a claim)`

| 区块 | 内容（只写真实能力） |
|---|---|
| **1. 目标** | 在**不使用贵方任何非公开数据**的前提下，验证「危机预演」方法对贵方场景的相关性：能否在 2 周内产出可上会讨论的预演报告，并暴露团队分歧。 |
| **2. 范围** | 1 个行业方向（如：消费品舆情 / 金融合规 / 政务舆情）；3 个公开历史事件（从 30 事件库选或由贵方指定公开事件）；3–5 次重复运行/事件（按交付规则读共识）。 |
| **3. 交付物** | ① 3 份 T-72h 信息包；② 3 份自包含 HTML 预演报告（含 Top-3 风险、真实结局对照、sha256 溯源、诚实局限）；③ 1 次 2 小时复盘会（远程）；④ 1 份《能力与缺口说明》（含与贵方流程的差距）。 |
| **4. 不交付（non-goals）** | 不预测未来事件；不提供准确率承诺；不做认证/测评；不接入贵方内部系统；不处理个人信息或涉密数据。 |
| **5. 贵方投入** | 1 名业务接口人（每周 2 小时）；1 次复盘会；对 3 个公开事件的行业相关性给出反馈。**无需提供内部数据、无需安装任何软件**（我们提供离线演示环境；若需本地部署，按 `docs/deployment.md` 的离线工作站形态）。 |
| **6. 时间线（建议）** | D0 启动会 30min → D1–D5 事件选择与信息包 → D6–D10 运行（3–5 次/事件）→ D11–D12 报告与内部审阅 → D13 复盘会 → D14 交付与下一步决定。 |
| **7. 成功判据（示例，需与贵方共同确认）** | ① 3 份报告中至少 2 份被业务方认为「有 1 个此前未讨论过的风险点」；② 复盘会形成 ≥3 条可执行改进项；③ 双方对「是否进入付费阶段」给出明确 yes/no。**不以 82.2% 作为验收线**（它是回测统计量，不是本次 pilot 的 SLA）。 |
| **8. 数据与合规** | 全程公开信息；离线环境；不接触个人信息；签署 NDA/DPA（以贵方法务版本为准）；交付物默认不含贵方名称（除非书面同意）。 |
| **9. 报价结构（示例，非报价）** | 见 `docs/enterprise/procurement.md` §5：试点固定费 + 后续按事件/工作坊计费；开源引擎 AGPL-3.0 免费。 |
| **10. 退出条件** | 任一方可在启动会前无责退出；启动会后按已完成工作量结算（以合同为准）。 |

> 这一页的每一行都必须能在仓库文档里找到依据；找不到的能力，删掉，不要写进提案。

---

## 5. 30 分钟会议议程

| 分钟 | 环节 | 谁 | 要点 |
|---|---|---|---|
| 0–3 | 目标对齐 | 我方 | 「今天不推销，只确认这个方法对你们是否有用；不需要你们提供任何内部数据。」 |
| 3–8 | 对方现状 | 对方 | 最近一次危机演练怎么做？谁参加？报告最后去了哪？痛点是什么？ |
| 8–18 | **现场 demo**（核心） | 我方共享屏幕 | `crh demo` → 打开 HTML 档案 → 停在第 4 页「Top-3 风险 vs 真实结局」与「Honest limitations」；**不剪辑失败数字** |
| 18–24 | 部署与合规 | 双方 | 数据流、离线/air-gap、模型接入（内部网关/Ollama/vLLM）、等保/PIPL 映射与**缺口**；明确「未认证」 |
| 24–28 | 试点范围 | 双方 | 选 1 个行业方向 + 3 个公开事件；确认接口人、时间窗、复盘会日期 |
| 28–30 | 下一步 | 我方 | 24h 内发一页 pilot 提案 + demo 录屏链接；约定 yes/no 回复时间 |

**会前要问对方的 6 个问题（决定是否值得做 pilot）：**
1. 上一次危机演练是什么时候？参与人有哪些部门？
2. 演练报告最后有没有进董事会/管理层会议？
3. 数据能否出域？有没有必须离线/信创的要求？
4. 谁是这次评估的最终决策人？预算在哪个科目？
5. 如果 pilot 只能证明一件事，你们希望是哪件？
6. 采购流程需要哪些材料（安全问卷、DPA、报价单、案例）？——**案例我们没有，提前说明。**

**会前准备：** 最新 `crh demo` 录屏（离线可播）、一页 pilot 提案 PDF、`docs/enterprise/security.md` + `compliance.md` 的 PDF、`data/failures.md` 摘要（证明敢公开失败）。

**会后跟进：** 24h 内发提案 + 录屏 + 「3 个公开事件候选清单」；第 3 天确认是否启动；第 7 天仍未回复则暂停，不连续催促。

---

## 6. 外联合规与诚实清单（每次发送前逐条过）

- [ ] 只联系公开工作邮箱；来源可追溯；未购买邮箱库。
- [ ] 每封邮件有一句退出方式；收到退订后立即从名单移除。
- [ ] 不写「已服务/已合作/某央企/某政府」；不写「符合等保」「已认证」。
- [ ] 不承诺准确率、不承诺预测、不承诺 SLA（未签约前）。
- [ ] 不附任何客户数据、个人信息、涉密材料；演示只用公开历史事件。
- [ ] 数字口径与 `00-star-benchmark.md` / README 一致：82.2%（95% CI 78.5–85.9，event-mean graded score，n=30×3）；17% 复现；STA 58 failed。
- [ ] 邮件落款含真实身份与仓库链接；不用夸张标题党。
- [ ] 政府/央企沟通中，主动说明「信创适配是 roadmap、无政府案例」，避免后续验收争议。
