# Canada NATO Defence Spending Gap Analysis

A business analyst portfolio project analyzing Canada's defence spending trajectory against NATO's benchmarks — from the 2% target Canada just reached to the new 5% target set for 2035.

**Author:** Jatin Sagwal

---

## Project Summary

Canada crossed NATO's 2% of GDP defence spending benchmark in FY2025-26 after 35 years of missing it. In the same period, NATO raised its collective target to 5% of GDP by 2035 (3.5% core defence + 1.5% security-related infrastructure). This project quantifies where Canada actually stands, how it compares to NATO peers, and what closing the new gap will cost — using only public, primary-source data.

The project follows a full business analyst workflow: stakeholder and requirements documentation, a data and analytics strategy, a Power BI data model and dashboard, and a set of published deliverables (presentation deck, PDF, and LinkedIn article) summarizing the findings.

## Key Findings

- Canada's defence spending grew from ~$20B (2014) to a projected $71.5B (2026) — a rise from 1.01% to 2.13% of GDP
- Despite the increase, Canada ranks 19th of 30 NATO members on % of GDP (2026 estimate)
- The projected funding gap to reach the new 3.5% core target is heavily back-loaded: near-zero through the early 2030s, then an estimated $68.2B jump in 2035-36 alone
- Reaching the 3.5% core target is projected to add ~6.3 percentage points to Canada's debt-to-GDP ratio by 2035-36

## Repository / Folder Contents

| File | Description |
|---|---|
| `Stakeholder_Requirements_Document.docx` | Stakeholder identification, RACI matrix, communication plan |
| `Project_Requirements_Document.docx` | Scope, functional/non-functional requirements, data requirements, timeline |
| `Strategy_Document.docx` | Analytical approach, data strategy, delivery roadmap, risk register |
| `PowerBI_Build_Guide.md` | Power Query M code, data model relationships, DAX measures, chart-by-chart build steps |
| `Canada_NATO_Defence_Spending_Analysis.pptx` / `.pdf` | 13-slide presentation deck with native, data-driven charts |
| `LinkedIn_Article_Canada_NATO_Spending.md` | Full-length LinkedIn article on the findings |
| `README.md` | This file |

*(Raw source data files — NATO expenditure data, StatCan GDP data, PBO fiscal reports — are used as inputs but not redistributed here; see Data Sources below to pull them directly.)*

## Data Sources

All data is public and primary-source. No proprietary or internal data was used.

| Source | Link |
|---|---|
| NATO Annual Defence Expenditure Report 2026 | https://www.nato.int/content/dam/nato/webready/documents/finance/def-exp-2026-en.pdf |
| Statistics Canada, Table 36-10-0104-01 (GDP) | https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610010401 |
| Parliamentary Budget Officer — Fiscal Implications of Meeting NATO's 5% Commitment (Feb 2026) | https://www.pbo-dpb.ca/en/publications/RP-2526-022-S--fiscal-implications-meeting-nato-5-commitment--repercussions-financieres-atteinte-cible-5-otan |
| Department of National Defence — 2% milestone announcement | https://www.canada.ca/en/department-national-defence/news/2026/03/canada-achieves-the-2-of-gross-domestic-product-defence-spending-benchmark.html |

## Methodology

1. **Stakeholder & requirements definition** — see `Stakeholder_Requirements_Document.docx` and `Project_Requirements_Document.docx`
2. **Data sourcing & cleaning** — Power Query used to unpivot, type-shape, and validate all datasets (see `PowerBI_Build_Guide.md`)
3. **Data modeling** — star schema built in Power BI, with a Year dimension table joined to four fact tables (Canada absolute spend, NATO peer % of GDP, PBO fiscal scenarios, StatCan GDP)
4. **Analysis** — trend analysis, peer benchmarking, and scenario/gap modeling using DAX measures
5. **Visualization** — 8-visual Power BI dashboard (2 pages) plus a 13-slide presentation deck with independently rebuilt native charts
6. **Publication** — findings summarized in a LinkedIn article and presentation deck for external audiences

## Tools Used

- **Power Query** — data cleaning and shaping
- **Power BI Desktop / Service** — data modeling, DAX, dashboard, publishing
- **DAX** — % of GDP, YoY change, NATO rank, gap and scenario calculations

## Limitations & Assumptions

- 2025 and 2026 figures are NATO/PBO estimates, not final actuals, and may be revised
- The PBO's published fiscal path includes a full funding-gap figure only for the terminal year (2035-36), not an interim year-by-year glide path; this is reflected as-is rather than interpolated
- Analysis uses nominal (current-price) GDP throughout, consistent with NATO's own reporting methodology

## Contact

**Jatin Sagwal**
