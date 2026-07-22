# Open Banking in Canada: Threat or Opportunity for the Big Six?

**A business/data analyst portfolio project** — forecasting Canada's open banking adoption curve, modeling revenue-at-risk for Canada's six largest banks, and delivering a strategic recommendation, backed by a full BI workflow from requirements through executive presentation.

**Author:** Jatin Sagwal — Business Analyst
**Status:** Complete (portfolio / demonstration project)
**Date:** July 2026

\---

## The problem

Canada's Consumer-Driven Banking Act received Royal Assent in March 2026, establishing the country's first open banking framework. Roughly 9 million Canadians already share bank credentials with third-party apps through unregulated screen scraping — the exact behavior the Act is designed to replace with secure, regulated data sharing.

This project answers the question every Big Six bank is currently facing: **how exposed is retail banking revenue to fintech disintermediation as open banking rolls out, and what should a bank's strategic response be** — defend, partner, or build?

## Approach

Rather than treat this as an isolated Canadian question, the analysis benchmarks Canada against markets that have already been through this transition — the UK and Australia (mandated regimes, like Canada) and the US (a market-led, voluntary-standards regime) — to build a defensible, evidence-based adoption forecast rather than a guess.

**Five-phase structure:**

1. **Canada baseline** — regulatory timeline, at-risk population, government cost/benefit estimates
2. **UK adoption curve** — the primary forecasting template (mandated-regime precedent)
3. **Comparison data** — US, Australia, EU, India, used to stress-test the Canada forecast
4. **Canada forecast model** — three adoption scenarios (conservative/base/optimistic) built from the UK curve
5. **Revenue-at-risk \& competitive layer** — Big Six financials, product-line exposure, and strategic posture

## What's in this deliverable set

|File|What it is|
|-|-|
|`Stakeholder\_Requirements\_Document.docx`|Business problem, stakeholder map, primary requirements|
|`Project\_Requirements\_Document.docx`|Project purpose, prioritized requirements, success criteria, assumptions, roll-out plan|
|`Strategy\_Document.docx`|Full dashboard specification — every chart, metric, and dimension|
|`Raw\_Bank\_Financials.xlsx`|Extracted FY2025 financials for all six banks (RBC, TD, BMO, CIBC, Scotiabank, National Bank) — total-bank, P\&C-segment, and fee-level detail, pulled directly from each bank's annual report|
|`PSD2\_PSD3\_Data\_Tracker.xlsx`|EU regulatory and adoption data, with an explicit note on the EU's data-fragmentation problem as a citable finding|
|*(master Excel workbook, held locally)*|Full data-to-model pipeline: raw country data → adoption forecast → revenue-at-risk calculation → Power BI-ready feed tables|
|*(Power BI dashboard, held locally)*|Interactive version of the four charts below, built from the Excel feed tables|
|`Open\_Banking\_Canada\_Executive\_Deck.pptx` / `.pdf`|Executive presentation summarizing the full analysis and recommendation|

## The four core analyses

1. **Adoption Curves** — Canada's forecast (3 scenarios) benchmarked against UK, US, and Australia adoption trajectories, aligned by years-since-launch rather than calendar year
2. **Revenue-at-Risk by Product Line** — \~$2.5B in estimated Big Six exposure (base case), broken out by payments, lending, and deposit/account fees
3. **CDBA Regulatory Milestone Tracker** — Royal Assent → Phase 1 (read access) → Phase 2 (write/payments)
4. **Strategic Posture Map** — where each of the Big Six currently sits on public commitment vs. digital/fintech exposure

## Key finding

TD, RBC, and BMO have already moved — jointly building **Cor.Connect**, a platform to control how open banking data flows to third parties — while CIBC has publicly described itself as at a "crossroads." Fintechs are lobbying against bank-controlled data gatekeeping. The strategic window to choose a position (defend / partner / build) is open now, and narrowing.

## Data sources

Built entirely from publicly available data — no proprietary or confidential information used:

* **Regulatory:** Canada Gazette, CFPB, EBA, Open Banking Ltd (UK), CDR.gov.au (Australia)
* **Market data:** FDX/CoinLaw (US), Sahamati (India), Konsentus (EU), Juniper Research (global)
* **Company filings:** Big Six FY2025 Annual Reports (SEDAR+)
* **Trade press:** The Logic, Open Banking Expo, McMillan LLP, DLA Piper, The Payments Association

Full source-by-source citation log is maintained in the project's data tracking workbooks.

## Skills demonstrated

Business requirements gathering · stakeholder analysis · primary and secondary research · financial statement analysis · quantitative forecasting/modeling · Excel (Power Query, formula-driven modeling) · Power BI (data modeling, DAX, dashboard design) · executive communication and presentation design.

## A note on scope

This is a portfolio project built to demonstrate an end-to-end BI workflow, not a commissioned engagement. The "client/sponsor" referenced in the requirements documents is a persona created for realism. Modeling assumptions (e.g., product-line revenue exposure percentages) are flagged explicitly where estimated rather than sourced — see the Strategy Document and PSD2/PSD3 tracker for the full caveat list.

\---

