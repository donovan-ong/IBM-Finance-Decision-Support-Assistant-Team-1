# FD_FIN_OVERVIEW — MDX/Rule Backup

Cube: FD_FIN_OVERVIEW (rebuilt version, dimensions: FD_Account, Period, FD_Version, FD_Measure — no Year dimension)
Backup date: 2026-09-18

All views below are hand-verified against source data unless noted otherwise. Re-verify after any further cube changes.

---

## TM1 Rule: Dollar Variance (cube-level rule on FD_FIN_OVERVIEW)

```
['Variance $'] = N: DB('FD_FIN_OVERVIEW', !FD_Account, !Period, 'Actual', !FD_Measure)
                 - DB('FD_FIN_OVERVIEW', !FD_Account, !Period, 'Budget', !FD_Measure);

FEEDERS;
['Actual'] => ['Variance $'];
```

---

## View: DASH_Variance_Overview

```mdx
WITH
   MEMBER [FD_Version].[FD_Version].[Actual $] AS
      [FD_Version].[FD_Version].[Actual],
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[Budget $] AS
      [FD_Version].[FD_Version].[Budget],
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[Variance $ (Fmt)] AS
      [FD_Version].[FD_Version].[Variance $],
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[Variance %] AS
      IIF(
         [FD_Version].[FD_Version].[Budget] = 0,
         0,
         ([FD_Version].[FD_Version].[Actual] - [FD_Version].[FD_Version].[Budget])
         / ABS([FD_Version].[FD_Version].[Budget]) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [FD_Version].[FD_Version].[Actual $],
      [FD_Version].[FD_Version].[Budget $],
      [FD_Version].[FD_Version].[Variance $ (Fmt)],
      [FD_Version].[FD_Version].[Variance %]
   } ON 0,
   {
      [FD_Account].[FD_Account].MEMBERS
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [Period].[Period].[Year101],
   [FD_Measure].[FD_Measure].[Amount])
```

---

## View: DASH_Gross_Margin

```mdx
WITH
   MEMBER [FD_Version].[FD_Version].[Gross Margin % (Actual)] AS
      IIF(
         ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual]) = 0, 0,
         (
            ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual])
            - ([FD_Account].[FD_Account].[Cost of Goods Sold], [FD_Version].[FD_Version].[Actual])
         )
         / ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual]) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Version].[FD_Version].[Gross Margin % (Budget)] AS
      IIF(
         ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Budget]) = 0, 0,
         (
            ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Budget])
            - ([FD_Account].[FD_Account].[Cost of Goods Sold], [FD_Version].[FD_Version].[Budget])
         )
         / ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Budget]) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [FD_Version].[FD_Version].[Gross Margin % (Actual)],
      [FD_Version].[FD_Version].[Gross Margin % (Budget)]
   } ON 0,
   {
      [FD_Measure].[FD_Measure].[Amount]
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [Period].[Period].[Year101]
)
```

---

## View: DASH_PoP_Growth

Note: `.LastChild` (used in the year-boundary branch) was a newly introduced function at time of writing — verify the boundary case specifically before trusting fully.

```mdx
WITH MEMBER [FD_Version].[FD_Version].[PoP Growth %] AS
   IIF(
      [Period].[Period].CurrentMember.PrevMember.Parent IS [Period].[Period].CurrentMember.Parent,

      IIF(
         ([Period].[Period].CurrentMember.PrevMember, [FD_Version].[FD_Version].[Actual]) = 0,
         0,
         (
            ([Period].[Period].CurrentMember, [FD_Version].[FD_Version].[Actual])
            - ([Period].[Period].CurrentMember.PrevMember, [FD_Version].[FD_Version].[Actual])
         )
         / ABS(([Period].[Period].CurrentMember.PrevMember, [FD_Version].[FD_Version].[Actual])) * 100
      ),

      IIF(
         ([Period].[Period].CurrentMember.Parent.PrevMember.LastChild, [FD_Version].[FD_Version].[Actual]) = 0,
         0,
         (
            ([Period].[Period].CurrentMember, [FD_Version].[FD_Version].[Actual])
            - ([Period].[Period].CurrentMember.Parent.PrevMember.LastChild, [FD_Version].[FD_Version].[Actual])
         )
         / ABS(([Period].[Period].CurrentMember.Parent.PrevMember.LastChild, [FD_Version].[FD_Version].[Actual])) * 100
      )
   ),
   FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [FD_Version].[FD_Version].[Actual],
      [FD_Version].[FD_Version].[PoP Growth %]
   } ON 0,
   {
      [FD_Account].[FD_Account].MEMBERS
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [Period].[Period].[Year102],
   [FD_Measure].[FD_Measure].[Amount]
)
```

---

## View: DASH_YoY_Growth

Simplified from the pre-rebuild version — no longer needs a second Year dimension navigated in lockstep.

```mdx
WITH MEMBER [FD_Version].[FD_Version].[YoY Growth %] AS
   IIF(
      (
         Cousin([Period].[Period].CurrentMember, [Period].[Period].CurrentMember.Parent.PrevMember),
         [FD_Version].[FD_Version].[Actual]
      ) = 0,
      0,
      (
         ([Period].[Period].CurrentMember, [FD_Version].[FD_Version].[Actual])
         -
         (
            Cousin([Period].[Period].CurrentMember, [Period].[Period].CurrentMember.Parent.PrevMember),
            [FD_Version].[FD_Version].[Actual]
         )
      )
      /
      ABS((
         Cousin([Period].[Period].CurrentMember, [Period].[Period].CurrentMember.Parent.PrevMember),
         [FD_Version].[FD_Version].[Actual]
      )) * 100
   ),
   FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [FD_Version].[FD_Version].[Actual],
      [FD_Version].[FD_Version].[YoY Growth %]
   } ON 0,
   {
      [FD_Account].[FD_Account].MEMBERS
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [Period].[Period].[Year201],
   [FD_Measure].[FD_Measure].[Amount]
)
```

---

## View: DASH_Variance_Contribution

```mdx
WITH MEMBER [FD_Version].[FD_Version].[Variance Contribution %] AS
   IIF(
      ([FD_Account].[FD_Account].[Operating Expenses], [FD_Version].[FD_Version].[Variance $]) = 0,
      0,
      ([FD_Account].[FD_Account].CurrentMember, [FD_Version].[FD_Version].[Variance $])
      / ([FD_Account].[FD_Account].[Operating Expenses], [FD_Version].[FD_Version].[Variance $]) * 100
   ),
   FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [FD_Version].[FD_Version].[Variance $],
      [FD_Version].[FD_Version].[Variance Contribution %]
   } ON 0,
   {
      [FD_Account].[FD_Account].[Operating Expenses].Children
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [Period].[Period].[Year101],
   [FD_Measure].[FD_Measure].[Amount]
)
```

---

## View: DASH_KPI_Summary (Wireframe 1 tiles)

Current tile set: Actual FY2025, Budget FY2025, Variance FY2025, Variance % FY2025, Gross Profit FY2025 (replaces the removed Forecast Revenue tile), PoP Growth Jul vs Jun 2025, YoY Growth Jun 2025 vs Jun 2026. Gross Margin Jun 2025 member definition retained below but not in the SELECT list — add back in if needed.

```mdx
WITH
   MEMBER [FD_Version].[FD_Version].[Actual FY2025] AS
      ([Period].[Period].[Year1], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual]),
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[Budget FY2025] AS
      ([Period].[Period].[Year1], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Budget]),
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[Variance FY2025] AS
      [FD_Version].[FD_Version].[Actual FY2025] - [FD_Version].[FD_Version].[Budget FY2025],
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[Variance % FY2025] AS
      IIF(
         [FD_Version].[FD_Version].[Budget FY2025] = 0, 0,
         [FD_Version].[FD_Version].[Variance FY2025] / ABS([FD_Version].[FD_Version].[Budget FY2025]) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Version].[FD_Version].[Gross Profit FY2025] AS
      (
         ([Period].[Period].[Year1], [FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual])
         - ([Period].[Period].[Year1], [FD_Account].[FD_Account].[Cost of Goods Sold], [FD_Version].[FD_Version].[Actual])
      ),
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[Gross Margin Jun 2025] AS
      IIF(
         ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual]) = 0, 0,
         (
            ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual])
            - ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Cost of Goods Sold], [FD_Version].[FD_Version].[Actual])
         )
         / ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual]) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Version].[FD_Version].[PoP Growth Jul vs Jun 2025] AS
      IIF(
         ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual]) = 0, 0,
         (
            ([Period].[Period].[Year107], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual])
            - ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual])
         )
         / ABS(([Period].[Period].[Year106], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual])) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Version].[FD_Version].[YoY Growth Jun 2025 vs Jun 2026] AS
      IIF(
         ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual]) = 0, 0,
         (
            ([Period].[Period].[Year206], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual])
            - ([Period].[Period].[Year106], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual])
         )
         / ABS(([Period].[Period].[Year106], [FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Actual])) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [FD_Version].[FD_Version].[Actual FY2025],
      [FD_Version].[FD_Version].[Budget FY2025],
      [FD_Version].[FD_Version].[Variance FY2025],
      [FD_Version].[FD_Version].[Variance % FY2025],
      [FD_Version].[FD_Version].[Gross Profit FY2025],
      [FD_Version].[FD_Version].[PoP Growth Jul vs Jun 2025],
      [FD_Version].[FD_Version].[YoY Growth Jun 2025 vs Jun 2026]
   } ON 0,
   {
      [FD_Measure].[FD_Measure].[Amount]
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
```

---

## View: DASH_Monthly_Trend (static MDX reference)

Note: the live Book widget uses a drag-and-drop Exploration with synchronized Period/FD_Account selector tiles (built directly in the UI, not as saved MDX) so that selector-driven year-switching works. The query below is the last static MDX version, useful as a fallback or for re-deriving the Exploration's structure, but is not what the Book currently runs.

```mdx
WITH
   MEMBER [FD_Version].[FD_Version].[Actual Value] AS [FD_Version].[FD_Version].[Actual], FORMAT_STRING = '$#,##0.00;-$#,##0.00'
   MEMBER [FD_Version].[FD_Version].[Budget Value] AS [FD_Version].[FD_Version].[Budget], FORMAT_STRING = '$#,##0.00;-$#,##0.00'

SELECT
   {
      [FD_Version].[FD_Version].[Actual Value],
      [FD_Version].[FD_Version].[Budget Value]
   } ON 0,
   {
      [Period].[Period].[Year101], [Period].[Period].[Year102], [Period].[Period].[Year103],
      [Period].[Period].[Year104], [Period].[Period].[Year105], [Period].[Period].[Year106],
      [Period].[Period].[Year107], [Period].[Period].[Year108], [Period].[Period].[Year109],
      [Period].[Period].[Year110], [Period].[Period].[Year111], [Period].[Period].[Year112]
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [FD_Account].[FD_Account].[Total Account],
   [FD_Measure].[FD_Measure].[Amount]
)
```

---

## View: DASH_Variance_Analysis (Wireframe 2)

```mdx
WITH
   MEMBER [FD_Version].[FD_Version].[Actual $] AS [FD_Version].[FD_Version].[Actual], FORMAT_STRING = '$#,##0.00;-$#,##0.00'
   MEMBER [FD_Version].[FD_Version].[Budget $] AS [FD_Version].[FD_Version].[Budget], FORMAT_STRING = '$#,##0.00;-$#,##0.00'
   MEMBER [FD_Version].[FD_Version].[Variance $ (Fmt)] AS [FD_Version].[FD_Version].[Variance $], FORMAT_STRING = '$#,##0.00;-$#,##0.00'
   MEMBER [FD_Version].[FD_Version].[Variance %] AS
      IIF([FD_Version].[FD_Version].[Budget] = 0, 0,
         ([FD_Version].[FD_Version].[Actual] - [FD_Version].[FD_Version].[Budget]) / ABS([FD_Version].[FD_Version].[Budget]) * 100
      ), FORMAT_STRING = '#,##0.0"%"'
   MEMBER [FD_Version].[FD_Version].[Variance Contribution %] AS
      IIF(
         ([FD_Account].[FD_Account].[Operating Expenses], [FD_Version].[FD_Version].[Variance $]) = 0, 0,
         ([FD_Account].[FD_Account].CurrentMember, [FD_Version].[FD_Version].[Variance $])
         / ([FD_Account].[FD_Account].[Operating Expenses], [FD_Version].[FD_Version].[Variance $]) * 100
      ), FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [FD_Version].[FD_Version].[Budget $],
      [FD_Version].[FD_Version].[Actual $],
      [FD_Version].[FD_Version].[Variance $ (Fmt)],
      [FD_Version].[FD_Version].[Variance %],
      [FD_Version].[FD_Version].[Variance Contribution %]
   } ON 0,
   {
      [FD_Account].[FD_Account].[Operating Expenses].Children
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [Period].[Period].[Year1],
   [FD_Measure].[FD_Measure].[Amount]
)
```

---

## View: DASH_Budget_Summary (Wireframe 3, Budget block)

Note: calculated members here are defined on FD_Account (a row dimension) rather than FD_Version, unlike every other view in this backup — this pattern was newly introduced and less thoroughly tested. Re-verify before further reliance.

```mdx
WITH
   MEMBER [FD_Account].[FD_Account].[Gross Profit] AS
      [FD_Account].[FD_Account].[Revenue] - [FD_Account].[FD_Account].[Cost of Goods Sold],
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Account].[FD_Account].[Gross Margin %] AS
      IIF(
         [FD_Account].[FD_Account].[Revenue] = 0, 0,
         [FD_Account].[FD_Account].[Gross Profit] / [FD_Account].[FD_Account].[Revenue] * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Account].[FD_Account].[Total Operating Expenses] AS
      [FD_Account].[FD_Account].[Operating Expenses],
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Account].[FD_Account].[Operating Result] AS
      [FD_Account].[FD_Account].[Total Account],
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

SELECT
   {
      [Period].[Period].[Year1],
      [Period].[Period].[Year1Q1],
      [Period].[Period].[Year1Q2],
      [Period].[Period].[Year1Q3],
      [Period].[Period].[Year1Q4]
   } ON 0,
   {
      [FD_Account].[FD_Account].[Total Account],
      [FD_Account].[FD_Account].[Revenue],
      [FD_Account].[FD_Account].[Cost of Goods Sold],
      [FD_Account].[FD_Account].[Gross Profit],
      [FD_Account].[FD_Account].[Gross Margin %],
      [FD_Account].[FD_Account].[Payroll Expense],
      [FD_Account].[FD_Account].[Marketing Expense],
      [FD_Account].[FD_Account].[Rent Expense],
      [FD_Account].[FD_Account].[Utilities Expense],
      [FD_Account].[FD_Account].[Other Expense],
      [FD_Account].[FD_Account].[Total Operating Expenses],
      [FD_Account].[FD_Account].[Operating Result]
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
WHERE (
   [FD_Version].[FD_Version].[Budget],
   [FD_Measure].[FD_Measure].[Amount]
)
```

---

## View: DASH_Performance_Calculations (Wireframe 3, Performance block)

Note: % Variance to Budget below is the corrected version (inlined from Variance $ and Budget directly) — an earlier draft referenced a non-existent [Variance %] member and caused a recursion error. YoY Growth % will show 0.00/blank for any column within Year1, since there is no prior year to compare against inside a single year's columns — expected, not a bug.

```mdx
WITH
   MEMBER [FD_Version].[FD_Version].[Actual Revenue] AS
      ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual]),
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[$ Variance to Budget] AS
      ([FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Variance $]),
      FORMAT_STRING = '$#,##0.00;-$#,##0.00'

   MEMBER [FD_Version].[FD_Version].[% Variance to Budget] AS
      IIF(
         ([FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Budget]) = 0, 0,
         ([FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Variance $])
         / ABS(([FD_Account].[FD_Account].[Total Account], [FD_Version].[FD_Version].[Budget])) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Version].[FD_Version].[Gross Margin %] AS
      IIF(
         ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual]) = 0, 0,
         (
            ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual])
            - ([FD_Account].[FD_Account].[Cost of Goods Sold], [FD_Version].[FD_Version].[Actual])
         )
         / ([FD_Account].[FD_Account].[Revenue], [FD_Version].[FD_Version].[Actual]) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Version].[FD_Version].[PoP Growth %] AS
      IIF(
         [Period].[Period].CurrentMember.PrevMember.Parent IS [Period].[Period].CurrentMember.Parent,
         IIF(
            ([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember.PrevMember, [FD_Version].[FD_Version].[Actual]) = 0, 0,
            (
               ([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember, [FD_Version].[FD_Version].[Actual])
               - ([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember.PrevMember, [FD_Version].[FD_Version].[Actual])
            )
            / ABS(([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember.PrevMember, [FD_Version].[FD_Version].[Actual])) * 100
         ),
         IIF(
            ([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember.Parent.PrevMember.LastChild, [FD_Version].[FD_Version].[Actual]) = 0, 0,
            (
               ([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember, [FD_Version].[FD_Version].[Actual])
               - ([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember.Parent.PrevMember.LastChild, [FD_Version].[FD_Version].[Actual])
            )
            / ABS(([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember.Parent.PrevMember.LastChild, [FD_Version].[FD_Version].[Actual])) * 100
         )
      ),
      FORMAT_STRING = '#,##0.0"%"'

   MEMBER [FD_Version].[FD_Version].[YoY Growth %] AS
      IIF(
         ([FD_Account].[FD_Account].[Total Account], Cousin([Period].[Period].CurrentMember, [Period].[Period].CurrentMember.Parent.PrevMember), [FD_Version].[FD_Version].[Actual]) = 0, 0,
         (
            ([FD_Account].[FD_Account].[Total Account], [Period].[Period].CurrentMember, [FD_Version].[FD_Version].[Actual])
            - ([FD_Account].[FD_Account].[Total Account], Cousin([Period].[Period].CurrentMember, [Period].[Period].CurrentMember.Parent.PrevMember), [FD_Version].[FD_Version].[Actual])
         )
         / ABS(([FD_Account].[FD_Account].[Total Account], Cousin([Period].[Period].CurrentMember, [Period].[Period].CurrentMember.Parent.PrevMember), [FD_Version].[FD_Version].[Actual])) * 100
      ),
      FORMAT_STRING = '#,##0.0"%"'

SELECT
   {
      [Period].[Period].[Year1],
      [Period].[Period].[Year1Q1],
      [Period].[Period].[Year1Q2],
      [Period].[Period].[Year1Q3],
      [Period].[Period].[Year1Q4]
   } ON 0,
   {
      [FD_Version].[FD_Version].[Actual Revenue],
      [FD_Version].[FD_Version].[$ Variance to Budget],
      [FD_Version].[FD_Version].[% Variance to Budget],
      [FD_Version].[FD_Version].[Gross Margin %],
      [FD_Version].[FD_Version].[PoP Growth %],
      [FD_Version].[FD_Version].[YoY Growth %]
   } ON 1
FROM
   [FD_FIN_OVERVIEW]
```

---

## Known open items (for reference, not part of the MDX itself)

- Forecast data does not exist in source files or cube (FD_Version has no Forecast element). Forecast Revenue and Variance-to-Forecast fields were removed from Wireframes 1 and 3 by BA decision (Monika), replaced with a stacked bar chart on Wireframe 3 and a Gross Profit tile on Wireframe 1.
- Month labels on the live Monthly Trend chart show raw element names (Year101, etc.) rather than calendar months — the selector-synchronized Exploration approach dropped the aliasing used in the static MDX version above.
- PoP Growth % at the Year1 (full-year) column level returns 0.0%, since a full year has no meaningful adjacent prior period at that consolidation level — expected, not an error.
- DASH_Budget_Summary uses calculated members on FD_Account rather than FD_Version, a pattern used only once in this project — worth extra scrutiny if reused elsewhere.
- Cube was rebuilt mid-project (Mike) to drop the standalone Year dimension, resolving prior selector-synchronization failures. All MDX above reflects the rebuilt, four-dimension structure (FD_Account, Period, FD_Version, FD_Measure).
