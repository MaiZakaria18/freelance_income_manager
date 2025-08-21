from rest_framework import serializers

class BudgetItemValidator:
    @staticmethod
    def validate_unique_category(budget_plan, category, instance=None):
        from budget_item.models import BudgetItem
        qs = BudgetItem.objects.filter(budget_plan=budget_plan, category=category)
        if instance:
            qs = qs.exclude(id=instance.id)
        if qs.exists():
            raise serializers.ValidationError("This category already exists in the budget plan.")

    @staticmethod
    def validate_budget_limit(budget_plan, amount, instance=None):
        from budget_item.models import BudgetItem
        total_amount = sum(
            item.max_allowed_amount
            for item in BudgetItem.objects.filter(budget_plan=budget_plan).exclude(id=getattr(instance, 'id', None))
        )
        if total_amount + amount > budget_plan.total_income:
            raise serializers.ValidationError("Budget exceeded the plan's total income.")
