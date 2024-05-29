from django.urls import path, include
from .swagger_urls import urlpatterns as swagger_urlpatterns

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('basic/', include('basic_info.urls')),
    path('', include(swagger_urlpatterns)),
]
