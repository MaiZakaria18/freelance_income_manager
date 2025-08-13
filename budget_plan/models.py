from django.db import models
from django.conf import settings

class BudgetPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Total income in {self.month} is {self.total_income}"

