from rest_framework import serializers
from category.serializers import CategorySerializer
from category.models import Category
from .models import BudgetItem
from core.budget_item_validator import BudgetItemValidator

class BudgetItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = BudgetItem
        fields = ['id', 'budget_plan', 'category', 'category_id', 'max_allowed_amount', 'tip']
        extra_kwargs = {'budget_plan': {'required': False}}

    def validate(self, attrs):
        budget_plan = attrs.get('budget_plan') or self.context.get('budget_plan') or getattr(self.instance,
                                                                                             'budget_plan', None)
        category = attrs.get('category') or getattr(self.instance, 'category', None)
        amount = attrs.get('max_allowed_amount') or getattr(self.instance, 'max_allowed_amount', None)

        if not all([budget_plan, category]) or amount is None:
            return attrs

        BudgetItemValidator.validate_unique_category(budget_plan, category, self.instance)
        BudgetItemValidator.validate_budget_limit(budget_plan, amount, self.instance)

        return attrs
