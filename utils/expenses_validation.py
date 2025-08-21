from decimal import Decimal
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from expenses.models import Expenses


class ExpenseBudgetValidationMixin:
    """
    Mixin to validate expense amounts against category and budget plan limits.
    """

    def validate_expense_budget(self, category, budget_plan, amount):
        """
        Raises ValidationError if category or total plan budget is exceeded.
        """
        # Validate category budget
        if category:
            total_spent_on_category = (
                Expenses.objects.filter(category=category)
                .aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
            )
            if total_spent_on_category + amount > category.max_allowed_amount:
                raise ValidationError(
                    f"Category budget exceeded for {category.category.name}."
                )

        # Validate total plan budget
        total_spent_on_plan = (
            Expenses.objects.filter(budget_plan=budget_plan)
            .aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        )
        if total_spent_on_plan + amount > budget_plan.total_income:
            raise ValidationError(
                "Total budget for this plan has been exceeded."
            )
