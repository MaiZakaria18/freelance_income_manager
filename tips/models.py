from django.db import models
from django.conf import settings
from category.models import Category

class Tip(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tips')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tips')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 2)
        return 0

    def __str__(self):
        return f"Tip by {self.user.email} on {self.category.name}"

class TipRating(models.Model):
    tip = models.ForeignKey(Tip, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tip_ratings')
    value = models.PositiveSmallIntegerField()  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tip', 'user')  # يمنع اليوزر من التقييم أكثر من مرة

    def __str__(self):
        return f"{self.value} by {self.user.email} for Tip {self.tip.id}"
