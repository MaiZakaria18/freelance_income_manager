from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from .filter import ExpenseFilter
from django.db.models import Q
from .models import Expenses
from .serializers import ExpenseSerializer
from rest_framework import status
from core.permissions import IsAdminOrOwner, IsAdminOnly
from rest_framework import generics
from rest_framework.response import Response
from core.pagination import CustomPagination
from core.budget_summary import get_budget_overview
from core.uncategorized_expenses import get_uncategorized_expenses
from core.category_summary import get_category_summary
from core.mixins import BudgetPlanMixin

class ExpenseSearchView(BudgetPlanMixin, generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrOwner]
    pagination_class = CustomPagination

    def get_queryset(self):
        budget_plan = self.get_budget_plan()

        filter_data = self.request.data.get("filter", {})
        search = filter_data.get("search")
        category_filter = filter_data.get("category")
        ordering = filter_data.get("ordering")

        qs = Expenses.objects.filter(budget_plan=budget_plan)

        if search:
            qs = qs.filter(
                Q(tip__icontains=search) |
                Q(category__category__name__icontains=search)
            )

        if category_filter:
            qs = qs.filter(category_id=category_filter)

        ordering_map = {
            "category": "category__category__name",
            "amount": "amount",
            "tip": "tip",
            "transaction_date": "transaction_date",
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

class ExpenseCreateView(BudgetPlanMixin, generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrOwner]

    def create(self, request, *args, **kwargs):
        budget_plan = self.get_budget_plan()

        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'budget_plan': budget_plan}
        )
        serializer.is_valid(raise_exception=True)
        expense = serializer.save(budget_plan=budget_plan)

        return Response(
            {
                "message": "Expense created successfully",
                "expenses": ExpenseSerializer(expense, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )

class ExpenseRetrieveView(generics.RetrieveAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrOwner]  # لو عندك صلاحيات خاصة

    def get_expense(self):
        plan_id = self.kwargs.get('plan_id')
        expense_id = self.kwargs.get('pk')
        try:
            return Expenses.objects.get(
                id=expense_id,
                budget_plan_id=plan_id,
                budget_plan__user=self.request.user
            )
        except Expenses.DoesNotExist:
            raise NotFound("Expense not found.")

    def get_object(self):
        return self.get_expense()


class ExpenseUpdateView(BudgetPlanMixin, generics.UpdateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrOwner]
    lookup_field = "pk"

    def get_object(self):
        return self.get_expense()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        expense = self.get_object()
        serializer = self.get_serializer(expense, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        updated_expense = serializer.instance
        warnings = self.get_warnings(updated_expense)

        return Response({
            "message": "Expense updated successfully",
            "warnings": warnings,
            "expenses": serializer.data
        })


class ExpenseDestroyView(BudgetPlanMixin, generics.DestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOrOwner]
    lookup_field = "pk"

    def get_object(self):
        return self.get_expense()

    def get_expense(self):
        pass


class BudgetPlanFullSummaryView(BudgetPlanMixin, generics.GenericAPIView):
    permission_classes = [IsAdminOrOwner]

    def post(self, request, *args, **kwargs):
        budget_plan = self.get_budget_plan()

        pagination_data = request.data.get("pagination", {})
        filter_data = request.data.get("filter", {})

        page_number = pagination_data.get("page", 1)
        page_size = pagination_data.get("page_size", 10)
        search = filter_data.get("search")

        budget_overview = get_budget_overview(budget_plan)
        category_summary = get_category_summary(budget_plan)
        uncategorized_data = get_uncategorized_expenses(
            budget_plan, search, page_number, page_size
        )

        return Response({
            "pagination": uncategorized_data["pagination"],
            "budget_plan": {
                "id": budget_plan.id,
                "month": budget_plan.month,
                "year": budget_plan.year
            },
            **budget_overview,
            "total_expense_uncategorized": float(uncategorized_data["total_uncategorized"]),
            "categories": category_summary,
            "uncategorized_expenses": uncategorized_data["expenses"]
        })


class ExpenseAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ['tip', 'category__category__name']
    ordering_fields = ['transaction_date', 'amount']
    ordering = ['-transaction_date']