import django_filters
from .models import Expenses

class ExpenseFilter(django_filters.FilterSet):
    transaction_date = django_filters.DateFromToRangeFilter()
    amount = django_filters.RangeFilter()
    tip = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='category__category__id')  # FK relations

    class Meta:
        model = Expenses
        fields = ['transaction_date', 'amount', 'tip', 'category']
