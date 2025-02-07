from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<int:event_id>/', views.event, name='event_edit'),
    path('event/delete/<int:event_id>/', views.delete_event, name='event_delete'),  # Pridaná URL pre mazanie
    path('', views.CalendarView.as_view(), name='calendar'),
]
