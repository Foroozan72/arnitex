from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

   
app_name = 'wallet'
router = DefaultRouter()

router.register(r'add-bank-account', views.AddBankAccount, basename='add-bank-account')
router.register(r'bank-account', views.BankAccountViewSet, basename='bank-account')
router.register(r'total-asset', views.TotalAsset, basename='total-asset')

urlpatterns = [
   path('',include(router.urls)),
]

