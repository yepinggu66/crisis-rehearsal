# 仓库设置（GitHub UI 操作清单 · v0.3.0）

> 目标：让第一次点进仓库的人，在 **5 秒内**知道「这是什么、能跑什么、证据在哪」；同时让采购/合规的人能找到 docs。
> 所有操作在 GitHub 网页完成（Settings / 仓库主页）。顺序按 §1 → §8 执行。**本文件不改 README**（README 由 W2 负责）。

---

## 1. About 描述（三版 EN + 三版 ZH，选一版）

GitHub About 的 description 在搜索结果里通常只显示前 ~120–160 字符，**前 90 字符必须自带信息**。
字符数已逐条标注（含空格；GitHub 上限 350）。

### EN（推荐第 1 版）

| # | 文案 | 长度 | 用法 |
|---|---|---:|---|
| EN-1 ✅ | `Rehearse a reputational crisis 72h before it breaks: swarm simulation + 30-event public backtest. Offline demo, AGPL-3.0.` | 121 | **推荐**（信息密度最高，含品类 + 证据 + 可跑） |
| EN-2 | `Open-source crisis rehearsal engine: LLM swarm simulation, 30 public crises backtested 3× each (82.2%, 95% CI 78.5–85.9).` | 121 | 强调数字，适合 HN 之后 |
| EN-3 | `Simulate how journalists, investors and regulators react — before the crisis lands. Runs on your own infrastructure.` | 116 | 面向企业读者，弱化数字 |

### ZH（中文读者 / 微信传播落地页）

| # | 文案 | 长度 | 用法 |
|---|---|---:|---|
| ZH-1 ✅ | `把危机提前 72 小时演一遍：群体模拟 + 30 起公开企业危机回测（82.2%，95% CI 78.5–85.9），可离线私有化部署。AGPL-3.0。` | 77 | **推荐**（数字 + 可跑 + 许可证） |
| ZH-2 | `危机预演引擎：用 LLM 群体模拟预演企业危机，30 起公开事件回测 3 次/起，证据与失败案例全部开源。` | 53 | 中文主站/公众号推荐 |
| ZH-3 | `在危机发生前 72 小时，把董事会、媒体、投资者、监管的反应先演一遍。开源，可私有化。` | 43 | 面向决策者，短 |

> 许可证口径：仓库实际为 **AGPL-3.0**，任何文案都不得写成 Apache/MIT。

**推荐组合：** About 用 **EN-1**（GitHub 默认英文界面 + 国际访客），中文传播靠 README-ZH 与公众号，不把中文塞进 About。

---

## 2. Topics（≤20 个，按优先级；GitHub 上限 20，小写、连字符）

当前 topics（API 实测，2026-10-31）：`agent-based-modeling, ai-agents, crisis-management, crisis-simulation, llm, llm-evaluation, multi-agent-simulation, public-relations, reproducibility, swarm-intelligence`（10 个）。

### 建议最终 20 个（直接复制）

```
crisis-simulation
crisis-management
tabletop-exercise
agent-based-simulation
agent-based-modeling
multi-agent-simulation
social-simulation
generative-agents
llm-agents
llm-evaluation
swarm-intelligence
public-opinion-analysis
reputation-management
risk-management
emergency-management
disaster-response
reproducibility
llm
python
ai-agents
```

**分组理由（每个 topic 的仓库规模来自 `00-star-benchmark.md` §2）：**

| 组 | topics | 为什么 |
|---|---|---|
| 核心定位（必须留） | crisis-simulation（12）、crisis-management（146）、tabletop-exercise（36） | 精准品类词；虽然池子小，但搜索/推荐命中精准 |
| 借流量：模拟/agent | agent-based-simulation（708）、agent-based-modeling（1,557）、multi-agent-simulation（151）、social-simulation（170）、generative-agents（131） | 进入 oasis / concordia / mesa 读者的浏览路径 |
| 借流量：LLM 开发者 | llm-agents（8,180）、llm-evaluation（8,874）、llm、python、ai-agents | 大池子，负责把 demo 推给能跑代码的人 |
| 买家词（企业/政府） | public-relations（64）、reputation-management（99）、risk-management（5,263）、emergency-management（207）、disaster-response（603） | 非开发者也会搜；给采购/应急口留入口 |
| 方法与可信度 | reproducibility、swarm-intelligence（850） | 差异化：公开回测 + 失败案例 |

**操作：** 仓库主页 → ⚙️（About 右侧齿轮）→ Topics 逐条粘贴 → Save。**不要**用 `simulation`（30,636 个仓库，纯噪音）、不要用 `incident-response`（7,518，且偏安全 IR，和声誉危机不是一回事）。

---

## 3. Homepage 链接

| 选项 | 链接 | 优点 | 缺点 | 建议 |
|---|---|---|---|---|
| A（当前） | `https://youtu.be/pj7PKonS2Ns` | 已有 2:42 demo | 不是入口页，无 README/数字 | 保留到 v0.3.0 demo 更新 |
| B ✅（发布时） | `https://pingguye.cn` | 已有站点，可放中文介绍/联系 | 若站点上没有仓库介绍，会掉转化 | **推荐，先确认站点有危机预演落地页** |
| C | `https://yepinggu66.github.io/crisis-rehearsal/` | 用 `crh site` 生成的静态索引站（30 个事件） | 需要开 GitHub Pages，且内容需审核 | 若 W1 的 `crh site` 质量过关，作为 v0.3.1 目标 |
| D | `https://github.com/yepinggu66/crisis-rehearsal/blob/main/docs/README.md` | 直接给文档索引 | 太长，不是营销页 | 备选 |

**推荐：** 发布日把 Homepage 换成 **B**，并在 pingguye.cn 上放一个「危机预演 / crisis-rehearsal」落地页（首屏：一句话 + demo 命令 + `github.com/yepinggu66/crisis-rehearsal` 按钮 + 联系邮箱）。没有落地页就保持 A。

---

## 4. Discussions（必须开）

Settings → Features → ✅ Discussions。

建议分类（Categories）：

| 分类 | 格式 | 用途 |
|---|---|---|
| 📣 Announcements | Announcement | 版本发布、数据更新（只有 maintainer 能发） |
| ❓ Q&A | Question / answer | 安装、数据复算、`crh` 用法 |
| 💡 Ideas | Open discussion | 场景包、政府版需求 |
| 🏛️ Government & enterprise pilots | Open discussion | 采购/试点询问（承接 `government_pilot` issue） |
| 🔬 Show your rehearsal | Open discussion | 用户贴自己的场景包/报告（增长素材） |

**种子帖（发布当天发）：**
1. `Welcome — start here`（置顶）：一句话定位、`crh demo` 命令、证据目录（`data/repeat_v02/`、`data/failures.md`）、诚实限制摘要、提问前先跑 demo。
2. `What would you rehearse?`：征集场景（医院、供应链、数据泄露、出海舆情），收集需求也收集 star。
3. `Pilot program (design, not a claim)`：说明企业/政府 pilot 的**设计稿**路径，明确「未认证、无政府案例」。

**规则：** 开 Discussion 不需要额外文件；但在 README 里加 Discussions 链接是 W2 的事（不要越界改 README）。

---

## 5. Projects（可选，建议 1 个看板）

Projects → New project（Table 视图）→ 字段：

| 字段 | 类型 | 选项 |
|---|---|---|
| Status | Single select | Inbox / Triaged / In progress / Blocked / Shipped |
| Type | Single select | bug / feature / data-integrity / government-pilot / docs |
| Sector | Single select | enterprise / government / developer / research |
| Priority | Single select | P0 / P1 / P2 |
| Target | Text | v0.3.0 / v0.3.1 / v0.4.0 |

**意义：** 让外部看到「这仓库有人在维护」。单人维护时只建看板、不承诺 SLA。

---

## 6. 置顶 issue 文案（Pin 2 个）

### Pin 1：`Start here — what this is, what it is not (v0.3.0)`

```markdown
## 60-second check (no API key, offline)

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo
`crh demo` 会校验证据包（`crh verify`）、复算已发布统计（`crh stats`）、生成 4 份自包含 HTML 演练档案 + 索引页。全程离线、无 API key、<10 秒。

## The numbers, with their error bars

- Top-3 risk hit rate **82.2%** — 95% CI **78.5–85.9**, event-mean graded score, n=30 events × 3 repeats. **不是**二值命中率、**不是**对未来事件的概率。
- 90 runs = 30 events × 3 repeats；统计单元是事件，不是 90 个独立样本。
- 只有 **5/30（17%）** 事件在三次运行中完全一致；within-event SD 0.26/3。
- 内部稳定性 **STA 58**，低于自设及格线 60 → **failed**。
- 失败案例在 `data/failures.md`，原文公开。

## What it is not

- 不是预测工具，不预测「下一个危机是什么」。
- 不是已认证产品：`docs/enterprise/compliance.md` 只是标准要求映射，**未认证、未测评**。
- 没有政府/客户案例；`docs/government.md` 是设计稿。
- LLM judge 尚未人工校准（`data/judge_calibration.md`）。

## Where to go next

- 企业/政府试点：见 `docs/enterprise/overview.md` 与 `docs/enterprise/procurement.md`
- 报 bug / 提需求：Issues 模板（bug / feature / government_pilot）
- 安全漏洞：请**不要**开 issue，见 `SECURITY.md`
- 讨论：Discussions → Q&A / Ideas

维护者：[PingguYe](https://x.com/PingguYe) · 联系：yepinggu@outlook.com
```

### Pin 2：`Roadmap v0.3.0 → v0.4.0 (and what we refuse to promise)`

```markdown
## v0.3.0 (this release)
- 可安装 CLI `crh`（verify / stats / report / demo / pack init|validate）
- 自包含 HTML 演练档案；场景包 schema；证据 sha256；离线 demo

## v0.3.x (bugfix only)
- 修复安装/编码/路径问题；不新增叙事

## v0.4.0 (planned, no dates promised)
- 人工校准 judge（`data/judge_calibration.md` 的模板）
- 非中文市场事件 ≥5 起（欢迎 PR，见 issue #3）
- 重新跑 agent-interview 步骤（见 issue #1）

## What we refuse to promise
- 不承诺「预测准确率」，只承诺可复算的回测与稳定的交付流程（3–5 runs 读共识）
- 不承诺认证/等保/SOC2；只提供要求映射与 gap 清单
- 不承诺 SLA，直到有付费合同
```

---

## 7. 社交预览图 brief（1280×640）

**当前状态（已核对）：** `docs/assets/social-preview.png` 存在，**1280×640 px**，163,872 bytes；源文件 `docs/assets/social-preview.html` 可改。**尚未上传到 GitHub**（Settings → General → Social preview 需要 Lead 手动上传）。

### 要求（GitHub 规范）
- 尺寸 **1280×640**（最小 640×320），比例 2:1；PNG/JPG/GIF，建议 <1 MB。
- 重要文字放在**中央安全区**：四周各留 ≥64 px；因为在 LinkedIn/Twitter 卡片里会被裁切。
- 深色底（与 README 一致）：`#0b1220`；强调色 `#7fd4ff`；正文字号 ≥28 px，标题 ≥64 px。
- **不出现**：客户 logo、政府徽标、认证徽章（ISO/SOC2/等保）、star 数、夸张词（revolutionary / world's first）。

### 建议文案（三选一，与现有源文件一致）
1. **主推（已实现）**：`Rehearse the crisis 72 hours before it happens.` + 三个数字块 `30 events / 90 runs / 82.2%`（标注 `95% CI 78.5–85.9`）+ 底栏 `github.com/yepinggu66/crisis-rehearsal` + `AGPL-3.0 · runs on your infrastructure`。
2. v0.3.0 更新版：把副标题换成 `One command, offline, no API key: crh demo`，证明「能跑」优先于数字。
3. 中文版（用于微信/知乎分享）：`把危机提前 72 小时演一遍` + `30 起公开危机回测 · 82.2% (78.5–85.9) · 离线可跑`。

### 上传步骤
Settings → General → **Social preview** → Upload image → 选 `docs/assets/social-preview.png` → 保存。
上传后在 X/LinkedIn/微信发链接会显示该图；**发布前先用 `https://cards-dev.twitter.com/validator`（或任意 OG 预览工具）检查裁切与可读性。**

---

## 8. 其他仓库设置清单

| 设置 | 位置 | 建议值 | 理由 |
|---|---|---|---|
| Issues | Settings → Features | ✅ On | 外部反馈入口；模板见 `.github/ISSUE_TEMPLATE/` |
| Discussions | Settings → Features | ✅ On | 承接问答与 pilot 询问 |
| Wiki | Settings → Features | ❌ Off | 文档都在 `docs/`，避免双源 |
| Sponsorships | Settings → Features | 视情况 | 开源核心 AGPL，商业在报告/工作坊；`FUNDING.yml` 里只留注释模板 |
| Releases | 主页右侧 | 发布 `v0.3.0` | 附 sdist、demo 视频、social-preview.png；Release notes 用诚实口径 |
| Topics | About 齿轮 | 见 §2 的 20 个 | 上限 20 |
| Social preview | Settings → General | 上传 1280×640 | 见 §7 |
| License | 已识别 | AGPL-3.0 | **任何文案不得写 Apache/MIT** |
| SECURITY.md | 仓库根 | 必须有（W2 交付） | 漏洞不走 issue |
| Branch protection | Settings → Branches | 保护 `main`：要求 CI status | 单人维护也要防止把红 CI 合进去 |
| Dependabot | Settings → Code security | 开 alerts | 提醒依赖/actions 风险 |
| Actions permissions | Settings → Actions | 只允许本仓库 workflows | 供应链最小权限 |
| `crh demo` CI 徽章 | README（W2 写） | `![CI](https://github.com/yepinggu66/crisis-rehearsal/actions/workflows/ci.yml/badge.svg)` | 让访客看到「真的在跑」 |

---

## 9. 首次发布操作顺序（Lead 执行）

1. 合并 W1/W2 → 确认 CI 绿。
2. 按 §1 设置 About（EN-1）+ §2 topics + §3 Homepage（B，若落地页就绪）。
3. 上传 §7 社交预览图。
4. 开 Discussions（§4）+ Pin 两条 issue（§6）。
5. 建 `v0.3.0` Release（tag `v0.3.0`，附 sdist/demo 视频/social-preview）。
6. 用 `posts/hn.md` 的发布日流程：HN（美东周二/周三上午）→ X EN 线程 → 次日知乎/即刻。
7. 发布后 24h 内：回所有评论/issue；把真实问答补进 Discussions 置顶帖。
8. 每周一按 `README.md` §6 记录数据。
