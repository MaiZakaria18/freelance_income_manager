from decimal import Decimal
from django.db.models import Sum
from expenses.models import Expenses
from budget_item.models import BudgetItem

def get_budget_overview(budget_plan):
    total_budget = BudgetItem.objects.filter(budget_plan=budget_plan).aggregate(
        total=Sum('max_allowed_amount')
    )['total'] or Decimal('0.00')

    total_expenses = Expenses.objects.filter(
        budget_plan=budget_plan,
        category__isnull=False
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')

    remaining = total_budget - total_expenses
    warnings = []

    if remaining <= 0:
        status = "Over Budget"
        warnings.append("⚠️ You have exceeded your total budget!")
    elif remaining <= (total_budget * Decimal('0.2')):
        status = "Close to Limit"
        warnings.append(f"⚠️ You are close to your total budget limit. Only {remaining} left.")
    else:
        status = "Within Budget"

    return {
        "total_budget": total_budget,
        "total_expenses": total_expenses,
        "remaining": remaining,
        "status": status,
        "warnings": warnings
    }
