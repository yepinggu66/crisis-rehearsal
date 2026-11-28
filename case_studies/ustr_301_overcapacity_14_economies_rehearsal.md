# Crisis Rehearsal Pro 0.5.0 — Global Trade & Supply-Chain War-Game Dossier
## The Nov 25, 2026 USTR Section 301 "Structural Overcapacity" Ruling (14 Economies, 15%–35% Tariffs): End of "China Plus One," Inflation Shock & 38-Day Corporate Survival Playbook

> **Date**: November 28, 2026  
> **Engine**: `Crisis Rehearsal Pro 0.5.0` (Explicit 8×8×72 Multi-Stakeholder Dynamics + Section 7 Calibration Protocol)  
> **Real-World Anchor**: On **November 25, 2026**, U.S. Trade Representative **Jamieson Greer** issued affirmative Section 301 determinations targeting **structural excess manufacturing capacity** across **14 economies**, proposing broad tiered tariffs of **15%–35%**—with written comments due **January 5, 2027** and public hearings starting **January 25, 2027** (*USTR*, *S&P Global*, *Holland & Knight*, *KPMG*, *Wiley*).

---

## 0. Executive Summary: The Structural Death of "China Plus One"

For six years, multinational boards hedged U.S.–China trade risk by moving assembly lines to **Vietnam, India, Thailand, Malaysia, Indonesia, Cambodia, and Bangladesh**. The November 25, 2026 USTR Section 301 ruling closes that arbitrage in a single stroke:

1. **Statutory Permanence**: Following the Supreme Court's February 2026 limits on emergency tariff powers (*Holland & Knight*), moving broad tariffs onto **Section 301 statutory footing** makes them far harder to overturn via litigation.
2. **Transshipment Sanctuaries Hit Hardest**: **Vietnam** faces the highest proposed headline cap at **up to 35%** (20% with a bilateral deal) and **India** up to **25%** (17% with a deal)—directly penalizing third-country assembly hubs linked to upstream non-market inputs (*S&P Global*, *PwC*).
3. **The 38-Day Boardroom Window (Nov 28 → Jan 5, 2027)**: Because the tariffs are currently *proposed*—with critical carve-outs for Section 232 goods, select semiconductors, patented pharmaceuticals, and critical raw materials (*Legal500*)—boards have exactly **38 days** before the January 5 comment deadline to audit HTS codes, file exclusion petitions, and re-price 2027 margins.

---

## 1. Verified Tariff Matrix & Exemption Map (14 Targeted Economies)

| Tier | Targeted Economies | Proposed Cap (Baseline / Deal-Linked) | Tail-Risk / Conditional Rate | Strategic Supply-Chain Impact |
| :---: | :--- | :---: | :---: | :--- |
| **Tier 1** | **Vietnam** | **20%** *(with bilateral deal)* | **Up to 35%** | Highest headline exposure; acute shock to U.S. apparel, footwear, furniture, and consumer-electronics assembly. |
| **Tier 2** | **India** | **17%** *(with bilateral deal)* | **Up to 25%** | Squeezes iPhone/electronics assembly diversification & industrial manufacturing hubs. |
| **Tier 3** | **China** | **+20%** *(layered on prior 301)* | **Up to 40%** *(if truce breaks)* | Compounds existing Section 301 stack; no energy carve-out applies to China (*S&P Global*). |
| **Tier 4** | **Singapore** | **10%** *(pathway under deal)* | **Up to 20%** | Impacts regional re-export, precision instrumentation, and med-tech hubs. |
| **Tier 5** | **Indonesia, Malaysia, Thailand, Cambodia, Bangladesh** | **Up to 18%** | **18%** | Eliminates low-cost ASEAN/South Asian transshipment arbitrage across textiles, solar/EV components, and OSAT packaging. |
| **Tier 6** | **EU, Japan, South Korea, Taiwan, Switzerland** | **15%** *(generally net of MFN/prior 301)* | **15%** | Compresses European/East Asian industrial machinery, precision tools, and specialty chemicals margins. |
| **Deferred** | **Mexico, Norway** | *No determination issued* | *Investigation left open* | **Mexico (USMCA)** emerges as the #1 nearshoring pressure-valve—though open investigation preserves leverage. |

**Critical Statutory Carve-Outs (*Legal500*, *S&P Global*)**:
- Products already covered by **Section 232** (steel, aluminum, copper, automobiles & auto parts);
- **Specific semiconductor articles**, patented pharmaceuticals, and critical domestic-manufacturing raw materials;
- Energy products (crude oil, LNG, coal) for the 13 non-China economies;
- General "netting" rules prevent infinite stacking on top of MFN/prior Section 301 rates (varies by country).

---

## 2. Engine Simulation Output (`Crisis Rehearsal Pro 0.5.0`)

We ran two deterministic corporate & supply-chain stress tests in `crh dynamics` (`model/params.v1.json`) comparing **Fast Pre-Jan-5 Execution (`T+4h`, `shock=0.76`)** against **Delayed Wait-and-See / Retaliatory Escalation (`T+18h`, `shock=0.91`)**:

| Corporate / Macro Regime | Option B: HTS Audit + Jan-5 USTR Filing + Dual-Sourcing & Margin Guidance (Recommended) | Option A: Wait-and-See Silence | Option C: Unhedged Margin Absorption / Public Confrontation | Commercial & Market Consequence |
| :--- | :--- | :--- | :--- | :--- |
| **Regime 1: Fast Supply-Chain Governance**<br>(`shock=0.76`, `delay=4h`) | **`V_max = 0.3169` (-49.8%)**<br>**`Long-tail = 16h` (-87.7%)**<br>`Residual = 0.4843` (`0.0246` at T+72h) | `V_max = 0.6308`<br>`Long-tail = 130h`<br>`Residual = 0.8339` | `V_max = 1.0000`<br>`Long-tail = 130h`<br>`Residual = 1.0000` | Secures HTS carve-outs before Jan 5, locks Mexico/bonded-warehouse capacity early, and stabilizes institutional earnings guidance. |
| **Regime 2: Delayed Response + Retaliation**<br>(`shock=0.91`, `delay=18h`) | **`V_max = 0.3735` (+17.9%)**<br>**`Long-tail = 31h` (+93.8%)**<br>`Residual = 0.5488` (`0.0276` at T+72h) | `V_max = 0.6297`<br>`Long-tail = 130h`<br>`Residual = 0.8334` | `V_max = 1.0000`<br>`Long-tail = 130h`<br>`Residual = 1.0000` | **Delay nearly doubles the tail (16h → 31h)**: freight rates spike on front-loading, Mexico capacity books out, and Q1 2027 gross-margin shock hits stock prices. |

### Parameter Sensitivity Ranking (`±20%` OAT Perturbation)
1. **`channels.tier1_press.alpha` (`swing = 0.0146`)** — Financial press coverage of retaliatory threats from the EU/China/ASEAN and U.S. CPI pass-through drives immediate sector-wide equity repricing.
2. **`channels.social_feed.alpha` (`swing = 0.0115`)** — Consumer price-hike viral backlash and retail brand boycotts.
3. **`channels.short_video.alpha` (`swing = 0.0110`)** — Port congestion and price-tag comparison clips accelerating inflation expectations.

---

## 3. Macro, Sector & Equity Impact Forecast (Q4 2026 – Q2 2027)

### 3.1 Macro & Federal Reserve Collision
- With Q3 2026 U.S. GDP revised to **4.3%** and October **Core PCE already at 3.3% YoY** (3-year high), imposing 15%–35% baseline tariffs across 14 major manufacturing partners injects a direct **cost-push inflation shock** into 2027 goods prices.
- **Conditional Probability Bands (Next 6 Months)**:
  - **Negotiated Bilateral Rate Caps Implemented (10%–20% effective band for allies/deals)**: **55% – 65%** (Primary Base Case — Vietnam/India/EU negotiate toward lower caps before final enforcement).
  - **Full Escalation & Retaliatory Trade War (35%–40% tail rates + EU/China countermeasures)**: **20% – 30%** (Triggers stagflation risk: sticky Core PCE >3.5% colliding with slowing global PMI).
  - **Judicial Stay or Broad Congressional Rollback**: **15% – 20%** (Lower than prior emergency-tariff challenges because Section 301 rests on established statutory authority).

### 3.2 Winners vs. Exposed Sectors
- **Most Exposed (Margin Compression Risk)**: U.S. apparel, footwear, furniture, consumer electronics, and retail importers heavily concentrated in **Vietnam (up to 35%)**, **Bangladesh/Cambodia (18%)**, and **China (+20% layered)**; European/Japanese industrial machinery exporters (15%).
- **Protected / Relative Beneficiaries**:
  - **Mexico / USMCA Nearshoring & North American Logistics/Rail** (deferred from Nov 25 determinations);
  - **Exempted Frontier Semiconductors & Patented Pharma** (carved out to prevent domestic shortages);
  - **U.S. Domestic Industrial & Automation Suppliers** gaining pricing umbrellas under 15%–35% import floors.

---

## 4. Boardroom Survival Playbook: Before the January 5, 2027 Deadline

### What Corporate Boards MUST NOT DO (Option C Traps)
1. **Do NOT wait until January 25 hearings to map Tier-2/Tier-3 origin** — By late January, ocean freight front-loading and Mexico contract-manufacturing slots will be fully booked at 2×–3× spot premiums.
2. **Do NOT assume "Vietnam/India = safe from China tariffs"** — The Nov 25 ruling explicitly targets Vietnam (up to 35%) and India (up to 25%); legacy "China Plus One" decks are now obsolete.
3. **Do NOT hide tariff exposure from equity analysts** — Institutional silence (`Option A`, `130h` tail) triggers steeper multiple compression than transparent scenario-banded margin guidance.

### What Corporate Boards MUST DO (Option B — 38-Day Execution Sprint)
1. **Complete Full HTS Code & Carve-Out Audit by December 15, 2026** — Identify every SKU qualifying for Section 232, semiconductor, pharma, or critical raw-material exemptions, and verify exact "netting" math vs. existing MFN/301 rates.
2. **File Formal USTR Written Comments & Hearing Requests Before January 5, 2027** — Coordinate through industry trade associations and legal counsel to lock in technical exclusions and phased implementation windows.
3. **Activate Dual-Track Margin & Supply-Chain Buffers** — Pre-book bonded warehouse / Foreign Trade Zone (FTZ) capacity, evaluate USMCA/Mexico final-assembly qualification, and publish clean 2027 gross-margin sensitivity bands (Base 15–20% vs. Tail 35%).

---

## 5. Reproducibility

```bash
# Regime 1: Fast Supply-Chain Governance (T+4h, shock=0.76)
crh dynamics --title "USTR Section 301 Overcapacity Tariffs R1" --shock 0.76 --delay 4 --sensitivity --json

# Regime 2: Delayed Response + Retaliation (T+18h, shock=0.91)
crh dynamics --title "USTR Section 301 Overcapacity Tariffs R2" --shock 0.91 --delay 18 --sensitivity --json
```

> **Disclaimer**: This dossier is a non-partisan, deterministic trade and supply-chain stress test produced by `Crisis Rehearsal Pro 0.5.0` based on public November 25, 2026 USTR filings and legal/market analyses. It is **not** legal, customs, or investment advice.
