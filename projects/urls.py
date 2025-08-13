from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectCreateView, ProjectSearchView, ProjectDetailView, AdminProjectViewSet

router = DefaultRouter()
router.register(r'admin', AdminProjectViewSet, basename='admin-projects')

urlpatterns = [
    path('', ProjectCreateView.as_view(), name='project-create'),
    path('search/', ProjectSearchView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('', include(router.urls)),
]
