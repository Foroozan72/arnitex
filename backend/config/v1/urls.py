from django.urls import path, include
from .swagger_urls import urlpatterns as swagger_urlpatterns

urlpatterns = [
<<<<<<< HEAD
    path('accounts/', include('accounts.urls')),
    path('basic/', include('basic_info.urls')),
=======
    path('accounts/', include('accounts.urls')), 
    path('', include(swagger_urlpatterns)),
>>>>>>> 4fed469bb1ab4676239b8120af28cd02dda18ee2
]
