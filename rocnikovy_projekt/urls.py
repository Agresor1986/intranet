"""
URL configuration for rocnikovy_projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from notifications.models import Notification
from django.conf.urls.static import static
from django.conf import settings


def home_view(request):
    """Hlavná stránka + notifikácie iba v home.html."""
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-timestamp") if request.user.is_authenticated else []
    return render(request, "home.html", {"notifications": notifications})

urlpatterns = [
    path("admin/", admin.site.urls),

    # Hlavná stránka + notifikácie iba pre home
    path("", home_view, name="home"),

    # Notifikácie cez include pre akcie
    path("", include("notifications.urls")),

    # Autentifikácia a ostatné aplikácie
    path("accounts/", include("django.contrib.auth.urls")),
    path('chat/', include('chat.urls')),
    path("calendar/", include("cal.urls")),
    path("forum/", include("forum.urls")),
    path("polls/", include("polls.urls")),
    path("documents/", include("documents.urls")),
    path("mail/", include("mail.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
