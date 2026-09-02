"""Generate synthetic finance CSVs into data/raw for development and testing.

Writes three files, matching the CSV/SQL Data Structure Specification:
  - data/raw/financial_data_2025.csv
  - data/raw/financial_data_2026.csv
  - data/raw/categories.csv   (seed data for the SQL Categories lookup table)

DISTRIBUTION MODEL (how the "clean" numbers are generated)
------------------------------------------------------------
Revenue and each Expense category follow their own compounding month-over-month
growth trend, which becomes that category's Budget_Value. Actual_Value is the
same trend value with random Gaussian noise applied on top (mean 0, category-
specific std dev), so Actual realistically over/undershoots Budget every month.
Cost of Goods Sold has no independent trend - it is generated as a fixed
percentage of Revenue's budget for the same period (COGS_TO_REVENUE_RATIO), so
Gross Margin lands in a realistic range instead of drifting randomly.

All of this is controlled by named constants below:
  - RANDOM_SEED            reroll the noise by changing this
  - REVENUE_PROFILE / EXPENSE_PROFILES   starting level, growth rate, and
    noise (volatility) per category - edit these to reshape the trend
  - COGS_TO_REVENUE_RATIO / COGS_NOISE_STD_PCT   COGS behaviour specifically

EDGE CASES (how the "dirty" cells are generated)
------------------------------------------------------------
The Financial Calculation Formulas reference requires the assistant to handle
missing values, division-by-zero, non-numeric values, and negative values -
each with a source file/row/column citation. The base trend above never
produces those on its own, so EDGE_CASES below is an explicit, hand-picked
list of (year, period, category) cells that get overwritten after the clean
data is generated, one entry per scenario the assistant must be able to
handle. Nothing is seeded probabilistically: every dirty cell is deliberate
and documented with a `reason`, so the dataset stays reviewable and each
scenario's exact location is known in advance (see print_edge_case_summary).
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configuration - change these to reshape the generated dataset.
# ---------------------------------------------------------------------------

RANDOM_SEED = 42  # Fixed so the generated CSVs are reproducible and diff-friendly in git.

YEARS = [2025, 2026]
MONTHS = list(range(1, 13))

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "data" / "raw"

# Fixed row order used for every month's block of categories. This matches the
# sample rows in the CSV/SQL Data Structure Specification exactly, which keeps
# the physical CSV row numbers (used below for edge-case citations) predictable.
CATEGORY_ORDER = [
    "Revenue",
    "Cost of Goods Sold",
    "Payroll Expense",
    "Marketing Expense",
    "Rent Expense",
    "Utilities Expense",
    "Other Expense",
]

CATEGORY_GROUP = {
    "Revenue": "Revenue",
    "Cost of Goods Sold": "COGS",
    "Payroll Expense": "Expense",
    "Marketing Expense": "Expense",
    "Rent Expense": "Expense",
    "Utilities Expense": "Expense",
    "Other Expense": "Expense",
}


@dataclass(frozen=True)
class CategoryProfile:
    """Defines how one category's monthly Budget/Actual values are generated."""

    name: str
    starting_budget: float       # Budget value in the first period (2025-01)
    monthly_growth_rate: float   # Compounding month-over-month growth applied to the trend
    noise_std_pct: float         # Std dev of Actual's random deviation from Budget, as a fraction (0.05 = 5%)


# Revenue: the growth trend everything else (COGS, Gross Margin) is measured against.
REVENUE_PROFILE = CategoryProfile(
    name="Revenue", starting_budget=175000.00, monthly_growth_rate=0.015, noise_std_pct=0.03
)

# Expense categories, ordered to match CATEGORY_ORDER. Each has its own starting
# level, growth rate, and volatility - e.g. Rent is flat and stable (fixed
# lease), Marketing and Other are volatile (discretionary spend).
EXPENSE_PROFILES = [
    CategoryProfile(name="Payroll Expense", starting_budget=42000.00, monthly_growth_rate=0.005, noise_std_pct=0.01),
    CategoryProfile(name="Marketing Expense", starting_budget=7000.00, monthly_growth_rate=0.010, noise_std_pct=0.12),
    CategoryProfile(name="Rent Expense", starting_budget=6000.00, monthly_growth_rate=0.000, noise_std_pct=0.005),
    CategoryProfile(name="Utilities Expense", starting_budget=2200.00, monthly_growth_rate=0.003, noise_std_pct=0.08),
    CategoryProfile(name="Other Expense", starting_budget=1500.00, monthly_growth_rate=0.005, noise_std_pct=0.15),
]

# Cost of Goods Sold is derived from Revenue's budget rather than having its own
# trend, so Gross Margin stays in a realistic band instead of drifting randomly.
COGS_TO_REVENUE_RATIO = 0.52
COGS_NOISE_STD_PCT = 0.02


# ---------------------------------------------------------------------------
# Edge cases - deliberately seeded "dirty" cells, applied after the clean data
# is generated. See the module docstring for why these are hand-picked rather
# than randomly injected.
# ---------------------------------------------------------------------------


class _Keep:
    """Sentinel meaning 'leave this field as generated'. Distinct from None,
    which means 'blank/missing' when written to the seeded cell."""

    def __repr__(self) -> str:
        return "KEEP"


KEEP = _Keep()


@dataclass(frozen=True)
class EdgeCase:
    """One deliberately seeded cell (or pair of cells) in the synthetic data.

    `actual` and `budget` are one of:
      - KEEP        leave the generated value untouched (default)
      - None        blank the cell (missing value)
      - float       an explicit numeric value (e.g. 0.0, or a negative number)
      - str         a non-numeric value written verbatim (e.g. "N/A")
    """

    year: int
    period: str
    category: str
    reason: str
    actual: Any = KEEP
    budget: Any = KEEP


EDGE_CASES: list[EdgeCase] = [
    # --- Missing values (Edge Case Handling Rule 2) --------------------------
    EdgeCase(
        2025, "2025-01", "Rent Expense",
        reason="Missing Actual value - canonical example from the CSV/SQL Data Structure Specification (Sec. 4).",
        actual=None,
    ),
    EdgeCase(
        2025, "2025-04", "Utilities Expense",
        reason="Missing Budget value - covers the missing-value case on the Budget field, not just Actual.",
        budget=None,
    ),
    EdgeCase(
        2025, "2025-08", "Marketing Expense",
        reason="Missing Actual value inside Q3 2025 (Jul-Sep) - tests that quarterly aggregation flags the "
               "missing month instead of silently excluding it.",
        actual=None,
    ),
    EdgeCase(
        2026, "2026-11", "Payroll Expense",
        reason="Missing Actual value inside FY2026 - tests that yearly aggregation flags the missing month.",
        actual=None,
    ),
    EdgeCase(
        2026, "2026-06", "Other Expense",
        reason="Both Actual and Budget missing for the same cell - full-blackout case.",
        actual=None, budget=None,
    ),

    # --- Division by zero (Edge Case Handling Rule 1) -------------------------
    EdgeCase(
        2025, "2025-05", "Utilities Expense",
        reason="Budget = 0 (explicit, not missing) - Percentage Variance division-by-zero case.",
        budget=0.00,
    ),
    EdgeCase(
        2026, "2026-02", "Revenue",
        reason="Revenue Actual = 0 (explicit) - Gross Margin division-by-zero case.",
        actual=0.00,
    ),
    EdgeCase(
        2025, "2025-09", "Cost of Goods Sold",
        reason="Actual = 0 - makes the previous-period value 0 for PoP Growth (Oct 2025 vs Sep 2025).",
        actual=0.00,
    ),
    # Five hand-picked 2026-07 Expense rows whose dollar variances sum to
    # exactly $0.00 (+500 -300 +0 -150 -50 = 0) - Variance Contribution by
    # Category division-by-zero case (total variance across the group = 0).
    EdgeCase(2026, "2026-07", "Payroll Expense", reason="Zero-sum-variance period (see comment above).", actual=45500.00, budget=45000.00),
    EdgeCase(2026, "2026-07", "Marketing Expense", reason="Zero-sum-variance period (see comment above).", actual=8700.00, budget=9000.00),
    EdgeCase(2026, "2026-07", "Rent Expense", reason="Zero-sum-variance period (see comment above).", actual=6200.00, budget=6200.00),
    EdgeCase(2026, "2026-07", "Utilities Expense", reason="Zero-sum-variance period (see comment above).", actual=1950.00, budget=2100.00),
    EdgeCase(2026, "2026-07", "Other Expense", reason="Zero-sum-variance period (see comment above).", actual=1450.00, budget=1500.00),

    # --- Negative values (Edge Case Handling Rule 4) --------------------------
    EdgeCase(
        2026, "2026-04", "Revenue",
        reason="Revenue Actual is negative (e.g. a large refund/reversal) - Gross Margin must flag negative "
               "Revenue as an invalid input instead of computing a misleading percentage.",
        actual=-10000.00,
    ),
    EdgeCase(
        2025, "2025-11", "Marketing Expense",
        reason="Budget is negative - Percentage Variance must add the negative-starting-value explanatory note.",
        budget=-2000.00,
    ),
    EdgeCase(
        2025, "2025-03", "Payroll Expense",
        reason="Actual is negative - makes the previous-period value negative for PoP Growth (Apr 2025 vs Mar 2025).",
        actual=-1500.00,
    ),

    # --- Non-numeric values (Edge Case Handling Rule 3) -----------------------
    EdgeCase(
        2026, "2026-09", "Rent Expense",
        reason="Actual contains non-numeric text ('N/A') instead of a number.",
        actual="N/A",
    ),
    EdgeCase(
        2025, "2025-12", "Utilities Expense",
        reason="Budget contains a non-numeric symbol string ('#REF!') - a second, distinct non-numeric case.",
        budget="#REF!",
    ),
]

# CSV column letters for Actual_Value / Budget_Value, used only for the
# human-readable edge-case summary printed at the end of a run.
COLUMN_LETTER = {"actual": "E", "budget": "F"}


# ---------------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------------


def _apply_noise(trend_value: float, noise_std_pct: float) -> float:
    """Return trend_value perturbed by Gaussian noise (mean 0, std noise_std_pct as a fraction of trend_value)."""
    noise_fraction = random.gauss(0.0, noise_std_pct)
    return round(trend_value * (1 + noise_fraction), 2)


def generate_base_rows() -> dict[tuple[int, str, str], dict[str, Any]]:
    """Build the "clean" dataset: one Actual/Budget pair per (year, period, category), before any edge cases."""
    rows: dict[tuple[int, str, str], dict[str, Any]] = {}

    month_index = 0  # 0-based count of months since 2025-01, drives the compounding growth trend
    for year in YEARS:
        for month in MONTHS:
            period = f"{year}-{month:02d}"

            revenue_budget = round(REVENUE_PROFILE.starting_budget * (1 + REVENUE_PROFILE.monthly_growth_rate) ** month_index, 2)
            revenue_actual = _apply_noise(revenue_budget, REVENUE_PROFILE.noise_std_pct)
            rows[(year, period, "Revenue")] = {"actual": revenue_actual, "budget": revenue_budget}

            cogs_budget = round(revenue_budget * COGS_TO_REVENUE_RATIO, 2)
            cogs_actual = _apply_noise(cogs_budget, COGS_NOISE_STD_PCT)
            rows[(year, period, "Cost of Goods Sold")] = {"actual": cogs_actual, "budget": cogs_budget}

            for profile in EXPENSE_PROFILES:
                budget = round(profile.starting_budget * (1 + profile.monthly_growth_rate) ** month_index, 2)
                actual = _apply_noise(budget, profile.noise_std_pct)
                rows[(year, period, profile.name)] = {"actual": actual, "budget": budget}

            month_index += 1

    return rows


def apply_edge_cases(rows: dict[tuple[int, str, str], dict[str, Any]], edge_cases: list[EdgeCase]) -> None:
    """Overwrite specific generated cells with the deliberately seeded edge-case values.

    Applied after generate_base_rows() so every edge case has a known, predictable
    Row/Column location once written to CSV (see print_edge_case_summary).
    """
    for edge_case in edge_cases:
        cell = rows[(edge_case.year, edge_case.period, edge_case.category)]
        if edge_case.actual is not KEEP:
            cell["actual"] = edge_case.actual
        if edge_case.budget is not KEEP:
            cell["budget"] = edge_case.budget


# ---------------------------------------------------------------------------
# CSV writing
# ---------------------------------------------------------------------------


def _format_cell(value: Any) -> str:
    """Render a cell for the CSV: blank for missing (None), 2dp for numeric, verbatim for seeded non-numeric text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return f"{value:.2f}"


def write_financial_data_csv(rows: dict[tuple[int, str, str], dict[str, Any]], year: int, output_dir: Path) -> None:
    """Write one financial_data_<year>.csv file, in the fixed Year/Period/Category row order."""
    file_path = output_dir / f"financial_data_{year}.csv"
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Year", "Period", "Category", "Category_Group", "Actual_Value", "Budget_Value"])

        for month in MONTHS:
            period = f"{year}-{month:02d}"
            for category_name in CATEGORY_ORDER:
                cell = rows[(year, period, category_name)]
                writer.writerow(
                    [
                        year,
                        period,
                        category_name,
                        CATEGORY_GROUP[category_name],
                        _format_cell(cell["actual"]),
                        _format_cell(cell["budget"]),
                    ]
                )


def write_categories_csv(output_dir: Path) -> None:
    """Write categories.csv: seed data for the SQL Categories lookup table."""
    file_path = output_dir / "categories.csv"
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["category_name", "category_group", "display_order"])
        for display_order, category_name in enumerate(CATEGORY_ORDER, start=1):
            writer.writerow([category_name, CATEGORY_GROUP[category_name], display_order])


# ---------------------------------------------------------------------------
# Review helper: print exactly where each edge case landed
# ---------------------------------------------------------------------------


def _row_number(period: str, category: str) -> int:
    """Physical CSV row number (header = row 1) for a (period, category) cell, matching the fixed write order."""
    month = int(period.split("-")[1])
    category_index = CATEGORY_ORDER.index(category)
    return 2 + (month - 1) * len(CATEGORY_ORDER) + category_index


def print_edge_case_summary(edge_cases: list[EdgeCase]) -> None:
    """Print a Row/Column citation for every seeded edge case, in the same style the assistant must use."""
    print("Seeded edge cases:")
    for edge_case in edge_cases:
        row = _row_number(edge_case.period, edge_case.category)
        file_name = f"financial_data_{edge_case.year}.csv"
        for field_name, value in (("actual", edge_case.actual), ("budget", edge_case.budget)):
            if value is KEEP:
                continue
            column = COLUMN_LETTER[field_name]
            print(f"  {file_name}, Row {row}, Column {column} ({edge_case.category} {field_name}) = {value!r} - {edge_case.reason}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    random.seed(RANDOM_SEED)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = generate_base_rows()
    apply_edge_cases(rows, EDGE_CASES)

    for year in YEARS:
        write_financial_data_csv(rows, year, OUTPUT_DIR)
    write_categories_csv(OUTPUT_DIR)

    print_edge_case_summary(EDGE_CASES)
    print(f"\nWrote {len(YEARS)} yearly file(s) and categories.csv to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
