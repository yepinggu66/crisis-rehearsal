# Government and public-sector edition

> **设计稿 / 无政府采购案例 / 未列入任何采购目录 / 未通过任何测评。**
> This is a design document. There is **no government procurement case, no pilot with a
> government body, no framework agreement, and no security assessment**. Nothing here should be
> read as evidence of government adoption. Section 8 lists what is deliberately not supported.
>
> 本文件是**设计稿**：无政府采购案例、未列入任何采购目录、未通过等保测评或任何政府安全测评、
> 未取得涉密资质。任何「已服务某政府部门」的说法都不成立。

## 1. 中文摘要（给内部汇报用）

危机预演是一个**离线可跑的危机桌面推演工具**：把一起真实的公开危机倒回到爆发前 72 小时，
只给模拟引擎当时公开可得的信息，让 7–12 个虚拟角色（媒体、投资者、监管、竞争对手等）演化两轮，
生成一份 8000 字左右的预演报告，再用固定评分规则与真实结局对照。公开回测是 30 起中国企业的
公开危机事件 × 3 次重复，Top-3 风险命中率为 **82.2%**（事件均值分级分，95% 置信区间
78.5–85.9）——这是「方向性证据」，**不是预测**，也不是任何准确率承诺；稳定性指标 STA 58
低于自设及格线 60，且只有 17% 的事件三次运行得到完全相同的分数，我们照实公布。

对政务场景的价值是：在政策发布、公共安全事件、食品安全事件、涉企舆情、应急会商之前，
把「第一 72 小时会怎么走、我们该在第几小时说什么、谁拍板」在会议室里先演一遍；产出是一份
自包含 HTML 预演档案（可直接进会商材料）和一份决策日志。

它**不是**舆情监测系统（不接实时数据），**不能**替代应急指挥系统与法定程序，**未**做等保测评，
**不支持**涉密环境。政府侧落地前，应先完成分级分类、网络与数据合规评估。

## 2. Scenarios that fit (and ones that do not)

| Scenario | What a rehearsal produces | Fit |
|---|---|---|
| Policy rollout (education, pricing, subsidies) | Pre-announcement reaction paths, likely misreadings, Q&A branches, first-48h communication choices | ✅ |
| Public-safety incident (assault, accident, disaster) | Escalation to national opinion, local-government response sequence, spokesperson timing | ✅ (with a local, non-classified pack) |
| Food-safety / product-safety enforcement | Regulator–media–consumer paths, correction-vs-silence branches | ✅ |
| Enterprise-related opinion (营商环境) | Whether a local enforcement action becomes a national story; third-party and investor reaction | ✅ |
| Emergency-command tabletop | A structured T-72h pack and a facilitated decision exercise | ✅ as a **tabletop aid**, not a command system |
| NIMBY / land / environmental projects | Stakeholder escalation, local vs. national media paths | ✅ |
| Classified incident response | — | ❌ **Not supported.** No classified-network qualification, no assessment; do not deploy |
| Real-time monitoring / early warning from live feeds | — | ❌ Not a monitoring system; no ingestion pipeline |

## 3. Classification and isolation (分级分类)

| Data class | Recommended deployment | Network | What to check |
|---|---|---|---|
| **公开 (public)** | Evidence workstation on any laptop; public corpus only | offline | None beyond normal endpoint hygiene |
| **内部 (internal)** | Private cloud / intranet single machine; packs about internal plans | no egress; local model or approved endpoint | Internal data-handling rules |
| **敏感（非涉密）** | Air-gapped workstation/server; local model only | physically isolated | Classification review, media-transfer rules, deletion record |
| **涉密 (classified)** | **Do not deploy.** | — | Requires 涉密信息系统集成资质、涉密测评、专用产品; this project has none |

Rule of thumb: if the scenario content could not be pasted into an internal email, it does not
go into a scenario pack on a machine with any egress. The tool has no field-level encryption of
its own; storage protection is the deployment's job.

## 4. Deployment in a government environment (today)

What actually works today, no roadmap:

- **x86_64 Linux (or Windows) + Python ≥ 3.9**, offline install, standard library only for the
  evidence workstation (`crh verify/stats/report/demo/pack/site`).
- **Single machine or a small intranet VM**, file-based outputs, no database, no inbound
  service, no telemetry.
- **Local model gateway** (Ollama/vLLM) for a full rehearsal without egress. The published grid
  used `deepseek-chat`; local-model quality on the grid is **not benchmarked** — treat local
  results as your own baseline, not as a reproduction of 82.2%.
- **Air-gap install** via offline wheels and media transfer: see
  [`deployment.md` §4](deployment.md#4-shape-c--air-gapped-installation).

What does **not** exist today: a 政务云 marketplace image, a 等保测评 report, a 国密-enabled
build, a 信创-certified package, or an integration adapter for command systems.

## 5. 信创 adaptation — status: roadmap, unverified

| Layer | Target | Status | Honest note |
|---|---|---|---|
| OS | 麒麟 / 统信 UOS | **未验证** | Pure-Python + stdlib CLI is likely portable, but we have not run it on these systems. Do not assume; test in your environment |
| CPU | 鲲鹏 / 飞腾 / 海光 / 龙芯 | **未验证** | Same; no performance data. Local-model inference on these platforms is a separate engineering task |
| Database | 达梦 / 人大金仓 | **不需要** for the CLI | The tool is file-based; a database only matters if you integrate with your own systems |
| 中间件 / 浏览器 | 国产浏览器、WPS | **未验证** | Dossiers are static, self-contained HTML; verify rendering and printing in your standard desktop image |
| 国密 | SM2 / SM3 / SM4 | **roadmap** | Today: SHA-256 for evidence integrity, TLS from your ingress. 国密改造 is not implemented |
| 信创整体认证 | 任何目录/认证 | **无** | No product certification, no catalogue entry, no compatibility certificate |

If a tender requires 信创/国密 certificates, this product does not meet that gate today. We
would rather say that than have a bid fail on verification.

## 6. Integration with existing systems

| Target system | What can be exchanged | How | Status |
|---|---|---|---|
| 舆情监测系统 | Exported event rows / T-72h material → scenario pack | Manual export (CSV/JSON) → `crh pack init` / edit → `crh pack validate` | 部分: file-based, no connector |
| 应急指挥系统 | Dossier (HTML) + decision log | Export the self-contained HTML; attach to the command file; print to PDF | 部分: no live API |
| 值班 / 会商流程 | Tabletop agenda, decision log, readout | Facilitated workshop; templates in the procurement pack | 部分 |
| OA / 公文系统 | Readout memo | Copy into your document workflow; the dossier prints cleanly | 未覆盖 |
| 政务云 / 大数据平台 | — | Not integrated; no agent, no connector, no data pipeline | 未覆盖 |

Design principle: **file-based by default.** A government network should not need to open a port
or trust a vendor service for a rehearsal to work. That is a security feature; it is also why
there is no "platform integration" to sell in v0.3.

## 7. Pilot process (建议, 2–4 weeks)

1. **Select a past public event** with a known outcome (e.g. a food-safety or public-safety
   event already in the public record). No classified material; no live incident.
2. **Classification and clean-room review**: internal owner + legal/compliance confirm the pack
   uses only pre-T0 public information and contains no sensitive material.
3. **Install offline** on a non-classified intranet machine; run `crh verify/stats/demo` and
   record the output (`docs/enterprise/procurement.md` §2).
4. **Run 3–5 times, read the consensus**; note the within-run disagreement instead of hiding it.
5. **Hold a 会商/tabletop**: 90–120 minutes, decision log with owners and deadlines; produce a
   readout memo that stays within "rehearsal, not forecast".
6. **Decide**: integrate into the annual exercise calendar, extend to another scenario, or stop.
   There is no obligation and no procurement commitment implied by a pilot.

Success criteria should be agreed in advance. Good ones are concrete: "the Top-3 includes one
risk the response team had not written down", "the decision log changes one action and names an
owner", "the readout survives legal review without overclaiming".

## 8. What is explicitly not supported

- **Classified networks** — no 涉密资质, no 涉密测评, no classified product certification.
- **等保 compliance as a product claim** — see [`enterprise/compliance.md`](enterprise/compliance.md):
  mapping only, no assessment.
- **Government procurement catalogue / framework** — not listed, no framework agreement.
- **Real-time monitoring or alerting** — no feed ingestion, no connectors.
- **Command-system integration** — no API, no protocol adapter.
- **信创 / 国密 certification** — roadmap, unverified.
- **Named government references** — none exist; we do not invent them.

## 9. Risks a government buyer should weigh

| Risk | Why it matters | Mitigation |
|---|---|---|
| Over-reading the 82.2% | It is an event-mean graded backtest on 30 Chinese corporate events, not a prediction of your incident | Read the limitations and `data/failures.md`; use it as a rehearsal, not an oracle |
| Model endpoint | A cloud API is an egress path; a local model keeps content in-perimeter but is unbenchmarked | Local model for sensitive content; record the choice |
| Classification mistakes | The operator decides what goes into a pack; the tool cannot classify for you | Written classification review before authoring |
| Stability | Only 17% of events reproduce identically across three runs | Run 3–5 times; read the consensus; document disagreements |
| Vendor maturity | Single-maintainer open-source project | Open code, reproducible evidence, no lock-in; treat support expectations accordingly |
| 信创/国密 requirements | May be mandatory in a tender | Not met today; do not bid on the assumption that it will be |

## 10. Contact

Open an issue on GitHub or email **yepinggu@outlook.com**. For government conversations we will
start by telling you what the tool cannot do (this page), then run the offline reproduction on
your own machine. If a procurement requires certificates we do not have, the honest answer is
no — and we will say so in writing.
