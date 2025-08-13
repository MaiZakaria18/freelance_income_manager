from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profession', 'location', 'avg_monthly_income', 'role')}),
    )

admin.site.register(User, CustomUserAdmin)
