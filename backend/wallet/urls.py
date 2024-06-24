from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'wallet'
router = DefaultRouter()

router.register(r'create_wallet', views.CreateWalletViewSet, basename='create_wallet')
router.register(r'read_wallet', views.WalletReadOnlyViewSet, basename='read_wallet')
router.register(r'read_transaction', views.TransactionReadOnlyViewSet, basename='read_transaction')

urlpatterns = [
   path('',include(router.urls))
]

