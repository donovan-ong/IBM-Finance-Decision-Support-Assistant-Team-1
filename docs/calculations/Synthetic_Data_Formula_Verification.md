# SYNTHETIC DATA FORMULA VERIFICATION

Worked Examples — Formulas Checked Against the Generated Dataset

**Project:** IBM-AI-Powered Finance Decision Support Assistant — Team A

**Purpose:** For each of the six calculations and four edge-case rules in
[Financial_Calculation_Formulas.md](Financial_Calculation_Formulas.md), this
document pulls real rows from the generated synthetic dataset, computes the
expected result by hand, and states the exact source citation the assistant
should produce. It exists so the calculation implementation can be checked
against known-correct answers, rather than only against its own logic.

**Status:** Reference — regenerate the worked numbers below if the generator
script or its parameters change (see Reproducibility).

---

## 1. Reproducibility

The dataset used for every example below was produced by:

| Variable | Value |
| --- | --- |
| Script | `data/scripts/generate_synthetic_data.py` |
| Script version | commit `ea3322b` on branch `feature/synthetic-data-generator` |
| Command | `python3 data/scripts/generate_synthetic_data.py` |
| `RANDOM_SEED` | `42` |
| Interpreter | CPython 3.13.2 |
| Dependencies used by the script | Python standard library only (`csv`, `random`) — no third-party packages, so no library version pinning is needed beyond the interpreter itself |

Running the exact command above on the same CPython version with
`RANDOM_SEED = 42` reproduces the "clean" (non-edge-case) values in this
document bit-for-bit, because `random.gauss` is deterministic for a given
seed. The 18 seeded edge-case cells (see `EDGE_CASES` in the script) are
hardcoded overrides and do not depend on the seed at all.

**Note:** `pyproject.toml` currently pins `requires-python = ">=3.11,<3.13"`,
but this reference run used 3.13.2 (the only interpreter available in this
environment). The script has no version-specific behavior, but if the team
standardizes on an in-range interpreter (3.11 or 3.12), rerun the command
above and diff the output against `data/raw/` before trusting this document
as-is — Gaussian noise draws are seed-reproducible *within* a CPython
version, not guaranteed identical *across* major versions.

The generated CSVs themselves (`data/raw/*.csv`) are gitignored and are not
committed — this document is the durable record of what a from-seed run
produces, until/unless the generator changes.

---

## 2. Row/column reference

Every category block is written in this fixed order (see `CATEGORY_ORDER`),
so a cell's row number is always `2 + (month - 1) × 7 + category_index`,
header = row 1:

| Category | Index | Column (Actual / Budget) |
| --- | --- | --- |
| Revenue | 0 | E / F |
| Cost of Goods Sold | 1 | E / F |
| Payroll Expense | 2 | E / F |
| Marketing Expense | 3 | E / F |
| Rent Expense | 4 | E / F |
| Utilities Expense | 5 | E / F |
| Other Expense | 6 | E / F |

---

## 3. Dollar Variance & Percentage Variance

**Formula:** `Dollar Variance = Actual − Budget`; `Percentage Variance = (Actual − Budget) / |Budget| × 100`

**Normal case — Payroll Expense, 2025-06** (`financial_data_2025.csv`, Row 39)

| Field | Value | Citation |
| --- | --- | --- |
| Actual_Value | 42,535.61 | Row 39, Column E |
| Budget_Value | 43,060.55 | Row 39, Column F |

- Dollar Variance = 42,535.61 − 43,060.55 = **−$524.94**
- Percentage Variance = −524.94 / \|43,060.55\| × 100 = **−1.2%**

**Edge case — missing Actual (Rent Expense, 2025-01, Row 6, Column E blank).**
Expected: *"Dollar Variance cannot be calculated because Actual Value is
missing from financial_data_2025.csv, Row 6, Column E."* No substitution of
0 permitted.

**Edge case — missing Budget (Utilities Expense, 2025-04, Row 28, Column F blank).**
Expected: *"Percentage Variance cannot be calculated because Budget Value is
missing from financial_data_2025.csv, Row 28, Column F."*

**Edge case — Budget = 0 (Utilities Expense, 2025-05, Row 35, Column F = 0.00).**
Dollar Variance is still computable (2,118.42 − 0.00 = **$2,118.42**), but
Percentage Variance is not. Expected: *"Percentage variance cannot be
calculated because Budget Value is 0. financial_data_2025.csv, Row 35,
Column F."*

**Edge case — negative Budget (Marketing Expense, 2025-11, Row 75, Column F = −2,000.00).**
Actual = 7,166.90 (Row 75, Column E).
Percentage Variance = (7,166.90 − (−2,000.00)) / \|−2,000.00\| × 100 = **458.3%**.
This is arithmetically correct but must carry the required explanatory note
that the result reflects movement from a negative starting budget, or a
reader will misread 458.3% as ordinary overspend.

**Edge case — non-numeric text (Rent Expense, 2026-09, Row 62, Column E = `"N/A"`).**
Expected: *"Calculation cannot be completed because Actual Value must be a
numeric value. The invalid value was found in financial_data_2026.csv,
Row 62, Column E."*

**Edge case — non-numeric symbol (Utilities Expense, 2025-12, Row 84, Column F = `"#REF!"`).**
Same rule, applied to Budget_Value: *"...Budget Value must be a numeric
value. The invalid value was found in financial_data_2025.csv, Row 84,
Column F."*

**Edge case — full blackout (Other Expense, 2026-06, Row 43, both Column E and F blank).**
Neither Dollar nor Percentage Variance can be calculated; both the missing
Actual and missing Budget must be identified.

---

## 4. Gross Margin

**Formula:** `Gross Margin (%) = (Revenue − COGS) / Revenue × 100`

**Normal case — 2025-06** (`financial_data_2025.csv`)

| Field | Value | Citation |
| --- | --- | --- |
| Revenue Actual | 193,479.20 | Row 37, Column E |
| Cost of Goods Sold Actual | 99,335.24 | Row 38, Column E |

- Gross Margin = (193,479.20 − 99,335.24) / 193,479.20 × 100 = **48.7%**

**Edge case — Revenue = 0 (2026-02, Row 9, Column E = 0.00).**
Expected: *"Gross margin cannot be calculated because revenue is zero."*
(financial_data_2026.csv, Row 9, Column E)

**Edge case — Revenue negative (2026-04, Row 23, Column E = −10,000.00).**
COGS Actual for the same period is 115,628.72 (Row 24, Column E). A literal
`(Revenue − COGS) / Revenue × 100` here computes (−10,000.00 − 115,628.72) /
−10,000.00 × 100 = **+1,256.3%** — a large *positive* "margin" for a period
where Revenue was actually negative and real costs were incurred, produced
only because two negative numbers divided out to a positive result. This is
exactly the misleading outcome the formula doc warns about, so it must
**not** be calculated at all. Expected: *"Gross Margin cannot be calculated:
Revenue is negative (-$10,000.00). financial_data_2026.csv, Row 23,
Column E."* (This mirrors the formula doc's own illustrative example almost
exactly — deliberately.)

---

## 5. Period-over-Period (PoP) Growth

**Formula:** `PoP Growth (%) = (Current − Previous) / |Previous| × 100`

**Normal case — Revenue, Jul 2025 vs Jun 2025** (adjacent months, `financial_data_2025.csv`)

| Period | Value | Citation |
| --- | --- | --- |
| Jun 2025 (previous) | 193,479.20 | Row 37, Column E |
| Jul 2025 (current) | 192,009.41 | Row 44, Column E |

- PoP Growth = (192,009.41 − 193,479.20) / \|193,479.20\| × 100 = **−0.8%**

**Edge case — previous period = 0 (Cost of Goods Sold, Oct 2025 vs Sep 2025).**
Sep 2025 Actual = 0.00 (Row 59, Column E); Oct 2025 Actual = 106,031.44
(Row 66, Column E). Expected: *"PoP Growth cannot be calculated because the
previous period value is 0. financial_data_2025.csv, Row 59, Column E."*

**Edge case — previous period negative (Payroll Expense, Apr 2025 vs Mar 2025).**
Mar 2025 Actual = −1,500.00 (Row 18, Column E); Apr 2025 Actual = 42,842.22
(Row 25, Column E).
PoP Growth = (42,842.22 − (−1,500.00)) / \|−1,500.00\| × 100 = **2,956.1%**.
Arithmetically correct, but meaningless without the required explanatory
note that the previous period's value was negative — the assistant must not
present 2,956.1% as an ordinary growth figure.

**Edge case — missing month inside a quarter (Marketing Expense, Q3 2025).**
Aug 2025 Actual is missing (Row 54, Column E blank); Jul 2025 (Row 47) and
Sep 2025 (Row 61) are present. A Q3 2025 quarterly PoP/variance figure for
Marketing Expense must not be computed — the assistant must identify Aug
2025 (financial_data_2025.csv, Row 54, Column E) as the specific missing
month, not just report "Q3 data incomplete."

**Edge case — missing month inside a year (Payroll Expense, FY2026).**
Nov 2026 Actual is missing (`financial_data_2026.csv`, Row 74, Column E). A
full-year 2026 aggregate for Payroll Expense must not be computed; Nov 2026
must be identified as the specific missing month.

**Not data-seeded — mismatched period length / non-adjacent periods.** The
formula doc also requires flagging when a user requests two periods of
different duration (e.g. a quarter vs. a full year) or two non-adjacent
periods of the same type (e.g. Q1 vs. Q3). This is a property of the
*requested comparison*, not the dataset, so no synthetic rows are seeded for
it — every clean pair of periods in this dataset can be used to verify the
assistant correctly rejects such a request (e.g. asking for Q1 2025 vs. FY2025).

---

## 6. Year-over-Year (YoY) Growth

**Formula:** `YoY Growth (%) = (Current Year Value − Same Period Prior Year Value) / |Same Period Prior Year Value| × 100`

**Normal case — Revenue, Jun 2026 vs Jun 2025**

| Period | Value | Citation |
| --- | --- | --- |
| Jun 2025 (prior year) | 193,479.20 | financial_data_2025.csv, Row 37, Column E |
| Jun 2026 (current) | 222,940.45 | financial_data_2026.csv, Row 37, Column E |

- YoY Growth = (222,940.45 − 193,479.20) / \|193,479.20\| × 100 = **15.2%**
- Both files must be cited, per Source Traceability Requirement 2.

**Division-by-zero and negative-prior-year-value logic.** YoY Growth uses
the identical formula shape as PoP Growth, just against a same-month
prior-year value instead of an adjacent-month value. No separate YoY-specific
zero/negative case is seeded in the dataset — the PoP Growth cases above
(Cost of Goods Sold Sep 2025 = 0, Payroll Expense Mar 2025 negative)
exercise the same shared arithmetic and edge-case branches, so a single
implementation of "growth vs. a reference period" can be validated once via
PoP and trusted for YoY. If the two are implemented as genuinely separate
code paths, add a dedicated YoY zero/negative case before sign-off.

---

## 7. Variance Contribution by Category

**Formula:** `Category Contribution (%) = Category Dollar Variance / Total Dollar Variance × 100`

**Normal case — Expense group, Jul 2025** (`financial_data_2025.csv`, Rows 46–50)

| Category | Actual | Budget | Dollar Variance | Contribution % |
| --- | --- | --- | --- | --- |
| Payroll Expense (Row 46) | 43,552.14 | 43,275.86 | +276.28 | 50.4% |
| Marketing Expense (Row 47) | 7,742.62 | 7,430.64 | +311.98 | 56.9% |
| Rent Expense (Row 48) | 6,019.50 | 6,000.00 | +19.50 | 3.6% |
| Utilities Expense (Row 49) | 2,325.64 | 2,239.90 | +85.74 | 15.6% |
| Other Expense (Row 50) | 1,400.21 | 1,545.57 | −145.36 | −26.5% |
| **Total** | | | **$548.14** | **100.0%** |

Contributions sum to 100.0% exactly here; small rounding drift (per the
formula doc's "approximately 100%" allowance) should be expected in general
since each percentage is rounded to 1 decimal place independently.

**Edge case — total variance = 0 (Expense group, 2026-07, Rows 46–50 of `financial_data_2026.csv`).**

| Category | Actual | Budget | Dollar Variance |
| --- | --- | --- | --- |
| Payroll Expense (Row 46) | 45,500.00 | 45,000.00 | +500.00 |
| Marketing Expense (Row 47) | 8,700.00 | 9,000.00 | −300.00 |
| Rent Expense (Row 48) | 6,200.00 | 6,200.00 | 0.00 |
| Utilities Expense (Row 49) | 1,950.00 | 2,100.00 | −150.00 |
| Other Expense (Row 50) | 1,450.00 | 1,500.00 | −50.00 |
| **Total** | | | **$0.00** |

These five values were hand-picked so the group's variances cancel exactly.
Expected: *"Contribution by category cannot be calculated because total
variance is zero. financial_data_2026.csv, Rows 46-50, Columns E-F."* No
individual category contribution should be computed or shown as 0%.

**Edge case — a category missing from the set (Payroll Expense, FY2026, or Marketing Expense, Q3 2025 — see Section 5).**
If a monthly/quarterly/yearly Variance Contribution calculation includes a
category with a missing Actual or Budget value in the aggregation window,
that category's contribution must not be shown as 0%. Expected: *"Category
contribution cannot be calculated for Payroll Expense because the required
value is missing."*

---

## 8. Edge-case coverage summary

| Rule (Financial_Calculation_Formulas.md) | Seeded in dataset? | Location |
| --- | --- | --- |
| Division by zero — Percentage Variance | Yes | Utilities Expense, 2025-05, Row 35 Col F |
| Division by zero — Gross Margin | Yes | Revenue, 2026-02, Row 9 Col E |
| Division by zero — PoP Growth | Yes | Cost of Goods Sold, 2025-09, Row 59 Col E |
| Division by zero — Variance Contribution | Yes | Expense group, 2026-07, Rows 46-50 |
| Division by zero — YoY Growth | Shared logic only (see Section 6) | — |
| Missing value — Actual | Yes (x3: isolated, quarter-internal, year-internal) | Rows 6, 54, 74 |
| Missing value — Budget | Yes | Utilities Expense, 2025-04, Row 28 Col F |
| Missing value — both fields | Yes | Other Expense, 2026-06, Row 43 |
| Non-numeric value | Yes (x2: text and symbol) | Rows 62 (2026), 84 (2025) |
| Negative result — Revenue (Gross Margin) | Yes | Revenue, 2026-04, Row 23 Col E |
| Negative result — Budget (Percentage Variance) | Yes | Marketing Expense, 2025-11, Row 75 Col F |
| Negative result — previous period (PoP Growth) | Yes | Payroll Expense, 2025-03, Row 18 Col E |
| Mismatched period length / non-adjacent periods (PoP/YoY) | Not data-seeded — request-shape check | Any clean period pair |

---

## 9. How to regenerate this document

If `generate_synthetic_data.py`'s constants (`RANDOM_SEED`, category
profiles, `COGS_TO_REVENUE_RATIO`, or `EDGE_CASES`) change, the "normal case"
numbers above will no longer match a fresh run:

1. Run `python3 data/scripts/generate_synthetic_data.py` from the repo root.
2. Re-pull the referenced clean rows (Section 3–7) from the new
   `data/raw/financial_data_2025.csv` / `financial_data_2026.csv`.
3. Recompute each formula and update the tables above.
4. The edge-case rows (Section 8) only change if `EDGE_CASES` itself is
   edited — they are independent of the random seed.
