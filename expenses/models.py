from django.db import models
from django.utils import timezone
from budget_plan.models import BudgetPlan
from budget_item.models import BudgetItem

class Expenses(models.Model):
    budget_plan = models.ForeignKey(BudgetPlan, on_delete=models.CASCADE)
    category = models.ForeignKey(BudgetItem,on_delete=models.SET_NULL, null=True, blank=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tip = models.TextField(null=True, blank=True)



    def __str__(self):
        return f"{self.category.name} - {self.amount} at {self.transaction_date}"
