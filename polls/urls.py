from django.urls import path
from . import views

app_name = "PollApp"

urlpatterns = [
    path("", views.HomeView.as_view(), name="polls"),
    path("poll/<int:poll_id>/", views.PollView.as_view(), name="poll"),
    path('create/', views.CreatePollView.as_view(), name='create_polls'),
    path('delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),
]
