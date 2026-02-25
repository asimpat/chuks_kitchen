from django.urls import path
from .views import SignupView, VerifyOTPView, LoginView, ResendOTPView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny




class CustomTokenView(TokenObtainPairView):
    permission_classes = [AllowAny]
   
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),

    
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
]