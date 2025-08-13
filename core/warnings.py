from decimal import Decimal
from django.db.models import Sum
from expenses.models import Expenses

def get_expense_warnings(expense):
    warnings = []

    if expense.category is None:
        warnings.append("This expense is not part of any budget and will not be counted in total expenses.")
        return warnings

    budget_item = expense.category
    max_allowed = budget_item.max_allowed_amount

    total_spent = Expenses.objects.filter(
        budget_plan=expense.budget_plan,
        category=budget_item
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    remaining = max_allowed - total_spent

    if remaining <= 0:
        warnings.append(f"⚠️ You have exceeded the budget for '{budget_item.category.name}'!")
    elif remaining <= (max_allowed * Decimal('0.2')):
        warnings.append(f"⚠️ You are close to reaching the budget limit for '{budget_item.category.name}'. Only {remaining} left.")

    return warnings
