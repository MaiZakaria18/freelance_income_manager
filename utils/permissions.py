from rest_framework.permissions import BasePermission
from users.exceptions import CustomPermissionDenied


class IsAdminOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_superuser or user.role == 'admin')


class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.role == 'admin':
            return True

        if hasattr(obj, 'user') and obj.user == user:
            return True

        if hasattr(obj, 'budget_plan') and getattr(obj.budget_plan, 'user', None) == user:
            return True

        raise CustomPermissionDenied("Resources Not Found.")

