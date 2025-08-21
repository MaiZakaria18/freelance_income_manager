from django.urls import path
from .views import AdminUserFullDataView

urlpatterns = [
    path('admin/user-data/<int:user_id>/', AdminUserFullDataView.as_view(), name='admin-user-data')
]
