# 00 · Star Benchmark — 危机预演 vs. 同类仓库（真实 API 侦察）

> **抓取时间：2026-10-31 01:51 (Asia/Shanghai) / 2026-10-30 17:51 UTC**
> **抓取方式：GitHub REST API，`gh api`，账号 `yepinggu66`（已登录）。**
> **原始返回：本目录 `recon/api-snapshot-2026-10-31.json`（84 KB，含下列全部关键字段）。**
> 本文件里每个 star / fork / 日期都来自该快照；没有一个是凭记忆写的。

---

## 1. 本仓库现状（subject repo）

来源：`GET /repos/yepinggu66/crisis-rehearsal`、`/traffic/*`、`/issues`、`/releases`。

| 字段 | 值 |
|---|---|
| full_name | `yepinggu66/crisis-rehearsal` |
| **stars** | **1**（唯一 star 是 owner 自己，2026-10-26T00:32:43Z） |
| forks | 0 |
| watchers (subscribers) | 0 |
| open issues | 3（全部是 owner 自己建的 roadmap issue，#1/#2/#3） |
| created_at | 2026-10-25T17:22:56Z（仓库只有 6 天） |
| pushed_at | 2026-10-27T15:44:37Z |
| license | AGPL-3.0 |
| homepage | `https://youtu.be/pj7PKonS2Ns`（YouTube demo） |
| topics | agent-based-modeling, ai-agents, crisis-management, crisis-simulation, llm, llm-evaluation, multi-agent-simulation, public-relations, reproducibility, swarm-intelligence |
| releases | `v0.1.0`（2026-10-25）、`v0.2.0`（2026-10-26），均有 release notes、无 star 转化 |

**14 天流量（Traffic API，2026-10-16 → 2026-10-29）：**

| 指标 | 数值 |
|---|---|
| views / unique visitors | 40 / 7 |
| clones / unique cloners | 114 / 55 |
| referrers | github.com 8（1 unique）、pingguye.cn 3（2）、t.co 1、一个 cloudflare 临时域名 1 |

解读：**有 55 个 unique cloner，却只有 0 个外部 star。** 说明「clone → 读懂 → star」这条链在 v0.2 断了：clone 的人拿到的是一份要 6 小时才能复现的研究包，不是 60 秒能验证的产品。这正是 v0.3.0 要修的东西，也是本增长包存在的理由。

---

## 2. 决定性事实：这个细分赛道的「star 引力」接近零

来源：`GET /search/repositories?q=topic:<topic>&per_page=1`（repo 数量），以及 topic 内按 star 排序的前 8 名。

| topic | 使用该 topic 的仓库数 | 该 topic 最高 star 仓库 |
|---|---:|---|
| `crisis-simulation` | **12** | bagusardin25/TeamDynamics — **11** |
| `crisis-management` | 146 | hevnsnt/Awesome_Incident_Response — 298（清单，非产品） |
| `tabletop-exercise` | 36 | mrwadams/attackgen — 1,258（网络安全 TTX） |
| `public-opinion-analysis` | 17 | 666ghj/MiroFish — 82,851（已跳出细分） |
| `multi-agent-simulation` | 151 | 666ghj/MiroFish — 82,851 |
| `social-simulation` | 170 | camel-ai/oasis — 5,366 |
| `generative-agents` | 131 | camel-ai/oasis — 5,366 |
| `agent-based-simulation` | 708 | chrxh/alien — 5,561 |
| `agent-based-modeling` | 1,557 | mesa/mesa — 3,928 |
| `swarm-intelligence` | 850 | 榜单被通用 AI/优化类仓库占据，无危机预演项目 |
| `llm-evaluation` | 8,874 | 极宽，不是精准流量 |
| `llm-agents` | 8,180 | 极宽，竞争激烈 |
| `emergency-management` | 207 | 无 LLM 产品进入前列 |
| `disaster-response` | 603 | 无 LLM 产品进入前列 |
| `wargaming` | 120 | 桌面/军事模拟为主 |
| `public-relations` | 64 | 无开发者向产品 |
| `risk-management` / `incident-response` / `simulation` | 5,263 / 7,518 / 30,636 | 泛化 topic，不做主定位 |

**结论 1：`crisis-simulation` 全 GitHub 只有 12 个仓库、最高 11 star。** 靠「危机预演」这个品类本身做自然增长，天花板个位数。任何「30 天 1000 star」的承诺都是拍脑袋。

**结论 2：star 在相邻赛道。** 我们要借的流量池按大小排：
1. `agent-based-simulation`（708 repos）与 `social-simulation`（170）——oasis / concordia / mesa 的读者；
2. `llm-agents` / `llm-evaluation`（8,000+）——开发者池子最大，但注意力最散；
3. `tabletop-exercise` / `crisis-management`（36 / 146）——企业安全与应急买家的词，不是开发者的词。

所以分发策略是：**用「可跑的 demo + 诚实的回测」进入 agent/simulation 开发者视野；用「企业/政府预演」进入采购视野。两条漏斗，不同渠道。**

---

## 3. 同类仓库真实数据（13 个对照 + 本仓库）

来源：`GET /repos/<owner>/<repo>`；「近期采样速度」来自 `GET /repos/<owner>/<repo>/events`（最多取 300 条公开事件，数其中 `WatchEvent`，按首尾时间算日均）。

> ⚠️ 方法说明：GitHub 的 `/stargazers` 时间戳接口在本环境对非 owner 仓库返回 404，无法逐 star 取时间。因此「近期采样速度」是用 **public events 里的 WatchEvent 样本**估的，窗口长度各仓库不同（0.4–30 天），只用于判断量级，**不用于精确预测**；「历史日均」= 当前 star ÷（创建至今的天数），是粗粒度基线。两者并列展示，避免单一数字误导。

| 仓库 | stars | forks | 创建日 | 历史日均 | 近期采样速度 | 定位 |
|---|---:|---:|---|---:|---:|---|
| 666ghj/MiroFish | **82,851** | 12,532 | 2025-11-26 | 244.6/d | **193.3/d**（样本 1.3 天） | 群体智能预测，现象级爆款 |
| 666ghj/BettaFish | 42,546 | 7,608 | 2024-07-01 | 50.0/d | 13.4/d（样本 18.3 天） | 舆情分析多 agent |
| joonspk-research/generative_agents | 22,312 | 3,128 | 2023-07-23 | 18.7/d | — | 斯坦福生成式 agent |
| camel-ai/camel | 17,996 | 2,130 | 2023-03-17 | 13.6/d | — | 多 agent 框架（组织站台） |
| **camel-ai/oasis** | **5,366** | 655 | 2024-11-13 | 7.5/d | **5.8/d**（样本 30.1 天） | 社交媒体群体模拟框架（本仓库上游之一） |
| chrxh/alien | 5,561 | 192 | 2020-10-19 | 2.5/d | — | 人工生命/CUDA 模拟 |
| mesa/mesa | 3,928 | 1,351 | 2014-09-19 | 0.9/d | — | ABM 学术框架（12 年） |
| google-deepmind/concordia | 1,843 | 397 | 2023-11-21 | 1.7/d | 3.3/d（样本 28.5 天） | DeepMind 社交模拟库 |
| mrwadams/attackgen | 1,258 | 170 | 2023-08-08 | 1.1/d | **0.4/d**（样本 29.2 天） | 安全事件桌面演练生成（最接近的「TTX 工具」品类第一） |
| tsinghua-fib-lab/LLM-Agent-Based-Modeling-and-Simulation | 305 | 35 | 2024-07-30 | 0.37/d | 0.16/d（样本 12.2 天） | LLM+ABM 论文清单 |
| bagusardin25/TeamDynamics | 11 | 2 | 2026-04-06 | 0.05/d | — | 危机模拟 + 多 agent（直接竞品形态） |
| ColinM-sys/StraitOfConsequences | 4 | 2 | 2026-04-25 | 0.02/d | — | 危机推演 hackathon 项目 |
| IcebergAI/IcebergTTX | 3 | 0 | 2026-05-11 | 0.02/d | — | 网络安全桌面演练 |
| **yepinggu66/crisis-rehearsal** | **1** | 0 | 2026-10-25 | 0.17/d | — | 本仓库（v0.2 研究包） |

### 3.1 四种增长形态（这是目标区间的全部依据）

| 形态 | 代表 | 速度 | 它靠什么 |
|---|---|---|---|
| A. 现象级爆款 | MiroFish / BettaFish | 190 / 13 star/日 | 强视觉产品 + 中文社区病毒传播 + 大 V/媒体；不可复制，不能当计划 |
| B. 机构/框架型 | oasis / camel / concordia | 3–8 star/日 | 组织背书 + 论文 + 持续发布会；有长期复利 |
| C. 细分工具型 | attackgen（TTX 品类第一） | **0.4–1.1 star/日** | 一个明确买家词 + 可跑 demo + 安全社区口碑；**这是本仓库最现实的对标** |
| D. 无分发小项目 | TeamDynamics / StraitOfConsequences / IcebergTTX | 0.02–0.05 star/日 | 只靠仓库存在，无人知道；**和本仓库当前状态同类** |

**关键对照：** 品类第一的 attackgen 三年累计 1,258 star，近 30 天新增约 13 star。一个「危机预演」仓库若没有超出品类第一的分发力度，90 天到 100–200 star 就已经是**好成绩**；到 1,000+ 需要现象级传播，不在可控范围内。

### 3.2 本仓库与竞品的差异化（写文案时的真实卖点）

| 维度 | MiroFish | oasis | attackgen | 本仓库 v0.3.0 |
|---|---|---|---|---|
| 可 60 秒验证 | 否（需装环境） | 否（需 API key） | 是（Streamlit） | **是：`crh demo`，离线 <10s，无 key** |
| 公开回测 + 失败案例 | 无 | 无 | 无 | **30 事件 × 3 跑，82.2%（78.5–85.9），失败与 STA 58 全公开** |
| 企业/政府可私有化说明 | 无 | 无 | 部分 | **有：docs/enterprise/*、docs/government.md（设计稿，未认证）** |
| 视觉证据 | 强 | 中 | 中 | 需补：HTML 档案 + 录屏（本包 demo-script.md） |

---

## 4. 这些数据如何变成目标（摘要，详见 `README.md` §4）

1. **不要用 MiroFish 的 82k 做目标锚点**——它是形态 A，靠病毒传播，且已经占用「群体智能预测」心智。
2. **用 attackgen 做下限锚点**：TTX 品类第一、有 demo、有买家词，近 30 天 +13 star（约 0.4/d，按同速率 90 天约 +39）。我们 90 天的基准目标 100–200 是它的 **2.5–5 倍**（详见 `launch_kit/README.md` §4），前提是**完成 8 个渠道的首发 + ≥3 个 awesome list 收录 + README 重写**；这部分是执行量，不是许愿。
3. **不确定性向上**：如果 HN Show HN 进 front page 或知乎/微信出现一篇 10 万+ 阅读，单次事件可能带来 150–500 star（形态 A 的短脉冲）；向下：如果只有 README 重写、没有分发，90 天后大概率 10–30 star（形态 D）。
4. **企业/政府线索与 star 不相关**：企业漏斗看的是 5–10 个有效对话、2 份 pilot 提案，不看 star 数。不要在对外文案里把 star 当背书。

---

## 5. 复现本文件的数据

```powershell
# 本仓库
gh api repos/yepinggu66/crisis-rehearsal
gh api repos/yepinggu66/crisis-rehearsal/traffic/views
gh api repos/yepinggu66/crisis-rehearsal/traffic/clones
gh api repos/yepinggu66/crisis-rehearsal/issues
gh api repos/yepinggu66/crisis-rehearsal/releases

# 对照仓库（完整列表见 recon/api-snapshot-2026-10-31.json）
gh api repos/666ghj/MiroFish
gh api repos/camel-ai/oasis
gh api repos/mrwadams/attackgen
gh api repos/google-deepmind/concordia
gh api repos/bagusardin25/TeamDynamics

# 近期 star 速度（WatchEvent 采样）
gh api 'repos/mrwadams/attackgen/events?per_page=100&page=1'

# topic 规模
gh api 'https://api.github.com/search/repositories?q=topic:crisis-simulation&per_page=1'
```

> 数字会变。**每次对外引用前重跑一次**，并在文案中标注「截至 YYYY-MM-DD」。本文件的数字仅在 2026-10-31 快照下成立。
