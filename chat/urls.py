from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('private/<str:username>/', views.private_chat, name='private_chat'),
]  
