from django.urls import re_path, path

from .consumers import CryptoTableConsumer

websocket_urlpatterns = [
    path("ws/crypto/table/<int:limit>/", CryptoTableConsumer.as_asgi()),
]