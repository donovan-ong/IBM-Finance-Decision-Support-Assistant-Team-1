"""Financial calculation module for Actual-vs-plan Dollar and Percentage Variances."""


def calculate_dollar_variance(actual: float, budget: float) -> dict:
  """Calculates the dollar variance between actual and budget figures.

  Formula: Dollar Variance = Actual - Budget

  Args:
      actual (float): The actual financial figure.
      budget (float): The budgeted financial figure.

  Returns:
      dict: Contains the numerical variance and formatted string result ($X.XX).
  """
  dollar_variance = actual - budget
  return {
      "dollar_variance": round(dollar_variance, 2),
      "formatted_result": f"${dollar_variance:,.2f}",
  }



def calculate_percentage_variance(actual: float, budget: float) -> dict:
  """Calculates the percentage variance between actual and budget figures.

  Formula: Percentage Variance = ((Actual - Budget) / Budget) * 100

  Args:
      actual (float): The actual financial figure.
      budget (float): The budgeted financial figure.

  Returns:
      dict: Contains the numerical percentage variance and formatted percentage
      string (X.X%), or an error/note for edge cases.
  """
  # Edge Case Rule 1: Division by Zero Prevention
  if budget == 0:
    return {
        "error": (
            "Percentage variance cannot be calculated because the base value"
            " is zero."
        )
    }

  percentage_variance = ((actual - budget) / abs(budget)) * 100

  # Note rule for negative base values
  note = None
  if budget < 0:
    note = (
        "Note: Result reflects a change relative to a negative starting value."
    )

  rounded_pct = round(percentage_variance, 1)
  return {
      "percentage_variance": rounded_pct,
      "formatted_result": f"{rounded_pct}%",
      "note": note,
  }