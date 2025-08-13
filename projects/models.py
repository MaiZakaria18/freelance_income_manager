from django.db import models
from django.conf import settings
     

class Project(models.Model):
    STATUS_CHOICES=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue')
    ]
    
    project_name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    project_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    class Meta:
        unique_together = ('user', 'project_name')


    def __str__(self):
        return f"{self.client_name} paid {self.project_amount}"