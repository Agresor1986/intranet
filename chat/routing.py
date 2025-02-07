from django.urls import path
from chat.consumers import ChatConsumer, PrivateChatConsumer

websocket_urlpatterns = [
    path("wss/group/", ChatConsumer.as_asgi()),  # pre skupinový chat
    path("wss/private/<str:username>/", PrivateChatConsumer.as_asgi()),  # pre súkromný chat
]

