from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'basic_info'
router = DefaultRouter()

router.register(r'country', views.CountryViewSet, basename='country')
router.register(r'city', views.CityViewSet, basename='city')
router.register(r'country-read', views.CountryReadOnlyViewSet, basename='country-read')
router.register(r'city-read', views.CityReadOnlyViewSet, basename='city-read')
# router.register(r'wallet', views.WalletViewSet, basename='wallet')


urlpatterns = [
   path('',include(router.urls))
]



