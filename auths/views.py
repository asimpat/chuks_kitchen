from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer, VerifyOTPSerializer, CustomTokenSerializer, ResendOTPSerializer
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction


class SignupView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):

        serializer = SignupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        # Try sending email
        if user.email:
            send_mail(
                "Chuks Kitchen Verification Code",
                f"Your OTP is {user.otp} as {user.role}. It expires in {settings.OTP_EXPIRY_MINUTES} minutes.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )

        return Response({
            "success": True,
            "message": "Signup successful. Check your email for OTP."
        }, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():

            return Response({
                "success": True,
                "message": "Account verified successfully"
            })

        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "New OTP sent"})
        return Response({"success": False, "errors": serializer.errors}, status=400)
