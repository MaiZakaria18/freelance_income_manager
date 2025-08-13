from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CustomLoginView, AdminUserViewSet

router = DefaultRouter()
router.register(r'admin', AdminUserViewSet, basename='admin-users')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
