from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import random
from datetime import timedelta

from django.utils import timezone
from django.core.mail import send_mail

from rest_framework import serializers
from django.conf import settings

from .models import User


class SignupSerializer(serializers.Serializer):

    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(required=False, allow_blank=True)
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default='customer',
        required=False
    )

    def validate_identifier(self, value):

        if "@" in value:

            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already registered")

        else:

            if not value.isdigit():
                raise serializers.ValidationError("Invalid phone number")

            if User.objects.filter(phone=value).exists():
                raise serializers.ValidationError("Phone already registered")

        return value

    def create(self, validated_data):

        identifier = validated_data['identifier'].strip().lower()
        password = validated_data['password']
        referral = validated_data.get('referral_code')
        role = validated_data.get('role', 'customer')

        otp = str(random.randint(100000, 999999))

        user = User(
            referral_code=referral,
            role=role,
            otp=otp,
            otp_created_at=timezone.now(),
            is_verified=False
        )

        if "@" in identifier:
            user.email = identifier
            user.username = identifier
        else:
            user.phone = identifier
            user.username = identifier

        user.set_password(password)
        user.save()

        return user


class VerifyOTPSerializer(serializers.Serializer):

    identifier = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):

        identifier = data['identifier']
        otp = data['otp']

        try:

            if "@" in identifier:
                user = User.objects.get(email=identifier)
            else:
                user = User.objects.get(phone=identifier)

        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if user.is_verified:
            raise serializers.ValidationError("Account already verified")

        if timezone.now() > user.otp_created_at + timedelta(minutes=settings.OTP_EXPIRY_MINUTES):
            raise serializers.ValidationError(
                "OTP expired. Please request a new one.")

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP")

        user.is_verified = True
        user.otp = None
        user.otp_created_at = None
        user.save()

        return data


class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token['role'] = user.role
        token['verified'] = user.is_verified

        return token

    def validate(self, attrs):

        data = super().validate(attrs)

        if not self.user.is_verified:
            raise serializers.ValidationError("Account not verified")

        return data


class ResendOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField()

    def validate_identifier(self, value):
        try:
            if "@" in value:
                user = User.objects.get(email=value)
            else:
                user = User.objects.get(phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        if user.is_verified:
            raise serializers.ValidationError("Account already verified")

        self.context['user'] = user
        return value

    def save(self):
        user = self.context['user']
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        if user.email:
            send_mail(
                "Chuks Kitchen - New OTP",
                f"Your new OTP is {otp}. Expires in {settings.OTP_EXPIRY_MINUTES} minutes.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
        return user
