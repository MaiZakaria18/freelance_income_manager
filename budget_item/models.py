from django.db import models
from budget_plan.models import BudgetPlan
from category.models import Category

class BudgetItem(models.Model):
    budget_plan = models.ForeignKey(BudgetPlan, on_delete=models.CASCADE, related_name="items")
    max_allowed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tip = models.TextField(null=True, blank=True)



    def __str__(self):
        return f"{self.category}: {self.max_allowed_amount}"

