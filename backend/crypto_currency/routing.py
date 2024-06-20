from django.urls import re_path, path

from .consumers import CryptoConsumer

websocket_urlpatterns = [
    path("ws/crypto/<int:limit>/", CryptoConsumer.as_asgi()),
]