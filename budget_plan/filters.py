import django_filters
from budget_plan.models import BudgetPlan

class BudgetPlanFilter(django_filters.FilterSet):
    month = django_filters.NumberFilter()
    year = django_filters.NumberFilter()
    user = django_filters.NumberFilter(field_name='user__id')

    class Meta:
        model = BudgetPlan
        fields = ['month', 'year', 'user']
