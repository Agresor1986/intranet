from django.urls import path
from . import views  # Import views zo súčasnej aplikácie

urlpatterns = [
    path('', views.send_mail_page, name='send_mail_page'),
]
