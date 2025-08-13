from rest_framework.exceptions import PermissionDenied

class CustomPermissionDenied(PermissionDenied):
    default_detail = "You are not authorized to access this content."
    default_code = "permission_denied"
