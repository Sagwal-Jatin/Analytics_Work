# Canadian Federal Procurement Analysis

### Competition, Vendor Concentration \& Spending Risk — FY2015–FY2026

An independent business intelligence project analyzing **$738 billion** in Government of Canada contract spending, built on the Open Government Portal's proactive-disclosure dataset. The project identifies competition gaps, vendor concentration risk, regional spending patterns, and equity-target performance across federal departments.

**Author:** Jatin Sagwal
**Tools:** Python (pandas, RapidFuzz) · SQL (DuckDB) · Power BI · GitHub

\---

## Business Question

> How competitive and concentrated is federal government procurement in Canada, and where are the highest-risk spending patterns — such as sole-source reliance, vendor concentration, and inequitable outcomes?

Federal procurement data is public, but no consolidated, decision-ready view exists that translates the raw disclosure files into insight on competition levels, vendor concentration, and spending risk. This project builds that view.

\---

## Key Findings

|Finding|Result|
|-|-|
|**Competition gap**|Only **4.5%** of $738.3B in total contract value was openly competitive; **57.1%** was sole-sourced / non-competitive|
|**Department concentration**|**National Defence** alone accounts for **$442.8B (60%)** of all federal contract value — more than the next five departments combined|
|**Vendor concentration**|After fixing a vendor-name inconsistency in the raw data, **Irving Shipbuilding Inc.** is the true #1 vendor at **$44.4B**, not Vancouver Shipyards ($25.9B)|
|**Market concentration (HHI)**|Average department-level HHI is **757.6** (competitive), but 5 departments — including Canadian Space Agency and Housing, Infrastructure \& Communities — exceed 2,500 (highly concentrated)|
|**Indigenous set-aside gap**|**91% of departments (65 of 71)** fall below the federal government's mandatory 5% Indigenous set-aside target; the government-wide weighted average is just **0.28%**|
|**Regional distribution**|Ontario (45.2%), BC (21.6%), Quebec (15.9%), and Nova Scotia (9.8%) dominate vendor location — largely explained by shipbuilding mega-contracts (Vancouver Shipyards, Irving Shipbuilding), not broad regional policy|
|**Trade-agreement exemption**|Parks Canada (94.4%), Crown-Indigenous Relations (78.8%), and Canadian Heritage (78.8%) have the highest share of exempt (lower-scrutiny) contract value|

Full narrative and supporting charts: see [`Procurement\_Analysis\_Presentation.pdf`](./Procurement_Analysis_Presentation.pdf).

\---

## Data Source

* **Dataset:** [Proactive Publication - Contracts](https://open.canada.ca/data/en/dataset/d8f85d91-7dec-4fd1-8055-483b77225d8b), Open Government Portal
* **Publisher:** Treasury Board of Canada Secretariat
* **Scope:** All federal contracts ≥ $10,000, all departments and agencies, FY2015–FY2026
* **License:** Open Government Licence – Canada
* **Note:** Data is self-reported and unaudited by the publishing departments

\---

## Methodology

**1. Clean — Python (pandas, RapidFuzz)**
Parsed and typed raw fields, converted calendar dates to Government of Canada fiscal years (April–March), and standardized inconsistent vendor names (e.g. merging "Irving Shipbuilding Inc" and "Irving Shipbuilding Inc." into one entity) using fuzzy string matching.

**2. Aggregate — SQL (DuckDB)**
Wrote analytical SQL queries to calculate:

* Competitive vs. sole-source value by department
* Top vendors by total contract value
* Market concentration (Herfindahl-Hirschman Index) by department
* Indigenous set-aside performance vs. the 5% PSIB target
* Regional vendor distribution by postal code
* Award-to-delivery efficiency (mean/median days)
* Trade-agreement coverage (exempt vs. covered value)

**3. Visualize — Power BI**
Built a two-page interactive dashboard with a shared design system:

* **Page 1 — Executive Summary:** procurement strategy breakdown, market concentration index, top 10 vendors, monthly award-volume trend
* **Page 2 — Operational Efficiency \& Compliance:** trade-agreement coverage, delivery efficiency, regional distribution, Indigenous set-aside progress

\---

## Repository Structure

```
├── README.md
├── data/
│   ├── raw/                        # original contracts.csv (not included — see Data Source)
│   └── clean/                      # 8 cleaned, aggregated CSVs (one per chart)
├── notebooks/
│   └── 01\_cleaning.ipynb           # Python data cleaning \& vendor standardization
├── sql/
│   └── queries.sql                 # DuckDB queries for all 8 metrics
├── dashboard/
│   ├── procurement\_dashboard\_theme.json   # Power BI theme (colors match this deck)
│   └── dashboard\_screenshots/      # exported visuals (Power BI files aren't renderable on GitHub)
├── docs/
│   ├── Stakeholder\_Requirements\_Document.docx
│   ├── Project\_Requirements\_Document.docx
│   └── Strategy\_Document.docx
└── Procurement\_Analysis\_Presentation.pdf / .pptx
```

\---

## Skills Demonstrated

* **Data cleaning \& entity resolution** — fuzzy matching to reconcile inconsistent vendor names at scale
* **SQL** — aggregation, window functions, and analytical queries in DuckDB
* **Statistical methods** — Herfindahl-Hirschman Index for market concentration
* **BI dashboard design** — two-audience (executive vs. operational) dashboard architecture with a consistent visual system
* **Requirements documentation** — stakeholder, project, and strategy documents following standard BI project practice
* **Data storytelling** — translating raw disclosure data into a decision-ready narrative

\---

## Limitations

* **Unaudited data:** Treasury Board Secretariat publishes this data as-is; it has not been independently audited for accuracy or completeness.
* **Thresholds changed over time:** The competitive-bidding threshold has shifted across the FY2015–2026 window; this analysis applies current thresholds uniformly rather than the exact rule in force on each contract date.
* **"Sole-source" ≠ wrongdoing:** Legitimate reasons for sole-sourcing exist (national security, IP lock-in, urgency). Findings describe patterns worth further review, not proven fraud.
* **No internal justification data:** This analysis has no access to the procurement file behind each award — only the disclosed summary record.

\--

