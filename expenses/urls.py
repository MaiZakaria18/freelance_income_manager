from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ExpenseCreateView, ExpenseRetrieveView,
                    ExpenseSearchView,BudgetPlanFullSummaryView,
                    ExpenseUpdateView, ExpenseDestroyView, ExpenseAdminViewSet)

router = DefaultRouter()
router.register(r'admin/expenses', ExpenseAdminViewSet, basename='admin-expenses')

urlpatterns = [
    path('budget-plan/<int:plan_id>/expenses/', ExpenseCreateView.as_view(), name='expenses-create'),
    path('budget-plan/<int:plan_id>/expenses-search/', ExpenseSearchView.as_view(), name='expenses-list'),
    path('budget-plan/<int:plan_id>/expenses/<int:pk>/', ExpenseRetrieveView.as_view(), name='expenses-detail'),
    path('budget-plan/<int:plan_id>/expenses/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expenses-update'),
    path('budget-plan/<int:plan_id>/expenses/<int:pk>/delete/', ExpenseDestroyView.as_view(), name='expenses-delete'),
    path('budget-plan/<int:plan_id>/full-summary/', BudgetPlanFullSummaryView.as_view(), name='budget-plan-full-summary'),
    path('', include(router.urls)),

]
