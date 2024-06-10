from django.urls import path, include
from .swagger_urls import urlpatterns as swagger_urlpatterns

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('basic-info/', include('basic_info.urls')),
    path('media-hub/', include('media_hub.urls')),
    path('support/', include('support.urls')),
    path('digital_currency/', include('digital_currency.urls')),
    path('', include(swagger_urlpatterns)),
]
