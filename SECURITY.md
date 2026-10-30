# Security policy

## Supported versions

| Version | Status |
|---|---|
| `0.3.x` | Supported — security fixes and documentation corrections |
| `< 0.3` | Not supported (v0.1/v0.2 were research snapshots; the evidence pack is unchanged, the code is superseded) |

This is a small open-source project, not a vendor with a 24×7 security team. The timelines below
are best-effort targets, not a contractual SLA (an SLA can be agreed separately — see
[`docs/enterprise/procurement.md`](docs/enterprise/procurement.md) §4).

## Reporting a vulnerability

**Do not open a public issue for a suspected vulnerability.**

- Email **yepinggu@outlook.com** with the subject line `[SECURITY] crisis-rehearsal`.
- If the repository has GitHub private vulnerability reporting enabled, you may use
  *Security → Report a vulnerability* instead; both reach the maintainer.
- We have no published PGP key. If you require encrypted email, say so in a first message and
  we will arrange a channel before you send details.

Please include:

1. affected version (`crh --version`) and platform;
2. a minimal reproduction — command, file contents or pack, and the observed result;
3. the impact you believe it has, and any suggested fix;
4. whether you want public credit.

## What happens next (best effort)

| Step | Target |
|---|---|
| Acknowledge receipt | 3 business days |
| Initial assessment and severity | 10 business days |
| Fix or documented mitigation for critical/high issues | 90 days |
| Public advisory / release note | after a fix is available, coordinated with the reporter |

We will tell you if we cannot meet a target. We do not run a bug bounty.

## Disclosure policy

Coordinated disclosure: we ask for up to 90 days before public detail, and we will credit you
in the release note unless you prefer to stay anonymous. If a fix is not coming, we will say so
and publish the limitation rather than silently closing the report.

## Scope

**In scope** for this repository:

- `crisis_rehearsal/` CLI and its command handling (path traversal in `--out`/`--repo`/`--event`
  handling, unsafe file writes, exit-code bypass);
- `crh verify` evidence verification (making an edited evidence file pass, or a valid pack fail);
- `crh pack validate` (accepting a malicious/invalid pack, or code execution through pack
  content);
- generated HTML dossiers (script injection from event/pack text; external resource loading that
  breaks the "self-contained, no-network" guarantee);
- the v0.1/v0.2 pipeline scripts and patches in this repository (credential leakage, unsafe
  file handling);
- dependency/supply-chain issues in what this repository ships.

**Out of scope** (report to the right owner):

- vulnerabilities in upstream **MiroFish** or **OASIS** — report upstream, then tell us so we can
  pin or patch;
- vulnerabilities in a model provider, cloud platform, OS, or the customer's deployment (TLS,
  SSO, container runtime);
- the quality, bias or stability of simulation output — that is a methodology limitation,
  documented in `README.md` and `data/failures.md`, not a vulnerability;
- the fact that the project has no certification or security assessment — that is disclosed in
  `docs/enterprise/compliance.md`;
- social engineering, physical access, or a compromised operator workstation.

## Safe harbour

We will not pursue legal action for good-faith security research that: stays within the scope
above, avoids privacy violations and data destruction, does not degrade service for others, and
gives us reasonable time to fix before public disclosure. When in doubt, email first.

## Security documentation

- [`docs/enterprise/security.md`](docs/enterprise/security.md) — threat model (STRIDE), data
  flow, default no-egress, credential handling, audit/RBAC design, retention; explicitly a
  design description, **not an assessment**.
- [`docs/enterprise/compliance.md`](docs/enterprise/compliance.md) — requirement mapping and
  gaps; no certification.
- [`docs/deployment.md`](docs/deployment.md) §8 — go-live hardening checklist.
