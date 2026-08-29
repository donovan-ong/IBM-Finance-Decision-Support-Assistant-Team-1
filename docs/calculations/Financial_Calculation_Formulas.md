# FINANCIAL CALCULATION FORMULAS

 Development & Testing Reference  
 
**Project:** IBM-AI-Powered Finance Decision Support Assistant — Team A

**Document created by:** BA – Raghdah Al-Gahdari

**Status:** Active reference — update here first, then reflect in code and test cases

**Last Update:** 29 August 2026

This file defines exactly how each financial metric is calculated in the assistant. The development team should use these definitions when building and validating calculations if a formula needs to change, it should be updated here first, then reflected in the code and test cases.

## Data Source Structure

The dataset should contain records for each financial category and month. Each yearly file should contain the monthly records for that year. The monthly data may be used directly for monthly calculations or aggregated to support quarterly and yearly analysis. A quarter consists of three consecutive months, while a year consists of twelve consecutive months. The exact column structure and naming conventions are development and implementation decisions and are therefore out of scope for this document. 

Every figure used in a calculation must be traceable to its source. The AI Assistant must provide traceability by identifying the source file, relevant period, column, and row from which each figure used in the calculation was obtained. Where a calculation uses aggregated data, the AI Assistant must identify the underlying months, rows, and columns used to derive the quarterly or yearly value. If a required value cannot be found in the ingested data, the AI Assistant must clearly state that the value is missing. It must not substitute, estimate, or assume a value that is not present in the source data. 

## Calculation Definitions

1. **Dollar Variance**

Dollar Variance = Actual Value − Budget Value

**Inputs needed:** Actual Value and Budget Value (both numeric and expressed in the applicable currency), retrieved for the same financial category and selected period. The selected period may be a month, quarter, or year. For quarterly or yearly calculations, the values must be derived by aggregating the relevant monthly data for the selected category and period.

**Output format:** Currency, 2 decimal places (e.g. $15,200.00).

**Note:**

- Both values must be present don't assume 0 if one is missing.

- A negative result is valid (it just means the actual came in under budget), so don't hide the sign.

- State the source file, and the exact row and column each value was read from, so the result is fully traceable.

- For quarterly or yearly calculations, the AI Assistant must identify the underlying monthly records used to derive the Actual and Budget values.

2. **Percentage Variance**

Percentage Variance = (Actual Value − Budget Value) / |Budget Value| × 100

**Inputs needed:** Actual Value and Budget Value, from the same financial category and selected period as above. The selected period may be a month, quarter, or year. For quarterly or yearly calculations, the values must be derived by aggregating the relevant monthly data for the selected category and period.

**Output format:** Percentage, 1 decimal place (e.g. 12.5%).

**Note:**

- If Budget Value is 0, this can't be calculated. Return a message like: "Percentage variance cannot be calculated because the base value is zero." Don't return NaN or an error code.

- If Budget Value is negative, the assistant must add a short explanatory note clarifying that the result reflects a change relative to a negative starting value, so the percentage is not misread as movement from a positive base.

- State the source file, and the exact row and column each value was read from, so the result is fully traceable.

- For quarterly or yearly calculations, the AI Assistant must identify the underlying monthly records used to derive the Actual and Budget values.

3. **Gross Margin**

Gross Margin (%) = (Revenue − Cost of Goods Sold) / Revenue × 100

**Inputs needed:** Revenue and Cost of Goods Sold (COGS), from the same selected period. The selected period may be a month, quarter, or year. For quarterly or yearly calculations, Revenue and COGS must be derived by aggregating the relevant monthly data before applying the formula.

**Output format:** Percentage, 1 decimal place (e.g. 14.6%).

**Note:**

- If Revenue is 0, return: "Gross margin cannot be calculated because revenue is zero.".

- If Revenue is negative (e.g. from major refunds or reversals), do not perform the calculation, a negative Revenue in the denominator would produce a misleading positive percentage instead of reflecting an actual loss. Flag this as an invalid input and explain why (e.g. "Gross Margin cannot be calculated: Revenue is negative (-$10,000). financial_data2026.csv, Row 12, Column C.").

- Margin can be negative if COGS is higher than Revenue — that's a valid result, don't suppress it.

- State the source file, and the exact row and column each value was read from, so the result is fully traceable.

- For quarterly or yearly calculations, the AI Assistant must identify the months included in the calculation.

4. **Period-over-Period (PoP) Growth**

PoP Growth (%) = (Current Period Value − Previous Period Value) / |Previous Period Value| × 100

**Inputs needed:** Current Period Value and Previous Period Value, from the same financial category and matching period type. The comparison may be month-to-month, quarter-to-quarter, or year-to-year. For quarterly calculations, each quarter must be derived by aggregating its three underlying monthly records. For yearly calculations, each year must be derived by aggregating its twelve underlying monthly records.

**Output format:** Percentage, 1 decimal place

**Note:**

- If the previous period value is 0, return an explanatory message rather than dividing by zero.

- The two periods being compared should be adjacent (e.g. Q1 to Q2). If they're not, this should be flagged for the user to confirm rather than calculated silently

- The two periods being compared must be of the same duration/type (e.g., quarter vs. quarter, month vs. month, year vs. year). If the durations differ (e.g., a full year vs. a single quarter), the assistant must not perform the calculation. Instead, it must ask the user to select two periods of matching length.

- If the previous period value is negative, the assistant must add a short explanatory note clarifying that the result reflects a change relative to a negative starting value.

- State the source file, exact row, and column where each value was read from, including both files when the comparison spans two years, so the result is fully traceable

- For quarterly or yearly calculations, the AI Assistant must identify the months included in each period used in the calculation.

5. **Year-over-Year (YoY) Growth**

YoY Growth (%) = (Current Year Value − Same Period Prior Year Value) / |Same Period Prior Year Value| × 100

**Inputs needed:** Current Period Value and the corresponding same period in the prior year, from the same financial category and matching period type. The comparison may be month-to-month, quarter-to-quarter, or full-year-to-full-year. For quarterly calculations, each quarter must be derived by aggregating its three underlying monthly records. For yearly calculations, each year must be derived by aggregating its twelve underlying monthly records.

**Output format:** Percentage, 1 decimal place

**Note:**

- If the same period prior year value is 0, return an explanatory message rather than dividing by zero

- The periods being compared need to match (e.g. Q2 this year vs Q2 last year, not Q2 vs Q3). A mismatch should trigger a clarification prompt instead of just calculating anyway.

- If the prior year period value is negative, the assistant must add a short explanatory note clarifying that the result reflects a change relative to a negative starting value

- State the source file, exact row, and column where each value was read from, including the matching period from each year when the comparison spans two yearly files, so the result is fully traceable.

- For quarterly or yearly calculations, the AI Assistant must identify the months included in each period used in the calculation.

6. **Variance Contribution by Category**

Category Contribution (%) = Category Dollar Variance / Total Dollar Variance × 100

**Inputs needed:** Dollar Variance for each category (from Formula 1) and the Total Dollar Variance across all categories within the same category set and selected period. The selected period may be a month, quarter, or year. For quarterly or yearly calculations, the Actual and Budget values used to derive the Dollar Variance for each category must be aggregated from the relevant monthly data before calculating the contribution.

**Output format:** Percentage, 1 decimal place. Contributions should total approximately 100%, allowing for small rounding differences.

**Note:**

- If a category is missing the required value, do not treat it as 0%. Return a message identifying the category, such as: "Category contribution cannot be calculated for [Category] because the required value is missing."

- If total Dollar Variance is 0, return: "Contribution by category cannot be calculated because total variance is zero."

- State the source file, exact row, and column where each category's Dollar Variance was read from, so the result is fully traceable.

- For quarterly or yearly calculations, the AI Assistant must identify the months included in the calculation for each category.

## Edge Case Handling Rules

1) **Division by Zero**

- If the value being divided by is 0, do not perform the calculation.

- The assistant must identify the specific value that is zero and provide its source file, exact row, and column.

- The assistant must not display NaN, Infinity, undefined, or a raw error code.

> **Example:** "Percentage variance cannot be calculated because Budget Value is 0. The value was found in financial_data2026.csv, Row 12, Column E."

2) **Missing Values**

- If a required value is missing, null, or unavailable, the calculation must not be performed.

- The AI Assistant must clearly identify the missing value.

- Where the expected source location is known, the AI Assistant must identify the source file, row, and column associated with the missing value.

- The AI Assistant must not assume that a missing value is 0.

- For quarterly or yearly calculations, the AI Assistant must identify the monthly data required to perform the calculation. If a required value for any month is missing, the AI Assistant must identify the missing value and, where known, specify its corresponding source file, row, and column.

**Example:** Percentage variance cannot be calculated because Actual Value is missing from financial_data2026.csv, Row 8, Column C.

3) **Non-Numeric Values**

- If a value that should be numeric contains text, symbols, or another non-numeric value, the calculation must not be performed.

- The assistant must identify the invalid value and its source file, row, and column.

- The assistant must return a clear message explaining that a numeric value is required.

> **Example:** Calculation cannot be completed because Actual Value must be a numeric value. The invalid value was found in financial_data2026.csv, Row 12, Column D.

4) **Negative Results**

- Negative results are valid where allowed by the calculation and must not be hidden, converted to zero, or removed.

- The assistant must display the negative sign in the result.

- Where appropriate, the assistant should explain what the negative result represents.

**Example**: Dollar Variance = -$4,200.00, meaning Actual Value was $4,200 below Budget Value.

## Source Traceability Requirements

1. Every value used in a calculation must be traceable to its source file, exact row, and column, where applicable.

2. If values are taken from different yearly files, the assistant must identify the source location for each value.

3. The assistant must not present a calculated result if the source of the required input values cannot be verified.

4. For quarterly or yearly calculations, the AI Assistant must identify the months included in the calculation and the corresponding source file, row, and column for the Actual and Budget values used to derive the result.

## General Formatting Rules

- Percentages to 1 decimal place, currency to 2 decimal places. Round only for display keep full precision during the actual calculation.

- Currency format: $#,###.## unless the client asks for something else.
