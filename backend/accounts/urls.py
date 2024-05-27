from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'accounts'
router = DefaultRouter()
router.register(r'dev-login', views.DevLogin, basename='dev-login')
router.register(r'check-email', views.CheckEmail, basename='check-email')
router.register(r'check-phone_number', views.CheckPhoneNumber, basename='check-phone_number')
router.register(r'send-otp', views.SendOTP, basename='send-otp')
router.register(r'register-verify', views.RegisterVerify, basename='register-verify')
router.register(r'login-verify', views.LoginVerify, basename='login-verify')
router.register(r'forget-password-verify', views.ForgetPasswordVerify, basename='forget-password-verify')
router.register(r'change-password', views.ChangePassword, basename='change-password')
router.register(r'logout', views.LogoutViewSet, basename='logout')
urlpatterns = [
    path('', include(router.urls)),
    path('profile/', views.UserProfileView.as_view(), name='profile')
]
