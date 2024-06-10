from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet

app_name = 'media_hub'
router = DefaultRouter()
router.register(r'image', ImageViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),
]