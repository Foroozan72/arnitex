from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'basic_info'
router = DefaultRouter()

router.register(r'country', views.CountryViewSetApiView, basename='country')
router.register(r'city', views.CityViewSetApiView, basename='city')


urlpatterns = [
   path('',include(router.urls))
]



