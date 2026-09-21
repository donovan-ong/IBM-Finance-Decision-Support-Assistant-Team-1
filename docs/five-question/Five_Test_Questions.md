# Five Test Questions

Used for both development testing and the Sprint demo. Same 5 questions, same expected answers.

Business scenario: mid-sized clothing retail business, Melbourne (per Business Rules, POL-DATA-002, Section 3).

| # | Question | Files compared | Calculation type | Needs Business Rule? | Needs Market Context? |
|---|---|---|---|---|---|
| 1 | What is the dollar variance between actual and budgeted revenue for our Melbourne clothing store in Q2 2026? | financial_data_2026.csv (Q2 actual vs budget, Revenue) | Dollar Variance | No | No |
| 2 | How did our gross margin change from Q1 2026 to Q2 2026? | financial_data_2026.csv (Q1 vs Q2) | Gross Margin + Period-over-Period Growth | No | No |
| 3 | What is our year-over-year revenue growth from 2025 to 2026? | financial_data_2025.csv vs financial_data_2026.csv | Year-over-Year Growth | Yes | Yes |
| 4 | Which expense category (e.g. Rent, Payroll, Marketing) contributed most to the variance in operating costs in Q2 2026? | financial_data_2026.csv (Q2 actual vs budget, by category) | Variance Contribution by Category | Yes | No |
| 5 | What is the percentage variance in COGS versus budget for Q2 2026, and what market factors may have contributed to this variance? | financial_data_2026.csv (Q2 COGS row) | Percentage Variance | Yes | Yes |
