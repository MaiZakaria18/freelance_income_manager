from rest_framework import serializers
from expenses.models import Expenses
from utils.expenses_validation import ExpenseBudgetValidationMixin
from budget_item.models import BudgetItem

class ExpenseSerializer(serializers.ModelSerializer, ExpenseBudgetValidationMixin):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BudgetItem.objects.all(),
        source='category',
        required=False,
        allow_null=True,
        write_only=True
    )

    class Meta:
        model = Expenses
        fields = ['id', 'category_id', 'amount', 'tip', 'transaction_date']

    def validate(self, data):
        budget_plan = self.context.get('budget_plan')
        if not budget_plan:
            raise serializers.ValidationError("Budget plan context is missing.")

        category = data.get('category')
        tip = data.get('tip')
        amount = data.get('amount')

        if category is None and (tip is None or tip.strip() == ''):
            raise serializers.ValidationError("Either category must be set or tip must be provided.")

        self.validate_expense_budget(category, budget_plan, amount)

        return data
