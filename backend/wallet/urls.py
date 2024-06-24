from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'wallet'
router = DefaultRouter()

router.register(r'create_wallet', views.CreateWalletViewSet, basename='create_wallet')

urlpatterns = [
   path('',include(router.urls))
]
