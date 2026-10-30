# Compliance mapping and gaps

> **本文是「要求映射 + 差距清单」，不是测评报告、不是法律意见。**
> This document maps the product to requirement families. It is **not** an assessment report,
> **not** a legal opinion, and **not** evidence of compliance. Crisis Rehearsal v0.3.0 has
> **no certification** (ISO 27001, SOC 2 or otherwise), **no 等保测评报告**, and **no
> government security assessment**. Any claim to the contrary is wrong.

## 1. How to read this document

- **Scope of the mapping:** the open-source CLI, evidence pack, generated dossiers and the
  reference deployment in [`deployment.md`](../deployment.md). Upstream MiroFish/OASIS and the
  customer's cloud/OS/network are outside the product's boundary.
- **Shared responsibility:** most control families are only satisfiable by the customer's
  environment (physical security, network segmentation, staff screening, change management,
  incident response). The product contributes specific technical controls; it cannot make a
  system "pass" anything on its own.
- **Status legend:**

| Status | Meaning |
|---|---|
| **支持 (supported)** | A shipped capability that a customer can demonstrate today (code, document, or generated artefact) |
| **部分 (partial)** | Design exists or the capability depends on deployment choices; not tested by us in the customer's environment |
| **未覆盖 (not covered)** | Not addressed by the product; customer or upstream responsibility |
| **roadmap** | Planned; not in v0.3.0 |

A mapping row is a conversation starter for your assessor, not a control attestation.

## 2. 等保 2.0 三级 (GB/T 22239-2019) — requirement-domain mapping

等保 is a system-level assessment (定级、备案、建设整改、等级测评、监督检查). A software
component cannot be "等保三级 certified"; the operating system, network, physical environment,
management processes and the测评 agency's report carry the bulk of it. What this product can do
is reduce the number of gaps a 三级 system has to close.

| 等保 2.0 domain | What a 三级 system typically needs | Product contribution | Status | Gap / customer responsibility |
|---|---|---|---|---|
| **安全物理环境** | Data-centre physical controls, equipment protection | Air-gap/on-prem deployment possible; no cloud-only dependency | 未覆盖 | Entirely the customer's facility |
| **安全通信网络** | Network segmentation, communication integrity/confidentiality | Offline workstation; private deployment with no egress; TLS at ingress (deployment doc) | 部分 | Network architecture, TLS, segmentation are deployment responsibilities |
| **安全区域边界** | Border protection, access control, intrusion prevention, malicious-code prevention | Default-deny egress reference design; single egress to model gateway | 部分 | Firewall/IPS/anti-malware are customer controls |
| **安全计算环境** — 身份鉴别 | Unique identity, complexity, re-authentication | No built-in identity; SSO/OIDC at ingress | 部分 | Customer IAM; built-in RBAC is roadmap |
| **安全计算环境** — 访问控制 | Least privilege, separation of duties | Filesystem-level separation per engagement; role design in `security.md` §7 | 部分 | OS ACLs / IAM; product RBAC roadmap |
| **安全计算环境** — 安全审计 | Audit records protected, retained ≥6 months, reviewed | CLI does not implement an audit log; container stdout can be shipped to SIEM; evidence hashes are not an operator audit trail | 未覆盖 (roadmap) | SIEM/log retention is customer-side; product audit log is roadmap |
| **安全计算环境** — 数据完整性 | Integrity of important data | `data/evidence.sha256` + `crh verify`; dossier evidence hashes; git history | 支持 (for the evidence pack) | Integrity of *customer* data stores is deployment responsibility |
| **安全计算环境** — 数据保密性/备份恢复 | Encryption, backups | No storage layer of its own; backup/restore procedure documented (`deployment.md` §7) | 部分 | Disk/volume encryption, backup infrastructure, restore testing |
| **安全管理中心** | Central monitoring, audit, management | No central management plane in v0.3 | 未覆盖 | Customer SOC/SIEM |
| **安全管理制度** | Security policy, personnel, development/ops processes | Open development, issue tracker, SECURITY.md, CONTRIBUTING.md; no internal ISMS | 未覆盖 | Customer's ISMS; we do not have a certified ISMS |
| **安全管理机构 / 人员** | Roles, screening, training | Single-maintainer project, no org-level structure | 未覆盖 | Customer organisation |
| **安全建设管理 / 运维管理** | Secure SDLC, change, configuration, incident management | Git history, pinned upstream commit, CI tests, release notes; no formal change board | 部分 | Customer's change/incident processes |

**Honest conclusion for a 三级 project:** treat the product as a **component** whose
deployment can be designed to fit a 三级 system. It provides offline operation, hash-verified
evidence and no default egress; it does **not** provide identity, audit logging, central
management, or a测评 report. Budget for those separately.

## 3. 数据安全法 (DSL)

| Requirement area | What it asks | Product contribution | Status |
|---|---|---|---|
| 数据分类分级 | Classify data and apply graded protection | Scenario-pack `meta.classification` field; guidance to classify packs before rehearsal | 部分 |
| 重要数据目录 / 风险评估 | Identify important data; periodic risk assessment | Not a data-inventory tool; no automatic classification | 未覆盖 |
| 数据出境 | Assessments/contracts for cross-border transfer | Nothing leaves the network by default; a cloud LLM API is an explicit egress path | 支持 (default) / 部分 (cloud config) |
| 处理活动记录 | Records of processing activities | Dossier evidence hashes + file timestamps; no product-level processing register | 部分 |
| 风险监测与事件报告 | Detect and report data-security incidents | No monitoring; incident reporting is the operator's duty | 未覆盖 |
| 委托处理 / DPA | Contractual controls with processors | DPA talking points in `procurement.md`; no standard DPA template published | 部分 |

## 4. 个人信息保护法 (PIPL)

The public corpus references **individuals named in public reporting** (executives, public
figures) and public events. It contains no private personal data, no contact details, no
customer data. Processing such publicly disclosed information within the scope of public
reporting/analysis is the project's basis; if you process it for another purpose, your own
legal analysis is required.

| Requirement area | Product contribution | Status |
|---|---|---|
| 处理公开个人信息的合理范围 | Corpus limited to public figures in public reporting; documented in `data/README.md` | 部分 |
| 最小必要 / 目的限定 | Event fields are purpose-bound (event, trigger, outcome, penalty, sources) | 部分 |
| 告知同意 / 个人权利 | Not handled by the product; a removal request for a named individual in the corpus goes to the maintainers (issue/email) and is reviewed | 部分 |
| 委托处理协议 | DPA points for customer deployments in `procurement.md` §7 | 部分 |
| 跨境提供 | Cloud API deployments may transfer prompt content; use a local model or a compliant transfer mechanism | 部分 |
| 个人信息保护影响评估 (PIPIA) | No template provided | 未覆盖 (roadmap) |

Guidance: if your scenario pack contains personal data, **you are the controller**. Minimise,
pseudonymise, define retention, and do not send it to a cloud model unless that transfer is
covered by your own assessment.

## 5. GDPR (for EU-facing deployments)

| GDPR area | Product contribution | Status |
|---|---|---|
| Art. 5 principles (lawfulness, minimisation, storage limitation) | Corpus is public-reporting material; customer packs responsibility of the controller | 部分 |
| Art. 6 lawful basis | Not determined by the product | 未覆盖 (controller's duty) |
| Art. 28 processor obligations | DPA points; no sub-processor list published because cloud-model choice is the customer's | 部分 |
| Art. 30 records of processing | No built-in register | 未覆盖 |
| Art. 32 security of processing | Offline/no-egress default; hash-verified evidence; deployment hardening guide | 部分 |
| Art. 35 DPIA | Not provided | 未覆盖 (roadmap) |
| Art. 33/34 breach notification | No monitoring; processor would notify the customer per contract | 部分 |
| Art. 44–49 international transfers | Cloud API may transfer data outside the EEA; local model avoids it; SCCs are the customer's responsibility | 部分 |
| Art. 15–22 data-subject rights | Removal path for named individuals in the corpus; customer packs are the customer's data | 部分 |

## 6. ISO/IEC 27001:2022 — Annex A themes

No ISMS, no Statement of Applicability, no certification, no surveillance audit. This table
says which themes the product's controls touch, not that the product "implements 27001".

| Annex A theme | Product contribution | Status |
|---|---|---|
| A.5 Organizational controls | Open governance docs, SECURITY.md, issue process; no policy set for customers | 部分 (docs) / 未覆盖 (certification) |
| A.6 People controls | Code of conduct, contribution rules; no employment screening (no employer role for contributors) | 部分 |
| A.7 Physical controls | None (no facility); air-gap deployment possible | 未覆盖 — customer |
| A.8 Technological controls | Hash-verified evidence, offline default, pinned dependencies, CI tests, deployment guide | 部分; audit logging, identity, vulnerability scanning are roadmap/customer-side |

## 7. SOC 2 (Trust Services Criteria)

No SOC 2 report, no audit, no readiness assessment. Security / Availability /
Confidentiality / Processing Integrity / Privacy are **not attested**. The only thing a buyer
can verify today is the evidence chain: `crh verify`, `crh stats`, the open code, and this gap
list. If a procurement process requires a SOC 2 report, this product does not meet that gate
today — and saying so is cheaper for everyone than a workaround.

## 8. Cross-cutting gaps

| Gap | Why it matters | Mitigation today | Roadmap |
|---|---|---|---|
| No built-in identity/RBAC | Shared deployments cannot prove least privilege | SSO at ingress + OS ACLs | Enterprise RBAC |
| No tamper-evident audit log | Regulated audits need who-did-what | stdout → SIEM; evidence hashes for *what* | Hash-chained audit log |
| No 国密 (SM2/SM3/SM4) support | 国内测评/行业要求 often expect SM algorithms | SHA-256 manifests, TLS via deployment | 国密 adaptation (with 信创 work) |
| No data-classification automation | Customers must classify packs manually | `meta.classification` field + guidance | Classification lint in `crh pack validate` |
| No PIPIA/DPIA template | Controllers must do it themselves | Guidance notes in this file | Template |
| No standard DPA/sub-processor list | Procurement needs paper | Talking points in `procurement.md` | Contract templates |
| No incident-response runbook for the product | Required by most frameworks | SECURITY.md disclosure path | IR runbook |
| No vulnerability scanning / SBOM published | Supply-chain due diligence | stdlib-only runtime; pinned upstream | SBOM + dependency scanning in CI |

## 9. How to answer a procurement questionnaire without lying

**Do**

- Quote this document and the status legend; attach it as-is.
- Distinguish **product contribution** from **customer responsibility** in every row.
- Offer a verifiable POC: `crh verify`, `crh stats`, offline demo, your own scenario pack.
- State the unassessed status plainly and name what it would take to assess.

**Don't**

- Don't sign "complies with ISO 27001 / SOC 2 / 等保三级". It does not.
- Don't claim "designed to be 等保三级 compliant" as if a design equals a测评.
- Don't promise certification dates in a bid. Roadmap is roadmap.
- Don't present the 82.2% backtest as an accuracy audit of your deployment.

**Copy-pasteable statement (English):**

> Crisis Rehearsal v0.3.0 is an open-source software component. It has not undergone an ISO/IEC
> 27001 certification, SOC 2 examination, 等保测评 or any third-party security assessment. The
> vendor provides a documented requirement mapping with explicit gaps. Deployment-level
> controls (identity, audit logging, network segmentation, physical security, incident
> response) remain the customer's responsibility.

**声明（中文，可直接引用）：**

> 危机预演 v0.3.0 是开源软件组件，未通过 ISO/IEC 27001 认证、SOC 2 审计、等保测评或任何第三方
> 安全评估。供应方提供要求映射与明确差距清单；身份、审计、网络分区、物理安全与应急响应等
> 部署级控制由使用方负责。

## 10. Contact

Compliance questions and correction requests: open an issue or email
**yepinggu@outlook.com**. If you believe a statement in this repository overclaims, report it —
we would rather publish a correction than defend a false sentence.

## Related documents

- [Security design notes](security.md) — the technical controls referenced in this mapping.
- [Procurement answer pack](procurement.md) — the questionnaire-facing companion to this file.
- [Deployment guide](../deployment.md) — what the deployment actually installs.
- [Government edition](../government.md) — classification and 信创 caveats.
- [ROADMAP](../../ROADMAP.md) — which gaps are scheduled and which are not promised.
