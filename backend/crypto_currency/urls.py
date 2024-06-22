from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'list', views.ListCryptoCurrensy, basename='list')
router.register(r'swap', views.SwapCryptoCurrensy, basename='swap')
router.register(r'swap-dollar-count', views.SwapDollarCryptoCurrensy, basename='swap-dollar-count')

urlpatterns = [
    path('', include(router.urls)), 
    path('crypto-dashboard/', views.crypto_dashboard, name='crypto_dashboard'),
]