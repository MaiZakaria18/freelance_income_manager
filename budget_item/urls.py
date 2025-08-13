from django.urls import path, include
from .views import BudgetItemCreateView, BudgetItemRetrieveUpdateDestroyView, BudgetItemSearchView, AdminBudgetItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admin', AdminBudgetItemViewSet, basename='admin-items')

urlpatterns = [

    path('budget-plan/<int:plan_id>/items/', BudgetItemCreateView.as_view(), name='budget-item-create'),
    path('budget-plan/<int:plan_id>/items-search/', BudgetItemSearchView.as_view(), name='budget-item-list'),
    path('budget-plan/<int:plan_id>/items/<int:pk>/', BudgetItemRetrieveUpdateDestroyView.as_view(), name='budget-item-detail'),
    path('', include(router.urls)),

]
