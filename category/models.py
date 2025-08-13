from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'],
                name='unique_category_per_user'
            )
        ]

    def __str__(self):
        return self.name
