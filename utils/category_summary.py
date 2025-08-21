# services/category_summary.py
from decimal import Decimal
from django.db.models import Sum
from expenses.models import Expenses
from budget_item.models import BudgetItem

def get_category_summary(budget_plan):
    categories_summary = []
    budget_items = BudgetItem.objects.filter(budget_plan=budget_plan).select_related('category')

    for item in budget_items:
        spent = Expenses.objects.filter(
            budget_plan=budget_plan,
            category=item
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        cat_remaining = item.max_allowed_amount - spent
        cat_status = "Within Limit"
        cat_warnings = []

        if cat_remaining <= 0:
            cat_status = "Over Limit"
            cat_warnings.append(f"⚠️ You exceeded the budget for category {item.category.name}.")
        elif cat_remaining <= (item.max_allowed_amount * Decimal('0.2')):
            cat_status = "Close to Limit"
            cat_warnings.append(
                f"⚠️ You are close to the limit for category {item.category.name}. Only {cat_remaining} left."
            )

        categories_summary.append({
            "category": {
                "id": item.category.id,
                "name": item.category.name
            },
            "allocated_budget": float(item.max_allowed_amount),
            "spent": float(spent),
            "remaining": float(cat_remaining),
            "status": cat_status,
            "warnings": cat_warnings
        })

    return categories_summary
