from datetime import date
from rest_framework import serializers
from .models import  BudgetPlan

class BudgetPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetPlan
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def validate(self, attrs):
        user = self.context['request'].user
        month = attrs.get('month')
        year = attrs.get('year')

        # Prevent creating budget for past months
        today = date.today()
        if year < today.year or (year == today.year and month < today.month):
            raise serializers.ValidationError(
                "You cannot create a budget for a past month."
            )

        existing_plans = BudgetPlan.objects.filter(user=user, month=month, year=year)
        if self.instance:
            existing_plans = existing_plans.exclude(pk=self.instance.pk)
        if existing_plans.exists():
            raise serializers.ValidationError(
                "You already created a budget for this month and year."
            )

        return attrs