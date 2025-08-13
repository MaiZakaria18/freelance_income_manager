from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import get_object_or_404
from core.permissions import IsAdminOrOwner
from core.pagination import CustomPagination
from django.db.models import Q
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from budget_plan.models import BudgetPlan
from budget_plan.serializers import BudgetPlanSerializer
from core.permissions import IsAdminOnly
from .filters import BudgetPlanFilter


class BudgetPlanCreateView(generics.CreateAPIView):

    serializer_class = BudgetPlanSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetPlanSearchView(generics.ListAPIView):
    serializer_class = BudgetPlanSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        filter_data = self.request.data.get("filter", {})
        search = filter_data.get("search")
        month_filter = filter_data.get("month")
        year_filter = filter_data.get("year")
        ordering = filter_data.get("ordering")

        qs = BudgetPlan.objects.all()
        if self.request.user.role != 'admin':
            qs = qs.filter(user=self.request.user)

        if search:
            qs = qs.filter(
                Q(month__icontains=search) |
                Q(year__icontains=search) |
                Q(user__email__icontains=search)
            )

        if month_filter:
            qs = qs.filter(month=month_filter)

        if year_filter:
            qs = qs.filter(year=year_filter)

        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BudgetPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetPlanSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_object(self):
        obj = get_object_or_404(BudgetPlan, pk=self.kwargs['pk'])

        if self.request.user != obj.user and self.request.user.role != 'admin':
            raise NotFound()

        return obj

class AdminBudgetPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BudgetPlan.objects.all()
    serializer_class = BudgetPlanSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BudgetPlanFilter
    search_fields = ['month', 'year', 'user__email']
    ordering_fields = ['month', 'year']
    ordering = ['-year', '-month']