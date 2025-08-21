from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from utils.permissions import IsAdminOnly
from rest_framework import generics, status
from rest_framework.response import Response
from utils.permissions import IsAdminOrOwner
from .filter import BudgetItemFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import BudgetItem, BudgetPlan
from .serializers import BudgetItemSerializer
from utils.pagination import CustomPagination
from utils.mixins import BudgetPlanMixin

class BudgetItemSearchView(BudgetPlanMixin, generics.ListAPIView):
    serializer_class = BudgetItemSerializer
    permission_classes = [IsAdminOrOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        budget_plan = self.get_budget_plan()

        filter_data = self.request.data.get("filter", {})
        search = filter_data.get("search")
        category_filter = filter_data.get("category")
        ordering = filter_data.get("ordering")

        qs = BudgetItem.objects.filter(budget_plan=budget_plan)

        if search:
            qs = qs.filter(
                Q(tip__icontains=search) |
                Q(category__name__icontains=search)
            )

        if category_filter:
            qs = qs.filter(category_id=category_filter)

        ordering_map = {
            "category": "category__name",
            "amount": "max_allowed_amount",
            "tip": "tip",
            "month": "budget_plan__month",
            "year": "budget_plan__year",
        }

        if ordering:
            clean_ordering = ordering.lstrip('-')
            ordering_field = ordering_map.get(clean_ordering)
            if ordering_field:
                if ordering.startswith('-'):
                    ordering_field = f"-{ordering_field}"
                qs = qs.order_by(ordering_field)

        return qs

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class BudgetItemCreateView(BudgetPlanMixin, generics.CreateAPIView):
    serializer_class = BudgetItemSerializer
    permission_classes = [IsAdminOrOwner]

    def create(self, request, *args, **kwargs):
        budget_plan = self.get_budget_plan()  # from your mixin
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(
            data=request.data,
            many=is_many,
            context={'bulk': is_many, 'budget_plan': budget_plan, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, budget_plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, budget_plan):
        serializer.save(budget_plan=budget_plan)


class BudgetItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetItemSerializer
    permission_classes = [IsAdminOrOwner]

    def get_queryset(self):
        return BudgetItem.objects.filter(
            budget_plan_id=self.kwargs["plan_id"]
        )

    def perform_update(self, serializer):
        serializer.save(budget_plan_id=self.kwargs["plan_id"])

class AdminBudgetItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BudgetItem.objects.all()
    serializer_class = BudgetItemSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BudgetItemFilter
    search_fields = ['category__name', 'budget_plan__month', 'budget_plan__year']
    ordering_fields = ['max_allowed_amount', 'budget_plan__month', 'budget_plan__year']
    ordering = ['-budget_plan__year', '-budget_plan__month']