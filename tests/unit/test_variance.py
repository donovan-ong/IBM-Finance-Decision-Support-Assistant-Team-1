# Per-calculation-function unit tests (e.g. finance_assistant.calculations.variance).
"""Validates Dollar Variance and Percentage Variance against standard cases
and all required edge cases in isolation.
"""

from finance_assistant.calculations.variance import (
    calculate_dollar_variance,
    calculate_percentage_variance,
)


def test_dollar_variance_positive():
  # Standard positive variance (Actual > Budget)
  result = calculate_dollar_variance(actual=1500.0, budget=1200.0)
  assert result["dollar_variance"] == 300.0
  assert result["formatted_result"] == "$300.00"


def test_dollar_variance_negative():
  # Negative variance (Actual < Budget) - valid result, sign preserved
  result = calculate_dollar_variance(actual=900.0, budget=1200.0)
  assert result["dollar_variance"] == -300.0
  assert result["formatted_result"] == "$-300.00"


def test_percentage_variance_standard():
  # Standard percentage variance calculation
  result = calculate_percentage_variance(actual=1125.0, budget=1000.0)
  assert result["percentage_variance"] == 12.5
  assert result["formatted_result"] == "12.5%"


def test_percentage_variance_edge_case_zero_budget():
  # Edge Case 1: Division by zero when budget is 0
  result = calculate_percentage_variance(actual=500.0, budget=0.0)
  assert "error" in result
  assert (
      result["error"]
      == "Percentage variance cannot be calculated because the base value is zero."
  )


def test_percentage_variance_edge_case_negative_budget():
  # Edge Case 2: Negative base value handling (includes explanatory note)
  result = calculate_percentage_variance(actual=100.0, budget=-200.0)
  assert "percentage_variance" in result
  assert result["note"] is not None
  assert "negative starting value" in result["note"]
