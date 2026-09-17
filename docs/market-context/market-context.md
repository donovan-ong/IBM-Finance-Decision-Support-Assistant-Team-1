# Market Context

| | |
|---|---|
| **Document ID** | POL-DATA-003 |
| **Version** | 0.1 |
| **Status** | Proposed / Pending Approval |
| **Owner** | Raghdah Al-Gahdari, Business Analyst |
| **Approved by** | [pending] |
| **Last updated** | 2026-09-17 |
| **Applies to** | AI Finance Decision Support — Team 1, built for IBM |

---

## 1. Purpose

This document defines the external economic, industry, and market factors that the Assistant may use when explaining financial variances. It also outlines how these factors should be retrieved, weighted, and cited. This provides the external-driver component of the Explain step described in `business-rules.md` (POL-DATA-002), Section 7.

The document does not cover materiality thresholds, variance classification, or the quantitative and qualitative materiality tests. These are defined in `business-rules.md` (POL-DATA-002), Sections 4–5. Data provenance and confidentiality requirements are covered in `synthetic-data-policy.md`, while calculation formulas are defined in `Financial_Calculation_Formulas.md`.

---

## 2. Scope

This document applies to the same seven financial categories, grouped into the same three Category_Group values, defined in `business-rules.md` (POL-DATA-002), Section 2:

| Category | Category_Group |
|---|---|
| Revenue | Revenue |
| Cost of Goods Sold | COGS |
| Payroll Expense | Expense |
| Marketing Expense | Expense |
| Rent Expense | Expense |
| Utilities Expense | Expense |
| Other Expense | Expense |

All mappings defined in Section 5 must use the following Category_Group values exactly as specified: **Revenue, COGS, and Expense**. These values constitute a strict technical dependency between the Classify and mapping steps. The Assistant performs mapping lookups using the Category_Group value generated during classification. Any inconsistency in naming or formatting may result in a lookup failure without generating an explicit error.

---

## 3. Relationship to the Assumed Business Scenario

This document adopts, but does not redefine, the business scenario specified in `business-rules.md` (POL-DATA-002), Section 3. The assumed scenario is a **mid-sized clothing retail business, located in Melbourne, Victoria**, where Cost of Goods Sold is the primary cost driver, gross margins are moderate and relatively stable, and discretionary categories such as Marketing and Other Expense may fluctuate due to campaign timing without necessarily indicating a business issue.

The materiality thresholds defined in `business-rules.md`, Section 5.1, were calibrated against this scenario. Accordingly, the weighting assigned to market context in Section 4 is based on the same assumptions.

If the underlying business scenario changes, the Section 4 priority table must be reviewed together with the Section 5.1 materiality thresholds in accordance with the governance process defined in Section 10.

---

## 4. Category Priority for Market Context

Not every category benefits equally from an external market explanation. Under the assumed scenario, priority is assigned as follows:

| Category_Group | Priority | Rationale |
|---|---|---|
| COGS | High | Largest cost driver under the assumed scenario (business-rules.md §3); variable and tied to supplier pricing (§5.1). |
| Revenue | High | Demand-driven core metric (business-rules.md §5.1); most retail revenue shortfalls trace to demand or competitor activity. |
| Utilities Expense | Medium | Semi-variable, seasonal/usage-driven (business-rules.md §5.1); market context is secondary to seasonality. |
| Marketing Expense | Low | Deviations are expected to reflect planned campaign timing, not an external driver (business-rules.md §5.1). |
| Other Expense | Low | Discretionary/miscellaneous by nature; a wide threshold band already absorbs routine fluctuation (business-rules.md §5.1). |
| Rent Expense | Low | Fixed contractual cost; a deviation is more likely to require qualitative review under business-rules.md, Section 5.2, than to be explained by an external market driver. |
| Payroll Expense | Low | Fixed/semi-fixed, headcount-driven; rarely explained by external market conditions. |

For low-priority categories, the Assistant should not proactively search for external market drivers. However, an external factor may still be surfaced where a qualitative trigger under `business-rules.md`, Section 5.2, independently indicates that the factor may be relevant.

---

## 5. External Factor Mapping

Each Category_Group is mapped to the external factor category most likely to explain its variance, the specific indicator to retrieve, and a reference source type:

| Category_Group | Factor Category | Indicator to Retrieve | Reference Source Type |
|---|---|---|---|
| COGS | Industry / Market | Raw material price – Cotton, A Index | World Bank Commodity Price Data (Pink Sheet) — CMO-Historical-Data-Monthly.xlsx, Sheet: Monthly Prices, Column: Cotton, A Index |
| Revenue | Market | Consumer demand – Clothing and footwear spending | ABS Monthly Household Spending Indicator — 5682002.xlsx, Sheet: Data1, Column 25: Household spending – Through the year percentage change; Clothing and footwear; Australia; Current Price |
| Revenue / COGS | Economic | Exchange rate – AUD/USD | RBA Table F11.1 — 2023-current.xls, Sheet: Data, Column B: A$1=USD |
| Expense | Economic | Inflation rate | ABS Consumer Price Index — ABS_Consumer_Price_Index_Australia.xlsx, Sheet: Data1, Column K: Percentage Change from Corresponding Month of Previous Year; All groups CPI; Australia |
| Expense | Economic | Interest rate – Cash Rate Target | RBA Table F1.1 — f01hist.xlsx, Sheet: Data, Column B: Cash Rate Target |
| Utilities Expense | Market | Electricity price – Victorian Default Offer (VDO) | Essential Services Commission (ESC) Victoria — Victorian Default Offer (VDO), small business figures. One confirmed annual figure per financial year (1 Jul–30 Jun), applied to all months in that year: 2024–25 = $3,530; 2025–26 = $3,620; 2026–27 = $3,380. AER's Default Market Offer does not apply to Victoria and is not used here. |

---

## 6. Position within the Assistant Workflow

Market context is retrieved and used exclusively within the Explain step of the Assistant workflow defined in `business-rules.md` (POL-DATA-002), Section 7:

**Detect → Calculate → Classify → Explain → Present → Human Decision**

Market context is retrieved only after a variance has passed the quantitative materiality test (business-rules.md §5.1) or triggered a qualitative test (§5.2). It is never used at the Detect, Calculate, or Classify steps, which remain strictly rule-based and are not affected by this document.

---

## 7. Language and Evidentiary Standard

Consistent with `business-rules.md` Section 6, an external market factor is **judgement-informed, not rule-based**. The Assistant must never present a market-context explanation with the same certainty as a rule-based calculation. Specifically, the Assistant:

- Must use probabilistic language only e.g. "may have contributed," "could be associated with," or "may be consistent with."
- Must never assert that an external factor is the confirmed cause of a variance.
- Must cite the specific indicator value, period, and source used, for every market-context statement (Section 8).
- When no market data is available for the relevant reporting period, explicitly state: "No matching market context is available for this period." The Assistant must not substitute the most recent available value for the missing period.

---

## 8. How the Assistant Retrieves and Cites Market Context

The Assistant does not generate market-context claims from its own training knowledge. It retrieves a pre-stored, sourced data record and inserts it into a constrained explanation. This section defines that mechanism.

### 8.1 Stored indicator record

Every external indicator held in the system's reference data is stored with four fields, all of which travel together and are never separated:

| Field | Example |
|---|---|
| Value | 9% increase |
| Period | June 2026 |
| Source name | World Bank Commodity Price Data |
| Source reference | worldbank.org (Pink Sheet) |

### 8.2 Period-matched retrieval

When a variance is flagged for a specific category and period, the Assistant looks up the indicator mapped to that Category_Group (Section 5) for the same period as the variance — not the latest available value. If no record matches that period, the Assistant states that no matching market context is available rather than substituting a different period's value.

### 8.3 Constrained explanation construction

The Assistant must apply the relevant rules defined in `business-rules.md` before incorporating external market context into an explanation.

The Assistant first calculates the variance and presents the relevant calculation steps and result. It then applies the materiality and qualitative criteria defined in `business-rules.md` to determine whether the variance requires further explanation.

Where the applicable criteria are met, the Assistant may use the period-matched market indicator retrieved in Section 8.2 to provide supporting context for the variance.

Market context must not override or influence the calculation or classification determined by the business rules. It is used solely to support the explanation of an identified variance.

The Assistant must not use general knowledge to introduce external facts that are not contained in the retrieved market indicator record. If no matching market context is available for the relevant period, the Assistant must state this explicitly rather than infer or substitute information from another period.

### 8.4 Citation format

Every market-context statement the Assistant produces follows a fixed citation pattern, with the source appended automatically rather than left to the model's discretion:

> "The [X%] variance in [Category] may be partly consistent with the [Y%] change in [Indicator] observed during [Period] (Source: [Source name])."

### 8.5 Output validation

Before an Explain-step output is presented, it must pass validation checks to ensure that:

- The explanation uses non-assertive language in accordance with Section 7.
- Any referenced market-context indicator includes the required source citation in accordance with Section 8.4.

If either validation check fails, the output must be rejected and regenerated before being presented to the analyst.

---

## 9. Relationship to Other Governing Documents

| Document | Relationship to this Document | Owner |
|---|---|---|
| `business-rules.md` (POL-DATA-002) | Defines the assumed scenario (§3) this document's priorities rely on, and the workflow step (§7) in which this document is used | Business Analyst |
| `synthetic-data-policy.md` (POL-DATA-001) | Governs provenance and confidentiality of the underlying dataset; this document assumes that policy's requirements are already satisfied. | Business Analyst |
| `Financial_Calculation_Formulas.md` | Defines the financial and variance calculations that provide the basis for the market-context explanation. | Business Analyst |
| `CSV_SQL_Data_Structure_Specification.md` | Defines the Category_Group values referenced in Sections 2 and 5 | Technical team, reviewed by BA |

---

## 10. Governance

- Any change to the assumed business scenario in business-rules.md §3 requires this document's priority table (Section 4) to be reviewed in the same review cycle.
- Any change to the mapping table (Section 5) or the citation mechanism (Section 8) requires BA sign-off and a version increment.
- This document moves from "Proposed" to "Approved" once reviewed and confirmed alongside `business-rules.md` (POL-DATA-002).

### Changelog

| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-09-17 | Initial draft, derived from prior market-context research and aligned to business-rules.md (POL-DATA-002) | Raghdah Al-Gahdari |

### Sign-off

By approving this document, the Supervisor confirms that the external-factor mapping, priorities, and citation rules outlined above have been reviewed and approved for use within the project.

| Role | Name | Signature | Date |
|---|---|---|---|
| Supervisor / Approver | Aaron | | |

---

## References

Australian Bureau of Statistics. (n.d.). *Consumer price index, Australia*. Retrieved September 17, 2026, from https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/latest-release

Australian Bureau of Statistics. (n.d.). *Monthly household spending indicator*. Retrieved September 17, 2026, from https://www.abs.gov.au/statistics/economy/finance/monthly-household-spending-indicator/latest-release

Essential Services Commission. (2025). *Victorian Default Offer price review 2025–26*. https://www.esc.vic.gov.au/electricity-and-gas/prices-tariffs-and-benchmarks/victorian-default-offer/victorian-default-offer-price-review-2025-26

Reserve Bank of Australia. (n.d.). *Historical data*. Retrieved September 17, 2026, from https://www.rba.gov.au/statistics/historical-data.html

Reserve Bank of Australia. (n.d.). *Interest rates* [Statistical tables]. Retrieved September 17, 2026, from https://www.rba.gov.au/statistics/tables/#interest-rates

World Bank. (n.d.). *Commodity markets*. Retrieved September 17, 2026, from https://www.worldbank.org/en/research/commodity-markets
