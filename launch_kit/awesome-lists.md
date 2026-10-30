# Awesome Lists 提交清单（18 个可提 PR + 门槛核对）

> **数据来源：** GitHub API 实测（2026-10-31 01:51 Asia/Shanghai），star 数见 `recon/api-snapshot-2026-10-31.json`；栏目名逐个从各仓库 README 抓取核对；CONTRIBUTING 文件是否存在用 `GET /repos/{owner}/{repo}/contents/CONTRIBUTING.md` 的真实退出码验证（不是猜的）。
> **本文件只准备 PR 资产，不代提 PR。** 必须由 Lead 用**自己的 GitHub 账号手动 fork → 改 README → 提 PR**（Agent 不执行 fork/PR/star）。

---

## 0. 通用规则（先读，违反会被拉黑）

1. **先 star + watch 目标清单，再提 PR。** 最好在提交前 1–2 周就 star，并读过 20 条以上现有条目，确认格式。
2. **一次只提 1 个 list、只加 1 条。** 同一个账号一天内对 5 个 awesome list 提 PR = 典型 spam 特征。
3. **严格按字母序 / 表格列 / 分类**，并复制现有条目的标点、链接格式、句末句号习惯。
4. PR 描述必须写：**加了什么、放在哪个分类、为什么符合该分类、如何验证（一条 `crh demo` 命令）**。不要只写 "add project"。
5. **不要**要求互 star / 互 PR；**不要**在 PR 里写「please merge, I'll star your repo」。
6. 被拒后**问一次原因**，按要求改一次；仍被拒就换下一家，不争论、不重复提。
7. 预期：**首轮通过率 30%–50%**。把它当分发长尾，不是主渠道。90 天内目标收录 ≥3 个。
8. 需要人工操作：fork、编辑 README、`git commit`、开 PR、回复 review。**本包不提供脚本自动提交。**

**提交节奏建议：** v0.3.0 发布后 **第 2 周**开始（先让仓库有 demo/Release，维护者点进去能看到活的东西），每周 1–2 个，A 组先提。

---

## 1. 总览（18 个）

| # | 仓库 | stars | 目标栏目（README 实测） | 适合度 | 提交方式 | 通过预期 |
|---|---|---:|---|---|---|---|
| 1 | e2b-dev/awesome-ai-agents | 30,716 | AI agents（按字母序的单条 `## [Name](url)` 条目） | **A** | PR 或官方表单 | 中 |
| 2 | steven2358/awesome-generative-ai | 12,789 | Agents → Autonomous agents | **A** | PR（有 CONTRIBUTING.md） | 中 |
| 3 | jim-schwoebel/awesome_ai_agents | 2,022 | Applications / Benchmarks / Tools | **A** | PR（README 内有 Contributing 节） | 中高 |
| 4 | Wanying-He/awesome-llm-social-simulation | 12 | General-Purpose Social Simulation Platforms（表格） | **A** | PR（README 明示 PRs welcome） | 高 |
| 5 | tamlhp/awesome-sns | 13 | Datasets and Benchmarks / LLM-Based Agentic Simulation | **A** | Issue 或 PR | 中高 |
| 6 | benchflow-ai/awesome-evals | 1,021 | 5 Evaluation infrastructure / 9 Agent-specific evaluation | **A** | PR（有 CONTRIBUTING.md） | 中 |
| 7 | VoltAgent/awesome-ai-agent-papers | 1,879 | AI Design + Build Ecosystem Tools | B | PR（有 CONTRIBUTING.md） | 中 |
| 8 | onejune2018/Awesome-LLM-Eval | 659 | Tools | B | PR（README 明示欢迎 PR） | 中低 |
| 9 | sboudon/ABM | 14 | Open Source Frameworks, Libraries & Software | B | PR（GPL 仓库，小清单） | 中高 |
| 10 | GRC-Engineer/awesome-security-GRC | 1,112 | Risk Management → Risk Management Tools & Packages | B | PR（有 CONTRIBUTING.md） | 低中 |
| 11 | veeral-patel/awesome-risk-quantification | 473 | Open Source Projects | B | PR | 低中 |
| 12 | sotopia-lab/awesome-social-agents | 117 | Applications（偏论文/工作清单） | B | PR（有 CONTRIBUTING.md） | 低 |
| 13 | tdi/awesome-private-ai | 192 | Agents & Orchestration（本地可跑工具） | B | PR（有 CONTRIBUTING.md） | 低中 |
| 14 | AiHubCN/Awesome-Chinese-LLM | 22,771 | 2.3 其他应用 | C | PR（无 CONTRIBUTING，按 README 格式） | 低 |
| 15 | WangRongsheng/awesome-LLM-resources | 9,055 | 智能体 Agents | C | PR | 低中 |
| 16 | dipakkr/awesome-ai-engineering | 22,495 | Best GitHub Repositories / AI tools | C | PR（有 CONTRIBUTING.md） | 低 |
| 17 | WenyuChiou/awesome-agentic-ai-zh | 8,300 | 📚 先收藏的學習入口（资源） | C | PR（有 CONTRIBUTING + 写作规范） | 低 |
| 18 | totogo/awesome-knowledge-graph | 1,905 | Infrastructure / Knowledge Engineering | C | PR（contributing.md） | 很低（组件非独立项目） |

> **A = 建议本周提；B = 视素材再提；C = 有余力再试，预期低。**

---

## 2. A 组：高适合度（先提这 6 个）

### 1. `e2b-dev/awesome-ai-agents`（30,716 stars）

- **栏目：** AI agents 单条列表（按项目名字母序）。现有条目格式是 `## [Name](url)` + 1–3 行描述 + 可选 `<details>`。
- **门槛核对：** ✅ 收录外部 GitHub 仓库（README 中约 222 个外部 github.com 链接）；✅ 无 star 门槛；✅ README 明示「Create a pull request or fill in this form」；❌ 无 CONTRIBUTING.md（按 README 说明走）；接受官方表单 `forms.gle/UXQFCogLYrPFvfoUA`。
- **适合度：** A。它是「AI agent」清单，我们的引擎是 agent-based simulation + 可跑 demo，落在「agents 应用」而非框架。
- **提交：** PR（或先表单）。按 C 字母序插在 `## [ChatDev…]` 之后、`## [CrewAI…]` 之前（以当时 README 为准）。
- **PR 标题：** `Add Crisis Rehearsal — open-source agent-swarm rehearsal engine with a 30-event backtest`
- **条目文案（复制，注意保持字母序与格式）：**

```markdown
## [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal)

Open-source crisis rehearsal engine. Rewinds a real reputational crisis to 72 hours before it broke, runs a 7–12 persona agent swarm (journalists, investors, regulators, competitors) on only the information that was public at that moment, and grades the rehearsal report's top-3 risks against the recorded outcome. 30 public events × 3 repeats; `crh demo` runs offline in under 10s with no API key.
```

---

### 2. `steven2358/awesome-generative-ai`（12,789 stars）

- **栏目：** `Agents` → `Autonomous agents`（README 实测存在该二级标题）。
- **门槛核对：** ✅ 收录外部仓库/产品（README 约 122 个外部链接）；✅ 有 `CONTRIBUTING.md`（已确认存在）；✅ 无 star 门槛；条目格式为 `- [Name](url) — 一句话 `。
- **适合度：** A。该清单覆盖 generative AI 工具/产品，我们的 LLM swarm 引擎可归入 autonomous agents。
- **提交：** PR，按字母序放在 `Autonomous agents` 小节。
- **PR 标题：** `Add Crisis Rehearsal to Agents / Autonomous agents`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Open-source crisis rehearsal engine: an LLM agent swarm rehearses a reputational crisis 72 hours before it breaks, backtested on 30 public events × 3 repeats (82.2% top-3 risk hit rate, 95% CI 78.5–85.9). Offline demo via `crh demo`.
```

---

### 3. `jim-schwoebel/awesome_ai_agents`（2,022 stars）

- **栏目：** `Applications`（首选；`Benchmarks` 也可，但我们的回测是方法而非 benchmark 数据集）。
- **门槛核对：** ✅ 收录外部项目（README 约 1,791 个外部 github 链接）；✅ README 内有「Contributing to this Repo」小节；❌ 无 CONTRIBUTING.md；无 star 门槛。
- **适合度：** A。清单定位是「AI agent 工具/项目/数据集」的综合 hub。
- **提交：** PR，按 README 内现有 Applications 小节的 bullet 格式。
- **PR 标题：** `Add Crisis Rehearsal to Applications`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) - Open-source crisis rehearsal engine that simulates how journalists, investors, regulators and competitors react 72 hours before a reputational crisis breaks; backtested on 30 public corporate crises (82.2% top-3 risk hit rate, 95% CI 78.5–85.9) with a 60-second offline demo.
```

---

### 4. `Wanying-He/awesome-llm-social-simulation`（12 stars）

- **栏目：** `General-Purpose Social Simulation Platforms`（表格）；备选 `Evaluations & Benchmarks`（`Benchmarks` 子节）。
- **门槛核对：** ✅ README 明示 `PRs welcome`；✅ 收录代码链接（表格有 `Code` 列，例如 YuLan-OneSim 的 GitHub 链接）；❌ 无 CONTRIBUTING.md；无 star 门槛。**注意：该表以论文/平台为主，Paper 列可写 `—`，但必须提供 Code 列链接。**
- **适合度：** A（品类最贴近：LLM 社会模拟 + 平台）。这是一个小清单（12 star），但命中精准。
- **提交：** PR，按表格列格式新增一行（`Framework | Paper | Affiliation | Date | Scale | Key Novelty | Code`）。
- **PR 标题：** `Add Crisis Rehearsal (rehearsal platform + 30-event backtest)`
- **条目文案（表格行，按列补）：**

```markdown
| **Crisis Rehearsal** | — (open methodology, no paper) | Independent | 2026.10 | 7–12 agents / event | Rehearses a reputational crisis at T-72h with an agent swarm; ships a 30-event × 3-repeat backtest (82.2%, 95% CI 78.5–85.9), failure cases, and a self-contained HTML dossier. Offline demo, AGPL-3.0 | [[Code](https://github.com/yepinggu66/crisis-rehearsal)] |
```

> 诚实提醒：我们没有论文。如果维护者要求「必须有 paper」，就明说没有，撤回这条，不伪造引用。

---

### 5. `tamlhp/awesome-sns`（13 stars）

- **栏目：** `Datasets and Benchmarks`（我们的价值是 30 事件证据包 + 90 条评分记录）；备选 `LLM-Based Agentic Simulation`（但该节偏论文）。
- **门槛核对：** ✅ README 明示「欢迎 issue / PR」；✅ 收录 datasets 与 benchmarks；✅ 有分类学（taxonomy）要求——必须对齐其分类；❌ 无 CONTRIBUTING.md；无 star 门槛。
- **适合度：** A（数据集/基准定位匹配）。它是论文向清单，条目通常是论文；我们以「开放数据集 + 基准」身份提交，附仓库链接。
- **提交：** 先开 issue 问「code+dataset 是否可入 Datasets and Benchmarks」，再按回复提 PR（更稳）。
- **PR/Issue 标题：** `Add Crisis Rehearsal: 30-event crisis backtest dataset + 90 judge records`
- **条目文案（按现有 bullet 格式，论文栏留空或写技术报告）：**

```markdown
- **Crisis Rehearsal** — An open benchmark of 30 publicly documented corporate crises with T-72h information packs, 90 LLM-judge records and failure cases; supports rehearsal research on agent-based social simulation. Code & data: https://github.com/yepinggu66/crisis-rehearsal (AGPL-3.0). No accompanying paper.
```

---

### 6. `benchflow-ai/awesome-evals`（1,021 stars）

- **栏目：** `5 · Evaluation infrastructure`（数据集/scorers）或 `9 · Agent-specific evaluation`；加类型标签 `benchmark`/`tool`。
- **门槛核对：** ✅ 收录工具/基准/数据集（README 约 163 个外部链接）；✅ 有 `CONTRIBUTING.md`；✅ 有明确条目格式（链接 + 类型标记 + 🆕/⚠️ 标记）；无 star 门槛。
- **适合度：** A（「LLM judge + 可复算基准 + 失败案例」是它明确收的内容）。
- **提交：** PR，按 CONTRIBUTING 的条目格式（Type / 一行说明 / 年份标记）。
- **PR 标题：** `Add Crisis Rehearsal — agent-swarm backtest with 90 fixed-judge records`
- **条目文案：**

```markdown
- **[Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal)** — Open benchmark for LLM-judged crisis rehearsal: 30 public events × 3 repeats, 90 fixed-prompt judge records, published failure cases and stability report (82.2% top-3 risk hit rate, 95% CI 78.5–85.9). Stdlib-only reproduction scripts; offline `crh demo`. · *benchmark / tool* — 🆕 2026
```

> ⚠️ 该 README 自己就强调「benchmark integrity: contamination, saturation, label errors」——我们的诚实披露（17% 复现、judge 未人工校准）正好对上它的调性，PR 描述里点出来。

---

## 3. B 组：中等适合（A 组完成后提）

### 7. `VoltAgent/awesome-ai-agent-papers`（1,879 stars）

- **栏目：** `AI Design + Build Ecosystem Tools`（README 实测存在该节）。
- **门槛核对：** ✅ 有 CONTRIBUTING.md；✅ 该节收工具（非仅论文）；无 star 门槛。
- **适合度：** B。主体是 papers，工具表只是附属。
- **PR 标题：** `Add Crisis Rehearsal to AI Design + Build Ecosystem Tools`
- **条目文案（按现有表格/列表格式）：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Open-source agent-swarm crisis rehearsal engine with a 30-event public backtest (82.2% top-3 risk hit rate, 95% CI 78.5–85.9) and offline `crh demo`.
```

---

### 8. `onejune2018/Awesome-LLM-Eval`（659 stars）

- **栏目：** `Tools`；备选 `Datasets or Benchmarks`。
- **门槛核对：** ✅ README 明示「welcome any pull request」；✅ Tools 节收开源工具；❌ 无 CONTRIBUTING.md；无 star 门槛。
- **适合度：** B。该清单聚焦 LLM 评测，我们的核心是危机预演，评测是手段不是主题。
- **PR 标题：** `Add Crisis Rehearsal to Tools`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) - A crisis rehearsal engine with a 30-event × 3-repeat backtest and a fixed LLM-judge protocol; 90 raw judge records, adaptation scripts, and failure cases are public. Offline demo: `crh demo`.
```

---

### 9. `sboudon/ABM`（14 stars）

- **栏目：** `Open Source Frameworks, Libraries & Software`。
- **门槛核对：** ✅ 收 ABM 软件（README 约 10 个外部链接）；✅ GPL-3.0 仓库，与 AGPL 兼容；❌ 无 CONTRIBUTING.md；无 star 门槛。**注意：该清单侧重交通/人群移动，我们的 ABM 是舆论/群体反应，要在描述里点明差异。**
- **适合度：** B（小而精准的 ABM 读者）。
- **PR 标题：** `Add Crisis Rehearsal — agent-based simulation for reputational crises`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Agent-based simulation of stakeholder reactions (media, investors, regulators, competitors) for reputation-crisis rehearsal, with a 30-event × 3-repeat public backtest (82.2% top-3 risk hit rate, 95% CI 78.5–85.9). Useful as a non-transport ABM case study with open evidence.
```

---

### 10. `GRC-Engineer/awesome-security-GRC`（1,112 stars）

- **栏目：** `Risk Management` → `Risk Management Tools & Packages`。
- **门槛核对：** ✅ 有 CONTRIBUTING.md；✅ 收 risk management 工具；无 star 门槛。**注意：该清单以安全 GRC 为主，声誉危机是相邻而非核心——PR 里必须说清「不是安全 IR 工具」。**
- **适合度：** B/C。
- **PR 标题：** `Add Crisis Rehearsal to Risk Management tools (reputation-crisis rehearsal, not security IR)`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Open-source rehearsal engine for reputation crises (simulates stakeholder reaction at T-72h; backtested on 30 public events × 3 repeats). Runs offline; AGPL-3.0. Not a security-incident-response tool.
```

---

### 11. `veeral-patel/awesome-risk-quantification`（473 stars）

- **栏目：** `Open Source Projects`。
- **门槛核对：** ✅ 收开源项目（README 短小，Open Source Projects 节）；❌ 无 CONTRIBUTING.md；无 star 门槛。**注意：该清单的 risk 偏金融/网络风险量化；我们把「回测命中率 + CI」作为量化风险证据，但别硬说成 financial risk。**
- **适合度：** B/C。
- **PR 标题：** `Add Crisis Rehearsal to Open Source Projects`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — An open, reproducible backtest of a crisis-rehearsal method (30 public corporate crises × 3 repeats), with published confidence intervals, stability metrics, and failure cases. AGPL-3.0.
```

---

### 12. `sotopia-lab/awesome-social-agents`（117 stars）

- **栏目：** `Applications`（README 有 `Applications` 二级标题；整体偏 papers）。
- **门槛核对：** ✅ 有 CONTRIBUTING.md；✅ 收录社会 agent 工作；无 star 门槛。**注意：以论文为主，无论文的项目可能被拒。**
- **适合度：** B/C。
- **PR 标题：** `Add Crisis Rehearsal to Applications (open rehearsal platform + backtest, no paper)`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Open-source platform for rehearsing reputational crises with social agents (journalists, investors, regulators, competitors); ships a 30-event × 3-repeat backtest, 90 judge records and failure cases. AGPL-3.0. No accompanying paper.
```

---

### 13. `tdi/awesome-private-ai`（192 stars）

- **栏目：** `Agents & Orchestration`；备选 `Privacy, Security & Governance`。
- **门槛核对：** ✅ 有 CONTRIBUTING.md；✅ 定位是「on-prem / air-gapped / self-hosted」工具；无 star 门槛。
- **适合度：** B（我们确实支持离线/air-gap，这是它收的调性；但它是「AI 基础设施」清单，我们是应用）。
- **PR 标题：** `Add Crisis Rehearsal — offline/air-gapped crisis rehearsal engine`
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Self-hosted crisis rehearsal engine: agent-swarm simulation for reputational crises, offline `crh demo` (no API key), local graph adapter replacing the cloud graph dependency, and deployment notes for air-gapped installs. AGPL-3.0.
```

---

## 4. C 组：可试但预期低（有时间再提）

### 14. `AiHubCN/Awesome-Chinese-LLM`（22,771 stars）

- **栏目：** `2. 应用` → `2.3 其他应用`。
- **门槛核对：** ✅ 收中文 LLM 生态项目；❌ 无 CONTRIBUTING.md；无 star 门槛。**注意：该清单以模型/微调/应用为主，我们不是模型；被拒概率高。**
- **条目文案：**

```markdown
- [危机预演 Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) - 用 LLM 群体模拟预演企业危机：30 起公开事件回测 ×3 次，证据链与失败案例开源，`crh demo` 离线可跑（AGPL-3.0）。
```

### 15. `WangRongsheng/awesome-LLM-resources`（9,055 stars）

- **栏目：** `智能体 Agents`。
- **门槛核对：** ✅ 收资源/项目链接（README 约 687 个外部链接）；❌ 无 CONTRIBUTING.md；无 star 门槛。
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) - 危机预演引擎：LLM 群体模拟 + 30 起公开危机回测（82.2%，95% CI 78.5–85.9），失败案例与评分记录全开源，离线 `crh demo`。
```

### 16. `dipakkr/awesome-ai-engineering`（22,495 stars）

- **栏目：** `Best GitHub Repositories`（AI & ML 部分）。
- **门槛核对：** ✅ 有 CONTRIBUTING.md；✅ 收录 GitHub 仓库；无 star 门槛。**注意：清单极泛，审核标准不透明。**
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Open-source crisis rehearsal engine (agent swarm + 30-event backtest, 82.2% top-3 risk hit rate, 95% CI 78.5–85.9) with an offline CLI demo.
```

### 17. `WenyuChiou/awesome-agentic-ai-zh`（8,300 stars）

- **栏目：** `📚 先收藏的學習入口`（资源）。
- **门槛核对：** ✅ 有 CONTRIBUTING.md + 写作规范（`resources/style-guide.md`）；该清单是学习路线，不是工具目录。**注意：风格不符，除非能写成「教学案例」。**
- **条目文案：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — 一个可跑通的 multi-agent 社会模拟教学案例：30 起公开危机的 T-72h 信息包、群体模拟、固定 judge 协议与 90 条原始评分记录；`crh demo` 离线复算（AGPL-3.0）。
```

### 18. `totogo/awesome-knowledge-graph`（1,905 stars）

- **栏目：** `Infrastructure`（或 `Knowledge Engineering`）。
- **门槛核对：** ✅ 有 contributing.md；✅ 收工具/框架。**注意：我们把知识图谱换成了本地 JSON adapter 只是组件，不是独立 KG 项目——被拒概率很高，不建议优先提。**
- **条目文案（若提）：**

```markdown
- [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) — Ships a local JSON knowledge-graph adapter (replacing a cloud graph dependency) as part of an open crisis-rehearsal pipeline; the graph layer is a single inspectable file, not a general-purpose KG framework.
```

---

## 5. 不建议提交（会被拒或伤信誉）

| 仓库 | stars | 原因 |
|---|---:|---|
| Shubhamsaboo/awesome-llm-apps | 143,505 | 它的条目必须把可运行 app 代码放进**它的仓库**（README 链接指向仓库内子目录），不是外链清单；放外部链接会被拒。 |
| Arindam200/awesome-ai-apps | 16,650 | 同上：要求贡献 app 代码到其仓库，格式不匹配。 |
| meirwah/awesome-incident-response | 9,514 | 纯安全 IR 工具；危机预演不是 IR 工具，归错类会被维护者移除。 |
| kyegomez/awesome-multi-agent-papers | 1,705 | 只收论文；我们无 arXiv 论文。 |
| husthuke/awesome-knowledge-graph | 5,176 | 中文 KG 学习资料为主，非工具清单。 |
| totogo/awesome-knowledge-graph | — | 见 #18：只是「不建议优先」。 |

---

## 6. 提交跟踪表（Lead 填）

| 日期 | 清单 | PR/Issue 链接 | 状态 | 维护者反馈 | 下步 |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

**验收标准（90 天）：** 提交 ≥8 个，合并 ≥3 个；每次被拒记录原因，用于修正条目文案（尤其是「太营销 / 不符合分类 / 无论文」三类）。

---

## 7. PR 描述模板（通用，按 list 微调）

```markdown
## What

Adds [Crisis Rehearsal](https://github.com/yepinggu66/crisis-rehearsal) to **<栏目名>**.

## Why it fits

Crisis Rehearsal is an open-source (AGPL-3.0) crisis rehearsal engine: an LLM agent swarm (journalists, investors, regulators, competitors) rehearses a reputational crisis 72 hours before it breaks, using only the information that was public at that moment. It ships a 30-event × 3-repeat public backtest — top-3 risk hit rate 82.2% (95% CI 78.5–85.9) — plus 90 raw judge records, failure cases and stability metrics, all recomputable offline.

## How to verify

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo

`crh demo` is offline, needs no API key, and runs in under 10 seconds.

## Disclosure

I am the maintainer. No commercial relationship with this list. No customer or government references exist; the repository documents its limitations, including a 17% exact-reproduction rate across repeats.
```

**提交后：** 保持 PR 只含这一条改动；维护者要求 rebase 就 rebase；合并后在 X/即刻感谢（不@骚扰）；把链接记进 `recon/measurements.md`。
