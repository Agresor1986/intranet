from django.urls import path
from chat.consumers import ChatConsumer, PrivateChatConsumer

websocket_urlpatterns = [
    path("ws/group/", ChatConsumer.as_asgi()),  
    path("ws/private/<str:username>/", PrivateChatConsumer.as_asgi()),  
]

