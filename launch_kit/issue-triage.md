# Issue 运营与分诊（issue-triage）

> 数据截至 2026-10-31 01:51（API）：**3 个 open issue，全部由 owner 自己创建，0 条评论，无 label、无 milestone。**
> 对访客的信号：仓库「有人在写 roadmap，但没人维护」。v0.3.0 发布前必须把这一步补上，否则流量来了也接不住。

---

## 1. 现状与总体动作

| # | 标题 | 状态 | 性质 | 建议 label | 建议 milestone | 保留？ |
|---|---|---|---|---|---|---|
| #1 | Methodology: re-run the agent-interview step (v0.1 reports logged 0/19 interviews) | open | 方法论债务 | `methodology`, `needs-research` | v0.3.1（根因） | ✅ 保留 |
| #2 | Roadmap: human-calibrate the judge | open | 方法论债务 / 可信度 | `methodology`, `trust` | v0.4.0 | ✅ 保留 |
| #3 | good first issue: add one non-Chinese-market event with a sourced T-72h seed | open | 可贡献入口 | `good first issue`, `data`, `help wanted` | v0.4.0 | ✅ 保留 |

**发布前必做（30 分钟）：**
1. 建 label（见 §3），给三个 issue 打上。
2. 建 2 个 milestone：`v0.3.1`（bugfix）、`v0.4.0`（methodology）。
3. 在每个 issue 下补一条**状态评论**（模板见 §2），说明「现在做到哪、下一步、欢迎怎么帮」。
4. 把 #3 做成「第一个外部贡献入口」：在 PR 模板与 README（W2 负责）里链过去；Discussions 置顶帖也链。
5. 发布后 48 小时内回所有新 issue（见 §4 SLA）。

> 不要为了「看起来活跃」而关闭 roadmap issue。#2/#3 是长期路线图，关闭会损失「可贡献」的信号。

---

## 2. 三个已有 issue 的处理建议 + 状态评论草稿

### #1 agent-interview 0/19

**分析：** 这是最严重的**方法论问题**，因为它影响「82.2% 到底在测什么」的表述：如果 Top-3 排序只来自知识图谱结构，那它更像「结构化推理」而不是「agent 群体对话」。README 已诚实披露，但 issue 没有结论。
**处理：** 保留，标 `methodology` + `needs-research`，milestone `v0.3.1`。
**建议动作：**
1. 先在 v0.3.1 里做**根因排查**（不改数字、不改 data）：检查 interview API 是否被禁用、interview prompt 是否格式错误、OASIS 版本是否变更、`meta.json` 是否记录 interview 数。
2. 拿到根因后再决定是否重跑 ≥3 个事件；重跑属于 v0.4.0。
3. 无论结论如何，更新 `docs/methodology.md`（W2 负责，Lead 协调）——**不能只改 README 措辞而不留证据**。

**状态评论草稿（英文，可直接发）：**

```markdown
Status update (maintainer): keeping this open as a methodology debt for v0.3.1.

Scope for v0.3.1 — root cause only, no re-run:
- [ ] check whether the interview step is disabled or misconfigured (OASIS version, interview prompt, API flag)
- [ ] record the interview count in the run's `meta.json`
- [ ] document findings in `docs/methodology.md` — whichever way it goes

If the root cause is found, the actual re-run (≥3 v0.2 events) moves to v0.4.0, because it changes report content and needs the full repeat/scoring protocol.

Why it matters: the Top-3 ordering is a claim about risk *ordering*. If it comes only from graph structure, the method is closer to structured inference than to agent dialogue, and the wording in the README should change accordingly. Until then, the current README limitation stands as written.
```

---

### #2 human-calibrate the judge

**分析：** 所有下游数字（82.2%、CI、STA）都继承 judge 偏差；没有人工校准，就不能说 judge 是宽松还是严格。这是**可信度的关键缺口**，但工作量不小（10 条记录 × 2 名独立评分者 + kappa）。
**处理：** 保留，milestone `v0.4.0`，label `methodology` + `trust`。
**建议动作：**
1. 先写清校准协议（谁评、是否盲评、分歧如何裁决），更新 `data/judge_calibration.md`。
2. 找 2 名独立评分者（可以是外部志愿者），发 `good first issue` 变体：`help wanted: human-score 10 judge records`。
3. 输出：人类间 raw agreement + Cohen's kappa、人类 vs LLM 的 agreement；写进 `data/judge_calibration.md`，再改 README 限制段。
**注意：** 不要把「人工校准」写成「已验证准确率」；校准的是 judge 的一致性/偏差，不是预演对未来的准确率。

**状态评论草稿：**

```markdown
Status (maintainer): this is the biggest credibility gap we have, and it stays open for v0.4.0.

Plan:
1. Write the calibration protocol first (blind scoring? two independent scorers? tie-breaking?) into `data/judge_calibration.md`.
2. Recruit 2 independent scorers (external volunteers are welcome — reply here if you want to help).
3. Sample 10 of the 90 records; report (a) raw agreement and Cohen's kappa between humans, (b) agreement between humans and the LLM judge.
4. Update `data/judge_calibration.md` and the README limitation line *only after* the result exists.

This calibrates judge consistency/bias. It does not turn the 82.2% into a validation of the method against the future — that distinction stays in the docs.
```

---

### #3 non-Chinese-market event（good first issue）

**分析：** 这是最好的「外部贡献入口」：范围清晰、验收标准已写、能直接测试泛化性。**它应该是我们主动营销的 issue**——在 Discussions 置顶、在 PR 模板里链、在 HN/知乎帖里提「欢迎带来源的 PR」。
**处理：** 保留，label `good first issue` + `data` + `help wanted`，milestone `v0.4.0`。
**注意数据红线：** `data/**` 是证据文件，**不接受为了修 bug 而改数据**；新增事件必须带来源 URL、T-72h 洁净室检查、并与现有 12 列格式一致。外来 PR 如果改了现有数据行 → 直接要求 rebase 到只新增行。

**状态评论草稿：**

```markdown
Status (maintainer): this is the intended first external contribution. Scope is intentionally small.

Checklist before you open a PR:
- [ ] one row in `data/events.csv` (same 12 columns), with live source URLs for trigger, outcome and penalty
- [ ] one seed in `data/seeds/` with only information public in the 72h before T0 (no post-T0 outcomes, no `待核` placeholders, no `可预测性` label)
- [ ] one pipeline run + judge score appended in the same format as the existing grid
- [ ] a manual post-T0 audit note in the PR description

If the event turns out to be unpredictable, submit it anyway — negative samples are part of the corpus. If you are unsure about a source, open a draft PR and ask; do not guess.

I can help with the run/scoring part if you provide the seed and sources.
```

---

## 3. Label 体系（发布前建好）

| Label | 颜色 | 用途 |
|---|---|---|
| `bug` | `#d73a4a` | 可复现的功能错误 |
| `data-integrity` | `#b60205` | 证据包 sha256 不符、数据被改动（最高优先级） |
| `needs-repro` | `#fbca04` | 缺环境/命令/输出，等待补充 |
| `docs` | `#0075ca` | 文档/链接/示例错误 |
| `enhancement` | `#a2eeef` | 新功能/场景包需求 |
| `methodology` | `#5319e7` | 统计/评分/实验设计问题 |
| `trust` | `#6f42c1` | judge 校准、合规表述、限制披露 |
| `good first issue` | `#7057ff` | 给外部贡献者的入口 |
| `help wanted` | `#008672` | 明确欢迎 PR |
| `government-pilot` | `#0e8a16` | 政府/央企/企业 pilot 询问（转私信） |
| `question` | `#d876e3` | 使用问题 → 优先引导到 Discussions |
| `wontfix` | `#ffffff` | 明确不做（附理由） |
| `duplicate` | `#cfd3d7` | 重复 |
| `security` | `#ee0701` | **不要用在公开 issue 上**；见 §5 安全流程 |

**Milestones：** `v0.3.1`（bugfix，2026-12）、`v0.4.0`（methodology，2027-Q1，无日期承诺）。

---

## 4. 首个外部 issue 的响应模板（重要）

### 4.1 通用 SLA（单人维护，按 best effort 写清楚，不承诺）

| 类型 | 首次响应 | 处理目标 |
|---|---|---|
| `data-integrity` / 安全 | **24 小时内** | 立即确认 + 复现 |
| `bug` | 48 小时内 | 7 天内给结论（修/延/不修） |
| `government-pilot` | 48 小时内 | 转邮件/会议（不在公开 issue 收集机构信息） |
| `enhancement` | 7 天内 | 进 milestone 或说明不排期 |
| `question` | 3 天内 | 引导 Discussions |

### 4.2 首次外部 bug issue（英文模板）

```markdown
Thanks for the report — this is the first external issue on the repo, so I want to get it right.

To reproduce, I need four things:
1. `crh --version` output
2. OS + Python version (`python -V`)
3. the exact command and the full output (copy text, not a screenshot)
4. `crh verify` result — if it reports a mismatch, stop here and tell me; we treat evidence-pack changes as data-integrity issues first

Once I can reproduce, I'll label it and either fix it or tell you plainly that it's out of scope for v0.3.x. I won't give a date I can't keep.

If this involves a security vulnerability, please do not continue here — close this and follow `SECURITY.md` instead.
```

**中文版（发给中文用户时用）：**

```text
谢谢你第一个来提 issue。为了复现，麻烦补四样东西：
1. `crh --version` 的输出
2. 操作系统 + Python 版本（`python -V`）
3. 完整命令和完整输出（文字，不要截图）
4. `crh verify` 的结果——如果出现校验不匹配，请先停在这里告诉我，我们会按 data-integrity 优先处理

能复现后我会打 label，然后要么修，要么明确告诉你 v0.3.x 不修。我不会给做不到的日期承诺。

如果涉及安全漏洞，请不要继续在这里公开——按仓库 `SECURITY.md` 的流程处理。
```

### 4.3 数据完整性问题（最高优先级）

**判断：** `crh verify` 报 FAILED / 用户发现 `data/repeat_v02/` 数字与 README 不一致 / PR 改动了 `data/**` 的既有行。
**动作：**
1. 立刻 label `data-integrity`，回复要求提供 `crh verify` 全文与 `sha256sum` 结果（Windows：`Get-FileHash`）。
2. **不要**在本地「顺手修一下数据」；先确认是代码 bug 还是数据被改。
3. 如果是数据被改：找到改动来源（commit / PR），回滚，保留证据；公开说明。
4. 如果是代码 bug：修代码，不改数据；补一个断言测试（stats 必须与 `data/repeat_v02` 一致）。
5. 处理完在 issue 里写清根因与受影响范围，并更新 `CHANGELOG`（Lead 负责）。

**回复模板：**

```markdown
Treating this as `data-integrity` (highest priority). Please paste:
- full `crh verify` output
- sha256 of the file(s) you changed or suspect: `sha256sum <file>` (Windows: `Get-FileHash <file>`)
- `git log --oneline -5` and `git status`

We will not edit the evidence pack to make a test pass. If the manifest and the data disagree, we find out which one is wrong, then fix the code or revert the data — and say which in this thread.
```

### 4.4 政府 / 企业 pilot 询问（`government_pilot.yml` 模板进来的）

```text
Thanks for reaching out. I've moved this to email (yepinggu@outlook.com) because a public issue is the wrong place for organization details.

Short version of what a pilot is, so you can decide if it's worth a call:
- 2 weeks, offline, on public historical events only — no internal data required
- deliverables: 3 T-72h packs, 3 self-contained HTML rehearsal dossiers, one 2-hour review session, one capability/gap memo
- we are not certified, we have no government/client references, and the compliance docs are requirement mappings with gaps

I'll reply to your email within 2 business days with a one-page proposal. If you'd rather not continue, tell me and I'll close this issue.
```

### 4.5 安全漏洞：**不要**在 issue 回答

回复一句并关闭/锁定：

```text
This looks like a security issue, so I'm closing this thread. Please report it privately following `SECURITY.md` (GitHub private vulnerability reporting / email). I'll acknowledge there and coordinate a fix and disclosure timeline.
```

同时：开启 GitHub Security Advisory（如果尚未开启），按 `SECURITY.md` 的时限处理；修好后在 Release notes 里致谢（经报告者同意）。

---

## 5. 关闭模板（避免「无声关闭」）

- **修好：** `Fixed in <commit/PR>. Thanks — added/updated <test/doc>.` + 链到 commit。
- **不修（wontfix）：** `Not planning to do this because <具体原因：超出范围/与 AGPL 商业边界冲突/无法验证>。If your use case is different, tell me and I'll reopen.`
- **无法复现：** `Closing for now because I couldn't reproduce with the info provided. If it happens again, reopen with <crh --version + full output>.`
- **重复：** `Duplicate of #<n>. Keeping the discussion there.`
- **超出范围（变成 pilot）：** `Moving this to email as a commercial/pilot conversation; issue closed to keep the tracker for reproducible bugs.`

**原则：** 每个关闭都留一句原因 + 一个可行动的下一步；不删评论、不锁帖（除非安全/骚扰）。

---

## 6. 发布后前 30 天的 issue 运营节奏

| 时间 | 动作 |
|---|---|
| 每天 1 次（15 分钟） | 看新 issue/PR；按 §4 SLA 回；把纯使用问题转 Discussions |
| 每周五 | 更新 Project 看板状态；把未决 issue 归到 milestone 或 `wontfix` |
| 每两周 | 写一条 Discussions「This week in Crisis Rehearsal」（修了什么、拒了什么）——增长素材 |
| 每月 | 复盘：外部 issue 数、平均首响、data-integrity 次数；写进 `recon/measurements.md` |

**不要做：** 为了显得活跃而批量关闭旧 issue；在 issue 里承诺日期；让公开 issue 承载客户/政府机构信息；用 bot 自动回复（个人项目用模板手写反而更可信）。
