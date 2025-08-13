from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from budget_plan.models import BudgetPlan

class BudgetPlanMixin:
    def get_budget_plan(self):
        if hasattr(self, '_budget_plan_cache') and self._budget_plan_cache:
            return self._budget_plan_cache

        budget_plan_id = self.kwargs.get("plan_id")
        if not budget_plan_id:
            raise NotFound("Budget plan ID not provided.")

        if self.request.user.role == 'admin':
            budget_plan = get_object_or_404(BudgetPlan, id=budget_plan_id)
        else:
            budget_plan = get_object_or_404(
                BudgetPlan,
                id=budget_plan_id,
                user=self.request.user
            )

        self._budget_plan_cache = budget_plan
        return budget_plan
