from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'login-register', views.LoginRegisterViewSet, basename='login-register')
router.register(r'register-verify', views.RegisterVerify, basename='register-verify')
router.register(r'login-verify', views.LoginVerify, basename='login-verify')
router.register(r'forget-password-verify', views.ForgetPasswordVerify, basename='forget-password-verify')

urlpatterns = [
    path('', include(router.urls)),

]
