from .models import PasswordResetOTP
import random
from users.models import User
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "Passwords do not match."})

        if old_password == new_password:
            raise serializers.ValidationError({"new_password": "New password must be different from old password."})

        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return {"message": "Password changed successfully."}


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.get(email=email)
        otp = str(random.randint(100000, 999999))

        # حفظ OTP في قاعدة البيانات
        PasswordResetOTP.objects.create(user=user, otp=otp)

        # إرسال الإيميل
        send_mail(
            subject="Your Password Reset OTP",
            message=f"Your OTP code is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )

        return {"message": "A verification code has been sent to your email."}


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).last()
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registered.")

        if not otp_obj:
            raise serializers.ValidationError("Invalid verification code.")
        if otp_obj.is_expired():
            raise serializers.ValidationError("Expired verification code.")

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        email = attrs['email']
        otp = attrs['otp']

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).last()
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registered.")

        if not otp_obj:
            raise serializers.ValidationError("Invalid verification code.")
        if otp_obj.is_expired():
            raise serializers.ValidationError("Expired verification code")

        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return {"message": "Password changed successfully."}
