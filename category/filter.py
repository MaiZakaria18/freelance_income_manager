import django_filters
from category.models import Category

class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    user = django_filters.NumberFilter(field_name='user__id')


    class Meta:
        model = Category
        fields = ['name', 'user']
