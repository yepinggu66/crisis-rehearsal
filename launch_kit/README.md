# 危机预演 v0.3.0 · 发布增长包（Launch Kit）

> **本目录只装「可直接复制发布」的资产，不替 Lead 执行发布。** 所有 commit / tag / push / 发帖 / star / PR 由 Lead（仓库所有者）人工完成。
> 基线：`0e2341f`（main）→ 目标版本 `v0.3.0`。侦察数据截至 **2026-10-31 01:51 Asia/Shanghai**（见 `00-star-benchmark.md`）。
> 诚实红线：本包不放任何客户名、政府背书、认证、准确率之外的「效果」承诺。每条对外文案里的数字都能在仓库里对上。

---

## 1. 资产索引

| 文件 | 作用 | 状态 | 前置依赖 |
|---|---|---|---|
| `00-star-benchmark.md` | 真实 API 侦察：本仓库 + 13 个同类仓库 + 20 个 topic 规模 | ✅ 可用 | 无（数据为 2026-10-31 快照） |
| `recon/api-snapshot-2026-10-31.json` | 上述数据的原始 API 返回（star/fork/topics/traffic/issues/releases） | ✅ 可用 | 无 |
| `recon/measurements.md` | 周度数据记录模板（stars/views/clones/渠道归因/企业漏斗）+ 数据纪律 | ✅ 模板可用（Lead 每周填真实数） | 无 |
| `README.md`（本文件） | 资产索引 + 90 天分发计划 + 30/90/180 天目标与依据 | ✅ 可用 | 无 |
| `repo-settings.md` | About 描述（EN/ZH 各 3 版）、topics、Homepage、Discussions/Projects、置顶 issue、社交预览图 brief | ✅ 可用 | Lead 在 GitHub UI 操作 |
| `posts/hn.md` | Show HN 文案 + 首评 FAQ + 发布时机 + HN 规则核对 | ✅ 可用 | `crh demo` 可跑、demo 素材 |
| `posts/reddit.md` | r/MachineLearning、r/LocalLLaMA、r/riskmanagement、r/China 分版文案 + 版规注意 | ✅ 可用 | 同上 |
| `posts/x.md` | 英文线程 + 中文两条线程（PingguYe 口吻） | ✅ 可用 | 社交预览图、demo 视频/截图 |
| `posts/linkedin.md` | CRO/PR/IR 版 + CISO/CIO/合规版 | ✅ 可用 | docs/enterprise/* |
| `posts/zhihu.md` | 知乎文章/回答（长文，方法 + 失败公开） | ✅ 可用 | 同上 |
| `posts/wechat.md` | 公众号长文（1000–1500 字） | ✅ 可用 | 同上 |
| `posts/jike.md` | 即刻短帖（3 版） | ✅ 可用 | 社交预览图 |
| `awesome-lists.md` | ≥15 个可提 PR 的 awesome list + 栏目核对 + PR 文案 + 门槛 | ✅ 可用 | 需人工 fork/PR；建议发布后 2 周再提 |
| `demo-script.md` | 60–90 秒录屏逐镜头脚本 + 终端 transcript（已用 `docs/assets/cli-demo.txt` 真实输出，0.16s / 43 文件校验） | ✅ 可用 | W1 `crh demo` 实跑输出（已核对） |
| `enterprise-outreach.md` | 3 封冷邮件（中 2 + 英 1）+ 1 页 pilot 提案 + 30 分钟会议议程 | ✅ 可用 | docs/enterprise/*、docs/government.md |
| `issue-triage.md` | 现有 3 个 open issue 处理建议 + 首个外部 issue 响应模板 + 标签体系 | ✅ 可用 | Lead 在 GitHub 建 labels |
| `.github/ISSUE_TEMPLATE/{bug,feature,government_pilot,config}.yml` | YAML issue forms（含安全漏洞不走 issue 的提示） | ✅ 可用 | Lead 合并后生效 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 模板（数据不可改、数字可复算、贴 `crh verify`） | ✅ 可用 | 同上 |
| `.github/FUNDING.yml` | 赞助入口（当前无赞助信息 → 注释模板） | ✅ 可用 | Lead 决定是否开通 |

---

## 2. 发布前置条件（Lead 必须先完成，否则本包文案里的命令不成立）

- [ ] **W1 合并**：`pipx install git+https://github.com/yepinggu66/crisis-rehearsal` 成功（或 clone + `pip install -e .`）；`crh --version` → `crh 0.3.0`；`crh verify` / `crh stats` / `crh demo` 实跑通过（离线、无 API key、<10s）。
- [ ] **W2 合并**：README/README-ZH、`docs/enterprise/*`、`docs/government.md`、`SECURITY.md`、`CONTRIBUTING.md`、`CITATION.cff` 进 main。
- [x] `docs/assets/cli-demo.txt` 已生成（W1 产出，2026-10-31 核对：43 files OK / `crh demo` 0.16s）；`docs/assets/architecture.svg`、`docs/assets/social-preview.png`（1280×640，已核对）已就位。
- [ ] 决定 PyPI：**当前未发布 PyPI**，所有文案统一用 README 的两行：`pipx install git+https://github.com/yepinggu66/crisis-rehearsal` + `crh demo --out demo`（无 pipx 时用 clone + `pip install -e .`）；**若已发布 PyPI**，才可写 `pip install crisis-rehearsal`。发布包默认按「未发布 PyPI」写，避免虚假命令。
- [ ] GitHub 设置按 `repo-settings.md` 完成：About、topics（≤20）、Homepage、Social preview、Discussions、置顶 issue。
- [ ] `v0.3.0` Release：tag、release notes（诚实数字 + 限制）、附件（sdist、`backtest_chart.png`、60–90s demo 视频、social-preview.png）。
- [ ] 60–90 秒 demo 录屏完成（按 `demo-script.md`），作为 Release 附件 + README 顶部链接。
- [ ] 全部对外文案过一遍 §9 红线和 `00-star-benchmark.md` 的数字口径（尤其 82.2% 必须带 CI 与「event-mean graded score」说明）。

---

## 3. 两条漏斗（不要混在一起看）

### 漏斗 A：开发者拿星（GitHub / HN / Reddit / X / 社区）

```
曝光（帖子/清单/搜索） → repo 页面（README 前 40 行 + 社交图 + demo 命令）
→ 120 秒内 clone/pip → crh demo 跑出 HTML → star（↔ issue/转发）
```

- 现状断点（真实数据）：14 天 40 views / 7 uniques / 114 clones / 55 unique cloners，**外部 star = 0**。clone 的人没有在 60 秒内看到「值得 star 的东西」。
- v0.3.0 的修复动作：`crh demo` 一条命令离线出 4 份 HTML 档案；README 顶部 40 行给出「是什么 / 为什么现在 / 30 秒怎么跑」；社交预览图 + demo 视频。
- 目标转化（**假设，需用 4 周数据校准**）：repo view → star **2%–5%**（开发者工具常见区间）；demo 执行者 → star **>30%**（跑出结果的人最可能 star）。

### 漏斗 B：企业/政府线索（LinkedIn / 公众号 / 知乎 / 冷邮件 / 采购渠道）

```
曝光（决策者内容） → docs/enterprise + docs/government → government_pilot issue / 邮件
→ 30 分钟会 → 2 周离线 POC → 付费 pilot
```

- 现状：0 条外部线索；`docs/enterprise/*` 与 `docs/government.md` 为 v0.3.0 新增（设计说明，未认证、无政府案例）。
- 目标（90 天）：**5–10 个有效对话**（能说清部署环境与场景）、**2 份书面 pilot 提案**、**1 个 2 周离线 POC**；不承诺签约。
- 关键：漏斗 B 的转化与 star 数**无关**。不要拿 star 数当企业背书，也不要用企业话术污染开发者文案。

---

## 4. 30 / 90 / 180 天 star 目标（区间 + 依据 + 不确定性）

### 4.1 目标表

| 时间点 | 保守（只做 README+1 个渠道） | **基准（执行本计划）** | 上行（HN 首页 或 中文爆款） |
|---|---:|---:|---:|
| 30 天（2026-11-30 前） | 8–20 | **20–45** | 80–150 |
| 90 天（2027-01-29 前） | 30–70 | **100–200** | 300–600 |
| 180 天（2027-04-29 前） | 60–120 | **200–400** | 600–1,000 |

> 这些是**计划区间，不是承诺**。对外（README、帖子）不写 star 目标；只在内部用。

### 4.2 依据（全部可查）

1. **品类引力接近零**：GitHub `crisis-simulation` topic 共 12 个仓库、最高 11 star；`tabletop-exercise` 最高 1,258 star（attackgen）。→ 靠品类自然搜索拿不到量。
2. **最接近的可比对象是 attackgen**：TTX 品类第一、有可跑 demo、有明确买家词，近 30 天新增约 13 star（WatchEvent 采样 0.41/d，按同速率 90 天约 +39）。→ 基准目标 100–200 是它的 **2.5–5 倍**，靠 8 个渠道首发 + awesome list 收录 + README 重写兑现；上行（300–600）才需要 HN 首页或中文爆款。
3. **本仓库当前无 GitHub 社交资产**：owner `yepinggu66` followers = **2**，无组织背书，无历史 repo 流量。→ 不能指望 GitHub 站内推荐，必须外部引流。
4. **渠道容量假设（必须用真实数据校准）**：
   - HN：Show HN 进 front page 概率按 **20%–35%** 计；进首页时 24h 约 3k–15k 浏览、star 转化 1%–3% → 30–450 star；未进首页约 100–500 浏览、≤5 star。→ 期望值约 60 star（基准的主要方差来源）。
   - Reddit（3–4 个版）：单帖 200–2,000 浏览，0.5%–2% → 每帖 1–20 star。
   - X：PingguYe 账号真实粉丝数需 owner 提供（无法从 API 核实）；<5k 时按 0–15 star/线程计。
   - 知乎/公众号/即刻：需 owner 提供阅读基线；冷启动按 0–30 star/篇计。
   - awesome list：每个收录 90 天内约 5–30 star（长尾，复利）。
   - 搜索/topic 自然流量：每月约 5–20 star（README 重写后才会发生）。
   → 基准模型加总约 **90–180**，取 100–200；保守 = 砍掉 HN 与中文渠道；上行 = HN 进首页 + 一篇中文爆款叠加。
5. **历史参照**：本仓库 6 天 1 star（owner 自己），0 外部转化；v0.2 的 55 个 unique cloner 没有 star —— 说明**产品体验**而非「宣传语」是当前瓶颈。

### 4.3 领先指标（比 star 更早告诉你计划是否有效）

| 指标 | 周基准 | 采集方式 | 若低于基准怎么办 |
|---|---:|---|---|
| repo views / 周 | 300+（发布会后 2 周起） | `gh api repos/…/traffic/views` | 渠道文案/标题问题 → 换标题、换社区 |
| clone 或 `crh demo` 执行 / 周 | 30+ | `gh api …/traffic/clones` + 用户回报 | 安装路径太长 → 优先发 PyPI / 简化命令 |
| view → star | ≥1.5% | star 增量 ÷ views | README 前 40 行/社交图问题 |
| 外部 issue / 周 | ≥1 | issues API | 没有反馈 = 没有真实用户 → 回到 demo 质量 |
| awesome list 收录 | ≥1/2 周 | 人工记录 | PR 被拒 → 修条目格式，再试下一家 |

### 4.4 Kill / Scale 规则

- **第 2 周末**：全渠道累计 views < 300 → 停止铺量，只保留 HN + 知乎 + 2 个 awesome list，把精力放回「demo 体验 + README 首屏」。
- **第 4 周末**：90 天进度 < 30 star → 不追加渠道预算，改用「每周 1 篇方法长文 + 1 个真实事件复盘」的慢内容策略。
- **任意时点**：单渠道带来 ≥50 star → 下一周把同类内容加频（同渠道 60% 精力），不要平均用力。
- **禁止**：买 star、互 star 群、投票互赞、伪造下载量/引用数。GitHub ToS 与 HN 规则都明确禁止。

---

## 5. 90 天分发计划（按周；负责人默认 Lead/PingguYe）

> 生产环境假设：单人维护。每周固定 3 个内容产出 + 1 次数据记录。所有时间以 Asia/Shanghai 标注，HN/Reddit 需换算美东时间。

| 周 | 阶段 | 渠道与动作 | 预期指标 | 成功判据 |
|---|---|---|---|---|
| **W0**（11-01→11-07） | 准备 | 合并 W1/W2；部署 GitHub 设置（About/topics/social preview/Discussions/置顶 issue）；录 60–90s demo；发 `v0.3.0` Release；`crh demo` 在三台干净机器复跑 | 发布条件全绿 | Release 上线；demo 可播；`crh demo` 通过 |
| **W1**（11-08→11-14） | 首发 | **周二/周三美东 08:00–10:00** Show HN（`posts/hn.md`）；同天 X 英文线程；T+1 回 HN 评论（AMA 式）；T+2 知乎长文 + 即刻短帖 | HN 进 front page（20–35% 概率）；repo views ≥800 | HN 存活 >3h 或 ≥20 comments；views ≥500 |
| **W2**（11-15→11-21） | 扩散 | Reddit 3 版（r/MachineLearning [P]、r/LocalLLaMA、r/riskmanagement；错开 48h，不跨版同文）；公众号长文；X 中文线程 A | 每帖 ≥5 有效评论；views ≥600 | 至少 1 个版不被删；外部 issue ≥2 |
| **W3**（11-22→11-28） | 长尾 | X 中文线程 B（诚实数字/失败复盘）；LinkedIn 2 版；开始向 5 个 A 类 awesome list 提 PR（间隔 ≥48h） | 线索 ≥2；star ≥15（30 天目标进度） | LinkedIn ≥1 次 CRO/CISO 层面互动；1 个 list 合并 |
| **W4**（11-29→12-05） | 校准 | 记录 30 天数据；按 §4.4 决定加码/收缩；发第 2 篇知乎（技术拆解：local graph adapter / 评判协议） | 30 天 star 落点 20–45 | 数据写进 `recon/measurements.md` |
| **W5–W6**（12-06→12-19） | 企业漏斗 | 冷邮件第一批 20 封（中 12 + 英 8，按 `enterprise-outreach.md`）；LinkedIn 第 3 版（pilot 邀请）；准备 1 页 pilot 提案 | 回信率 ≥8%；≥2 通 30 分钟会 | 2 份书面 pilot 提案 |
| **W7–W8**（12-20→01-02） | 第二波 | HN 不重复发；发第 3 篇长文（「30 起危机回测的 5 个失败模式」）；reddit r/tabletop 或 r/cybersecurity 讨论帖（不发链接，先给方法） | views 累计 ≥2,500；star ≥60 | 外部 issue ≥5；≥1 个 POC 进入排期 |
| **W9–W10**（01-03→01-16） | 清单复利 | 剩余 B 类 awesome list PR（每次 1–2 个）；GitHub Collections 候选；找 1 个 newsletter 提及（次选） | star ≥90 | 收录 ≥3 个清单 |
| **W11–W13**（01-17→01-29） | 收口 | 90 天复盘（发布 `launch_kit/recon/measurements.md` 摘要到 issue/Discussions）；准备 v0.3.1（只修 bug，不新增叙事）；企业漏斗跟进 | 90 天 star 落点 100–200 | 5–10 个有效企业对话；1 个 POC 启动 |

### 5.1 内容日历（发布后 14 天，防止同稿多投被判定 spam）

| 日 | 渠道 | 内容 | 注意 |
|---|---|---|---|
| D0（周二/三） | HN + X EN | Show HN + EN 线程 | HN 标题必须以 `Show HN:` 开头；不发投票请求 |
| D1 | HN 评论区 | 首评 FAQ（自己发第一条实质评论）+ 回所有问题 | 必须在线 3–4h |
| D2 | 知乎 + 即刻 | 方法长文 + 短帖 | 知乎不放外链堆砌，正文给结论 |
| D3 | GitHub Discussions | 开「Ask the maintainer / 首个外部 issue」帖 | 置顶后可承接流量 |
| D4 | 公众号 | 长文（1000–1500 字） | 预告「下期：失败模式」 |
| D6 | Reddit r/MachineLearning | [P] Project 帖 | 版规以当日为准；先看版内近 30 天同类帖 |
| D8 | Reddit r/LocalLLaMA | 强调离线/无 API key demo | 不重复 D6 文案 |
| D10 | LinkedIn | CRO/CISO 2 版分两次发（间隔 3 天） | 不用「revolutionary」「world's first」 |
| D12 | X 中文线程 | 「我们把自己失败也发了」 | 带 STA 58 与 17% 数字 |
| D14 | 数据记录 | 30 天中期数据 | 更新 `recon/measurements.md` |

### 5.2 渠道优先级

| 级别 | 渠道 | 理由 | 发布节奏 |
|---|---|---|---|
| **P0** | HN Show HN | 开发者密度最高；能验证「60 秒 tryable」；规则明确 | 仅 1 次（大改版才可再发） |
| **P0** | 知乎 + 公众号 | 中文决策者与开发者双覆盖；企业线索主渠道 | 每周 ≤2 篇 |
| **P0** | GitHub 仓库设置 + Release + 清单收录 | 所有渠道的落地页；复利资产 | 一次性 + 每 2 周补 |
| **P1** | Reddit（精选 3 版） | 垂直反馈质量高；易被判定自宣，需间隔与版本化 | 每周 1 版 |
| **P1** | X（EN + 中文） | 建立 PingguYe 个人品牌；英文线程可被转推 | 每周 2–3 条/1 线程 |
| **P1** | LinkedIn | 企业/政府决策者，漏斗 B | 每 3–4 天 1 条 |
| **P2** | 即刻、 newsletters、GitHub Collections | 补充曝光 | 有素材才发 |
| **不做** | 微信群互 star、买 star、批量 cold DM、r/China 政治话题 | 违规/伤品牌/无转化 | — |

---

## 6. 度量与复盘

每周一 10:00 记录一次（命令可直接跑）：

```powershell
gh api repos/yepinggu66/crisis-rehearsal --jq '{stars: .stargazers_count, forks: .forks_count, issues: .open_issues_count}'
gh api repos/yepinggu66/crisis-rehearsal/traffic/views
gh api repos/yepinggu66/crisis-rehearsal/traffic/clones
gh api repos/yepinggu66/crisis-rehearsal/issues --jq '.[] | {number, title, created_at}'
```

记录到 `launch_kit/recon/measurements.md`（Lead 建表，字段：日期 / stars / views / uniques / clones / 外部 issue 数 / 本周渠道与产出 / 结论 / 下周动作）。**只记录真实数，不美化。**

复盘问题（每 2 周）：
1. 哪个渠道带来了可归因的 views / star？（GitHub referrers API 可辅助，但多数是 direct）
2. `crh demo` 是否被真实执行？有没有人贴输出/截图？
3. 企业漏斗：有几封邮件进入「愿意开会」状态？卡在哪个问题（部署/合规/价格/效果）？

---

## 7. 已知风险与应对

| 风险 | 影响 | 应对 |
|---|---|---|
| 安装命令与 README 不一致导致失败 | 直接伤信任 | 统一用 README 的 `pipx install git+…` + `crh demo --out demo`；clone + `pip install -e .` 只作 fallback；PyPI 发布后再改文案 |
| `crh demo` 在 Windows 中文路径/编码出错 | 首发日最致命 | 发布前在干净 Windows + Linux 各跑一次；README 给 PowerShell/Bash 两版 |
| HN 判定为「landing page/宣传」 | 帖被删/无人理 | Show HN 只发「可跑的东西」；首评给方法、限制、失败，不推销 |
| 中文渠道被判定营销 | 限流 | 长文以方法/复盘为主，仓库链接放文末 |
| 政府/企业文案被理解为「已认证/已合作」 | 合规风险 | 只用 `docs/enterprise/compliance.md` 的映射表措辞；明确「未认证、无政府案例」 |
| 17% 稳定性被对手/评论者攻击 | 舆情 | 主动公开：这是设计选择（3–5 跑读共识），不是隐藏缺陷 |
| awesome list PR 被拒 | 浪费时间 | 先 star/watch 目标 list ≥2 周；按 `awesome-lists.md` 的格式逐条提交；一次 1 家 |

---

## 8. 数字口径速查（写任何文案前核对）

| 说法 | 正确写法 | 禁止写法 |
|---|---|---|
| 82.2% | 「Top-3 risk hit rate **82.2%**，95% CI **78.5–85.9**，event-mean graded score，n=30 events × 3 runs」 | 「准确率 82.2%」「预测准确率」「概率 82.2%」 |
| 90 runs | 「90 runs = 30 events × 3 repeats；统计单元是 30 个事件」 | 「90 个独立样本」 |
| 17% | 「只有 5/30 事件在三次运行中完全一致」 | 「复现率 17%」（会被误解为完全可复现） |
| STA 58 | 「内部稳定性 STA 58，低于自设及格线 60 → failed」 | 「STA 58 分，接近及格」 |
| 失败案例 | 「`data/failures.md` 公开了漏报与误报」 | 「没有失败案例」 |
| 企业/政府 | 「设计说明 / roadmap，**未认证、未测评、无政府案例**」 | 「符合等保」「已服务政府」 |
| 成本 | 「~$0.03/事件（DeepSeek API）、~4 分钟/次」 | 「零成本」「实时」 |
| demo | 「`crh demo` 离线、无 API key、<10s」 | 「一键预测」「实时预警」 |
