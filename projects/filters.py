import django_filters
from .models import Project

class ProjectFilter(django_filters.FilterSet):
    payment_date_from = django_filters.DateFilter(field_name='payment_date', lookup_expr='gte')
    payment_date_to = django_filters.DateFilter(field_name='payment_date', lookup_expr='lte')
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')

    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=Project.STATUS_CHOICES,
        help_text=" pending, paid, overdue"
    )

    class Meta:
        model = Project
        fields = ['status', 'user', 'client_name']