# Business Rules

| | |
|---|---|
| **Document ID** | POL-DATA-002 |
| **Version** | 0.1 |
| **Status** | Proposed / Pending Approval |
| **Owner** | Raghdah Al-Gahdari, Business Analyst |
| **Approved by** | [pending] |
| **Last updated** | 2026-09-10 |
| **Applies to** | AI Finance Decision Support — Team 1, built for IBM |

---

## 1. Purpose

This document defines the **materiality thresholds, variance classification logic, and category-specific rules** used by the Assistant when detecting, calculating, classifying, and explaining financial variances.

It translates the findings in `synthetic-data-research.docx` (Section 2: Financial Variance and Materiality Research) into concrete, testable rules the Assistant applies against the project's dataset, as defined in `CSV_SQL_Data_Structure_Specification.docx` and `Financial_Calculation_Formulas.md`.

**This document does not** cover data provenance or confidentiality (see `synthetic-data-policy.md`), and does not cover external economic or industry drivers used to explain a variance (see `market-context.md`). It also does not determine whether the synthetic data itself is realistic — it defines the business logic the Assistant applies to whatever data it is given.

---

## 2. Scope

This document applies to the seven financial categories defined in the project schema (`CSV_SQL_Data_Structure_Specification.docx`, Section 3):

| Category | Category_Group |
|---|---|
| Revenue | Revenue |
| Cost of Goods Sold | COGS |
| Payroll Expense | Expense |
| Marketing Expense | Expense |
| Rent Expense | Expense |
| Utilities Expense | Expense |
| Other Expense | Expense |

---

## 3. Assumed Business Scenario

The research (`synthetic-data-research.docx`, Section 2.3) establishes that materiality and variance behaviour differ by industry. This project therefore adopts one explicit, fixed scenario, so that the thresholds in Section 5 have a real business justification rather than being arbitrary:

> **Assumed scenario: a mid-sized retail/services business**, with Cost of Goods Sold as its largest cost driver, moderate and relatively stable gross margins, and discretionary categories (Marketing, Other Expense) that are expected to fluctuate with campaign timing rather than signal a problem.

This scenario was chosen because it fits the category set already defined in the schema (a Revenue line, a COGS line tied to Revenue, and five expense lines split between fixed and discretionary spend) without requiring any change to the dataset structure. All thresholds and rules below are justified against this scenario, not against any property of the synthetic-data generator.

---

## 4. Variance Definitions

| Term | Meaning | Relevance to Project |
|---|---|---|
| Variance | Difference between actual and budgeted/expected value | Core calculation (Formula 1, `Financial_Calculation_Formulas.md`) |
| Favourable variance | Actual result is better than budget (e.g. lower expenses, higher revenue) | Used to classify the result |
| Unfavourable variance | Actual result is worse than budget (e.g. higher expenses, lower revenue) | Used to classify the result |
| Cost variance | Difference between actual cost and budgeted cost | Applies to COGS and all Expense-group categories |
| Revenue variance | Difference between actual revenue and budgeted revenue | Applies to the Revenue category |

### 4.1 Favourable / Unfavourable Classification Rule

| Category_Group | Actual > Budget | Actual < Budget |
|---|---|---|
| Revenue | Favourable | Unfavourable |
| COGS | Unfavourable | Favourable |
| Expense | Unfavourable | Favourable |

This rule applies to every category within a group. It is a fixed rule — no judgement is required to apply it.

---

## 5. Materiality: A Two-Part Test

Per the research (Section 2.4), materiality is **not size alone** — a variance is material if it could reasonably influence a decision-maker's judgement. Under the assumed scenario (Section 3), the Assistant applies both parts of the test below. A variance is treated as material if **either** part is triggered.

### 5.1 Part 1 — Quantitative Test (Rule-Based)

Fixed and predictable categories are given tighter thresholds than variable or discretionary ones, consistent with the research finding that "different financial items can have different levels of normal variation" (Section 2.3):

| Category | Predictability | Percentage Variance Threshold | Justification |
|---|---|---|---|
| Rent Expense | Fixed (contractual lease) | 3% | Contractual costs should not move without a known cause; any deviation is worth surfacing |
| Payroll Expense | Fixed/semi-fixed | 5% | Headcount-driven, changes gradually; a mid-size retail/services business would not expect large swings outside a hiring/restructuring event |
| Revenue | Demand-driven, core metric | 8% | Directly affects overall financial performance (Research 2.3.1); consistent with the "total revenue" materiality benchmark of 0.5–1% for a single line item is too tight at consolidated level, so 5% is used as the operating-variance threshold, distinct from statement-level materiality |
| Cost of Goods Sold | Variable, tied to Revenue and supplier pricing | 8% | Expected to move with sales volume and supplier costs; a retail/services business normally tolerates more movement here than in Revenue itself |
| Utilities Expense | Semi-variable (seasonal/usage) | 20% | Usage- and season-driven; normal fluctuation is expected and does not by itself indicate an issue |
| Marketing Expense | Discretionary | 30% | Campaign-timing driven; deviations commonly reflect planned business activity, not a problem (Research 2.3.1) |
| Other Expense | Discretionary/miscellaneous | 38% | Least predictable category by nature; a wide band avoids flagging routine, low-materiality fluctuations |

**Threshold Note:** 

 The thresholds presented above are proposed management defaults developed for the assumed mid-sized retail/services business scenario. Where applicable, thresholds were calibrated at approximately **2.5x the standard deviation of normal random variation (noise_std_pct)** built into the dataset generator for each category, consistent with the statistical Empirical Rule (Wikipedia contributors, 2026) and the logic used in Statistical Process Control, where control limits are set at 2.5-3x standard deviation to distinguish genuine signals from normal random fluctuation. This ensures that a flagged variance is unlikely to result from random noise alone (less than ~1% probability) and more likely reflects an actual business change. These thresholds are intended to support consistent variance assessment within this project and should not be interpreted as universal accounting or audit materiality thresholds. The proposed thresholds should be reviewed against the dataset generation assumptions and formally approved by the project team prior to implementation

### 5.2 Part 2 — Qualitative Test (Judgement-Based)

A variance is also treated as material, regardless of size, if any of the following apply:

- It relates to a category with compliance or regulatory reporting relevance.
- It suggests a possible data or process error (e.g. a value flagged under the Edge Case Handling Rules in `Financial_Calculation_Formulas.md`).
- It could reasonably be expected to affect a decision a reader of the analysis would make.

The qualitative test cannot be reduced to a fixed rule — it requires human judgement. The Assistant's role here is limited to **flagging** the variance and the reason it may be qualitatively relevant; it does not decide materiality on the analyst's behalf.

---

## 6. Rule-Based vs. Judgement-Based Behaviour

The research asks explicitly which Assistant behaviours should be rule-based and which should involve judgement. This project draws that line as follows:

| Behaviour | Basis | Owner of the Decision |
|---|---|---|
| Calculating Dollar Variance / Percentage Variance | Rule-based (fixed formula) | Assistant |
| Classifying Favourable / Unfavourable | Rule-based (Section 4.1) | Assistant |
| Comparing variance against the quantitative threshold (Section 5.1) | Rule-based | Assistant |
| Flagging a qualitative materiality trigger (Section 5.2) | Judgement-informed, but Assistant only flags — does not conclude | Assistant flags, Analyst confirms |
| Identifying a possible external driver (economic/industry/market) | Judgement-informed, using `market-context.md`, always in probabilistic language | Assistant proposes, Analyst evaluates |
| Deciding whether to investigate further or take action | Judgement | Financial Analyst only |

The Assistant must never present a judgement-based output (Section 5.2, or a driver from `market-context.md`) with the same certainty as a rule-based calculation. Rule-based outputs are stated as facts; judgement-informed outputs are stated as possibilities requiring analyst review.

---

## 7. Assistant Workflow

**Detect → Calculate → Classify → Explain → Present → Human Decision**

| Step | Assistant Action | Basis |
|---|---|---|
| Detect | Identify whether a variance exists for the requested category/period | Rule-based — `Financial_Calculation_Formulas.md` |
| Calculate | Compute the requested formula (Dollar/Percentage Variance, Gross Margin, PoP, YoY, Contribution) | Rule-based — `Financial_Calculation_Formulas.md` |
| Classify | Apply Section 4.1 (direction) and Section 5.1 (quantitative threshold) | Rule-based — this document |
| Explain | Flag any qualitative trigger (Section 5.2) and any relevant external driver (`market-context.md`), in probabilistic language | Judgement-informed — this document + `market-context.md` |
| Present | Present the result with full source traceability (file, row, column) | Rule-based — `Financial_Calculation_Formulas.md`, Source Traceability Requirements |
| Human decision | The financial analyst decides whether further investigation or action is required | Judgement — Analyst only |

The Assistant must not send alerts, escalate cases, approve budgets, override figures, or take corrective action at any step.

---

## 8. Relationship to Other Governing Documents

| Document | Relationship to this Document | Owner |
|---|---|---|
| `synthetic-data-policy.md` | Governs provenance and confidentiality of the underlying dataset; this document assumes that policy's requirements are already satisfied | Business Analyst |
| `market-context.md` | Supplies the external drivers used in the "Explain" step (Section 7) | Business Analyst |
| `Financial_Calculation_Formulas.md` | Defines the calculation logic this document's classification and threshold rules are applied on top of | Business Analyst |
| `CSV_SQL_Data_Structure_Specification.docx` | Defines the categories, fields, and schema this document's rules reference | Technical team, reviewed by BA |

---

## 9. Governance

- Any change to the assumed scenario (Section 3)requires BA sign-off and a version increment.
- Any change to the threshold values (Section 5.1) must be reviewed by the BA and formally approved by the Supervisor before implementation.
- This document moves from "Proposed" to "Approved" once the scenario and thresholds are formally confirmed.

### Changelog

| Version | Date | Change | Author |
|---|---|---|---|
| 0.1 | 2026-09-10 | Initial draft, derived from `synthetic-data-research.docx` Section 2 | Raghdah Al-Gahdari |

---

## 10. References

- Smalley, T. F. I. (2026, May 18). What is variance analysis? https://www.ibm.com/think/topics/variance-analysis

- IFRS - IAS 1 Presentation of Financial Statements. (n.d.). https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements/

- What is Variance Threshold? Definition, Process & Key Metrics. (n.d.). https://www.hyperbots.com/glossary/variance-threshold#formula-for-calculating-variance

- Team, C. (2026, May 11). Materiality threshold in audits. Corporate Finance Institute. https://corporatefinanceinstitute.com/resources/accounting/materiality-threshold-in-audits/

- What is Materiality? Accounting Definition - Navan. (2026, May 31). Navan. https://navan.com/resources/glossary/what-is-materiality

- A, A. (2026, April 14). Quantitative Materiality: How auditors calculate thresholds. CLFI. https://clfi.co.uk/resources/quantitative-materiality/#real-world-example

- Wikipedia contributors. (2026, August 10). 68–95–99.7 rule. Wikipedia. https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule


