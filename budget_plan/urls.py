from django.urls import path, include
from .views import BudgetPlanCreateView, BudgetPlanDetailView, BudgetPlanSearchView, AdminBudgetPlanViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admin', AdminBudgetPlanViewSet, basename='admin-budget-plan')
urlpatterns = [
    path('', BudgetPlanCreateView.as_view(), name='budget-plan-list-create'),
    path('search/', BudgetPlanSearchView.as_view(), name='project-list'),
    path('<int:pk>/', BudgetPlanDetailView.as_view(), name='budget-plan-detail'),
    path('', include(router.urls)),

]
