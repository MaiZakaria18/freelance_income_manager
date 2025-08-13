import django_filters
from budget_item.models import BudgetItem

class BudgetItemFilter(django_filters.FilterSet):
    budget_plan = django_filters.NumberFilter(field_name='budget_plan__id')
    category = django_filters.NumberFilter(field_name='category__id')
    max_allowed_amount_min = django_filters.NumberFilter(field_name='max_allowed_amount', lookup_expr='gte')
    max_allowed_amount_max = django_filters.NumberFilter(field_name='max_allowed_amount', lookup_expr='lte')

    class Meta:
        model = BudgetItem
        fields = ['budget_plan', 'category', 'max_allowed_amount_min', 'max_allowed_amount_max']
