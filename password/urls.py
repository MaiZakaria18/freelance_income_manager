from django.urls import path
from .views import (
    ForgotPasswordView,
    VerifyOTPView,
    ResetPasswordView,
    ChangePasswordView
)

urlpatterns = [
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('password/forgot/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('password/verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('password/reset/', ResetPasswordView.as_view(), name='reset_password'),
]