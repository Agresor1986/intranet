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
    path("", home_view, name="home"),
    path("", include("notifications.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('chat/', include('chat.urls')),
    path("calendar/", include("cal.urls")),
    path("forum/", include("forum.urls")),
    path("polls/", include("polls.urls")),
    path("documents/", include("documents.urls")),
    path("mail/", include("mail.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
