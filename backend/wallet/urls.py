from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

   
app_name = 'wallet'
router = DefaultRouter()

router.register(r'create_wallet', views.CreateWalletViewSet, basename='create_wallet')
router.register(r'read_wallet', views.WalletReadOnlyViewSet, basename='read_wallet')
router.register(r'read_transaction', views.TransactionReadOnlyViewSet, basename='read_transaction')
router.register(r'transfer_wallet', views.WalletViewSetTransfer, basename='transfer_wallet') 


urlpatterns = [
   path('',include(router.urls)),
   path('check_wallet/<str:wallet_id>/', views.CheckWalletView.as_view(), name='check_wallet'),
]

