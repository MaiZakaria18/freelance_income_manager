from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import CategorySearchView, CategoryUpdateView, CategoryDeleteView, CategoryCreateView, CategoryAdminViewSet

router = DefaultRouter()
router.register(r'admin', CategoryAdminViewSet, basename='admin-category')



urlpatterns = [
    path('categories/search/', CategorySearchView.as_view(), name='initial-category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('', include(router.urls)),

]