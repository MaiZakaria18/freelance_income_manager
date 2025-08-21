from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404

from users.models import User
from projects.models import Project
from budget_plan.models import BudgetPlan
from budget_item.models import BudgetItem

from projects.serializers import ProjectSerializer
from budget_plan.serializers import BudgetPlanSerializer
from budget_item.serializers import BudgetItemSerializer

from projects.filters import ProjectFilter
from budget_plan.filters import BudgetPlanFilter
from budget_item.filter import BudgetItemFilter

from utils.pagination import CustomPagination


class AdminUserFullDataView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        project_qs = Project.objects.select_related('user').filter(user=user)
        project_qs = ProjectFilter(request.GET, queryset=project_qs).qs

        plan_qs = BudgetPlan.objects.select_related('user').filter(user=user)
        plan_qs = BudgetPlanFilter(request.GET, queryset=plan_qs).qs

        item_qs = BudgetItem.objects.select_related('budget_plan', 'budget_plan__user').filter(budget_plan__user=user)
        item_qs = BudgetItemFilter(request.GET, queryset=item_qs).qs

        # pagination
        paginator = CustomPagination()
        paginated_projects = paginator.paginate_queryset(project_qs, request)
        paginated_plans = paginator.paginate_queryset(plan_qs, request)
        paginated_items = paginator.paginate_queryset(item_qs, request)

        return Response({
            "user_id": user_id,
            "projects": ProjectSerializer(paginated_projects, many=True).data,
            "budget_plans": BudgetPlanSerializer(paginated_plans, many=True).data,
            "budget_items": BudgetItemSerializer(paginated_items, many=True).data
        })
