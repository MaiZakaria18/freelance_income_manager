from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ObjectDoesNotExist):
            response.data['detail'] = "Resource not found"
        elif response.status_code == 404:
            response.data['detail'] = "Resource not found"
        elif response.status_code == 403:
            response.data['detail'] = "You do not have permission to perform this action"

    return response
