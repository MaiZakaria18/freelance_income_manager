from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('utils.urls')),
    path('api/users/', include('users.urls')),
    path('api/', include('password.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/budget-plan/', include('budget_plan.urls')),
    path('api/', include('category.urls')),
    path('api/', include('budget_item.urls')),
    path('api/', include('expenses.urls')),
    path('api/', include('tips.urls')),

]
