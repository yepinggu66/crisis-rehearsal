# LinkedIn 文案（2 版）

> 读者：CRO / 公关与 IR 负责人（版 A）、CISO / CIO / 合规与采购负责人（版 B）。
> 规则要点：不编客户、不写「已认证」、不放价格；hashtag ≤5；链接放正文中后段或首评；配 1 张社交预览图或 3–5 页 carousel。
> 两版间隔 ≥3 天发布，不要同一天发。

---

## 版 A · 面向 CRO / PR / IR / 董事会秘书

**长度：** ~1,900 字符（LinkedIn 上限 3,000）。

```text
The first 24 hours of a crisis get written into public memory. Most companies only buy monitoring — after the fact. The budget that already exists sits on the response side.

We built something for the side before: an open-source crisis rehearsal engine that rewinds a real crisis to 72 hours before it broke and runs a simulation on only the information that was public at that moment.

How it works, briefly:
• 30 publicly documented corporate crises (2018–2026), each with a T-72h information pack — a clean room, no hindsight
• 7–12 persona agents (journalists, retail investors, regulators, short sellers, competitors) react for 2 rounds on a simulated feed
• an ~8k-character rehearsal report is produced
• a fixed LLM judge scores the report's top-3 risks against the recorded real outcome

The result, stated the way we insist on stating it:
• Top-3 risk hit rate 82.2% (95% CI 78.5–85.9; event-mean graded score, n=30 events × 3 repeats)
• Only 5/30 events scored identically across all three runs; within-event SD 0.26/3
• Our internal stability score is 58 — below our own pass line of 60. We publish it as failed.
• The dominant error mode is false escalation: legal/regulatory branches that felt plausible but never happened (documented, with post-mortems)

That last part matters more to a crisis team than the headline. A rehearsal is not a forecast. Its value is the artifact it forces you to produce before the crisis: timeline, stakeholder map, escalation ladder, decision log — and the disagreements it surfaces while they are still cheap.

For the people who will actually evaluate it: the evidence pack is public. Any engineer can verify the numbers offline in under 10 seconds — no API key:

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo

What we don't have: client logos, government references, or certifications. We don't claim any. The engine is AGPL-3.0 and open; we sell rehearsal reports and workshops, not software licenses.

If your team runs board-level crisis exercises once or twice a year, I'd value a 30-minute conversation about what a two-week offline pilot would need to prove. The pilot outline (design, not a claim) is in the repo: docs/enterprise/overview.md.

#RiskManagement #CrisisManagement #CorporateCommunications #OpenSource
```

**发布注意：**
- 配图用仓库社交预览图（1280×640），或把「30 events / 90 runs / 82.2% (78.5–85.9)」做成 1 页图。
- 首条评论补 GitHub 链接，正文里保留一处在文中（LinkedIn 会降权外链，但决策者需要点得到）。
- 不 @ 任何公司/政府账号；不在评论区收集个人信息。

---

## 版 B · 面向 CISO / CIO / 合规与采购

**长度：** ~2,100 字符。

```text
The first question we get from a security or procurement review isn't "how accurate is it?" It's "does any of our data leave the network?"

Fair question. Here's the honest answer for our open-source crisis rehearsal engine, v0.3.0.

What it does: rewinds a public corporate crisis to 72 hours before it broke, runs an LLM swarm simulation on only the information that was public then, and produces a rehearsal dossier. The 30-event backtest is published, including its failures.

Data flow, by default:
• the shipped demo (crh demo) is fully offline: no network calls, no API key, stdlib only; it verifies the evidence pack by sha256 and generates self-contained HTML dossiers
• the simulation step (regenerating runs) is the only part that needs a model endpoint — and that endpoint can be an internal one (Ollama / vLLM / an approved gateway)
• upstream MiroFish depends on Zep Cloud for its knowledge graph; we replaced it with a local JSON graph adapter, so the pipeline runs with zero cloud graph service
• deployment notes cover three shapes: offline evidence workstation, private cloud (docker compose), and air-gapped install — docs/deployment.md

On compliance — read this part carefully:
• docs/enterprise/compliance.md maps requirements to 等保 2.0 三级 (GB/T 22239-2019), 数据安全法, 个人信息保护法, GDPR, ISO/IEC 27001:2022 and SOC 2
• it is a requirement mapping with explicit gaps, NOT a certification. We are not certified or assessed by any of these.
• audit logging, RBAC and multi-tenancy are design notes, not shipped features. docs/enterprise/security.md says which is which.
• there are no government or enterprise production references. docs/government.md is a design document.

Numbers, with error bars (because a procurement team will ask):
Top-3 risk hit rate 82.2% (95% CI 78.5–85.9; event-mean graded score, n=30 events × 3 repeats). Only 5/30 events reproduce exactly across three runs, and the internal stability score is 58 vs. a 60 pass line — we publish that as failed. It is a rehearsal/backtest producing directional evidence, not a forecast.

If you want your own security and compliance reviewers to look at the real thing rather than a deck:

    pipx install git+https://github.com/yepinggu66/crisis-rehearsal
    crh demo --out demo

Then the two documents worth their time are docs/enterprise/security.md (STRIDE threat model, trust boundaries, what we do not claim) and docs/enterprise/compliance.md (the gap list). If the gaps are acceptable, the pilot path is a two-week offline POC, and the procurement answer pack — deliverables, acceptance criteria, DPA points, 15 questions — is in docs/enterprise/procurement.md.

Open core: the engine is AGPL-3.0. We sell rehearsal reports and workshops, not licenses; the commercial boundary is stated in the repo.

#CISO #Compliance #等保 #DataSecurity #OpenSource #AI
```

**发布注意：**
- 等保/GDPR/ISO 的写法必须是「映射 / 未认证」；如果同事想改成「符合等保」，拒绝——`docs/enterprise/compliance.md` §8 已写清怎么在不撒谎的前提下回答采购问卷。
- 不要放「某央企/某银行已采用」类表述；一个都没有。
- 可以在评论区补 `docs/enterprise/procurement.md` 的链接，但正文不要贴价格。

---

## 两版通用注意

| 项 | 做法 |
|---|---|
| 时间 | 周二–周四 08:00–10:00（发布者本地时间），避开周一上午堆积 |
| 形式 | 纯文本 + 1 张图；长文用 carousel（1 页问题 / 2 页方法 / 3 页数字含 CI / 4 页失败 / 5 页 demo 命令） |
| 频率 | 版 A 发布后 3 天发版 B；之后每 2 周一条「数据/复盘」短帖，保持存在感 |
| 互动 | 只回复实质问题；销售话术私信转邮件，不在评论区报价 |
| 诚信 | 不写「industry-leading」「proven」；所有数字带 CI 或样本量 |
