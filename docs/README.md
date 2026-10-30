# Documentation index

Four ways in, depending on who you are. Every document here is written to be read **before**
the sales conversation, not after it.

## 30 秒上手 · Start here

| Document | What it answers |
|---|---|
| [README](../README.md) | What it is, why it exists, 30-second quick start, the published numbers, honest limitations |
| [README-ZH](../README-ZH.md) | 中文版主文档（面向中文读者重写，不是逐字翻译） |
| [docs/cli.md](cli.md) | Full `crh` command reference with real output |
| [data/README.md](../data/README.md) | What is in the evidence pack and how to recompute it |
| [data/repeat_v02/README.md](../data/repeat_v02/README.md) | The 90 judge records: schema, hashes, what is *not* shipped |

## 决策者 · For buyers (CRO / CISO / CIO / emergency office)

| Document | What it answers |
|---|---|
| [enterprise/overview.md](enterprise/overview.md) | Who it serves, scenarios, deliverables, open-core boundary, 30/60/90-day pilot |
| [enterprise/security.md](enterprise/security.md) | Trust boundaries, default no-egress, STRIDE table, audit/RBAC design, retention — design notes, not an assessment |
| [enterprise/compliance.md](enterprise/compliance.md) | 等保 2.0 三级 / 数据安全法 / 个保法 / GDPR / ISO 27001 / SOC 2 requirement mapping with gaps; **no certification** |
| [enterprise/procurement.md](enterprise/procurement.md) | Acceptance criteria, SLA template, price-structure example, POC plan, DPA points, 15 procurement FAQs |
| [government.md](government.md) | 政务/公共部门版：分级分类、涉密隔离（不支持）、信创 roadmap、系统对接、试点流程；**设计稿，无案例** |
| [ROADMAP.md](../ROADMAP.md) | What is planned for v0.4 / v1.0, and what is explicitly not promised |

## 技术 · For engineers and architects

| Document | What it answers |
|---|---|
| [architecture.md](architecture.md) | Components, data contracts, deployment topologies, extension points, upstream MiroFish/OASIS relationship |
| [deployment.md](deployment.md) | Offline workstation / private cloud / air-gap, model backends, sizing and cost transparency, operations |
| [cli.md](cli.md) | `crh verify/stats/report/demo/pack/site` reference |
| [ci/github-actions.yml](ci/github-actions.yml) | CI workflow definition, ready to enable (header explains the one-line copy step and why it is not enabled yet) |
| [patches.md](patches.md) | The five patches against pinned upstream commit `7657031`, and how to verify them |
| [methodology.md](methodology.md) | The T-72h clean room, hit definitions (H1/H2/H3), judge protocol, known limitations |
| [reports/1.md](reports/1.md), [reports/28.md](reports/28.md) | Full sample rehearsal reports (events 1 and 28) |
| [data/failures.md](../data/failures.md) | The events we lost, with post-mortems in the judge's words |

## 合规 · 采购 · 方法论

| Document | What it answers |
|---|---|
| [SECURITY.md](../SECURITY.md) | Vulnerability disclosure, supported versions, response targets |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Dev setup, data contribution rules (T-72h clean room, evidence immutable), review checklist |
| [GOVERNANCE.md](../GOVERNANCE.md) | Roles, decision process, release process, how the commercial boundary is kept |
| [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) | Community behaviour expectations and enforcement |
| [CITATION.cff](../CITATION.cff) | How to cite the project in a paper, report or filing |
| [data/judge_calibration.md](../data/judge_calibration.md) | Status of human calibration of the LLM judge: **not yet run** (the template is here) |

## Other assets

- [`docs/assets/architecture.svg`](assets/architecture.svg) — architecture diagram used in `architecture.md`.
- [`docs/assets/report-preview.png`](assets/report-preview.png) — screenshot of a generated rehearsal dossier (the README preview).
- [`docs/assets/cli-demo.txt`](assets/cli-demo.txt) — terminal transcript of `crh demo`.

## A reading warning

If you only read one section of this repository, read the honest limitations in
[README §Honest limitations](../README.md#honest-limitations) and
[`data/failures.md`](../data/failures.md). The headline number is an event-mean graded score on
30 Chinese public events; the stability metric fails our own pass line; the judge is not
human-calibrated. The method is useful **because** those limits are written down.
