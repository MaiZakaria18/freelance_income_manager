from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    email = models.EmailField(unique=True)
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    avg_monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    role = models.CharField(max_length=20, default='freelancer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'profession', 'location']


    def __str__(self):
        return self.email