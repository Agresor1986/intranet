from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="používateľ")
    title = models.CharField(max_length=200, verbose_name="názov")
    description = models.TextField(verbose_name="popis")
    start_time = models.DateTimeField(db_index=True, verbose_name="začiatok")
    end_time = models.DateTimeField(db_index=True, verbose_name="koniec")
    COLOR_CHOICES = [
        ('#FF0000', 'Dôležité'),
        ('#00FF00', 'Pripomienky'),
        ('#0000FF', 'Porady'),
    ]
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FF0000', verbose_name="typ")
    is_global = models.BooleanField(default=False, verbose_name="globálna udalosť")
    notification_sent_today = models.BooleanField(default=False, verbose_name="notifikácia dnes")
    notification_sent_now = models.BooleanField(default=False, verbose_name="notifikácia teraz")
    notification_sent_5_min = models.BooleanField(default=False, verbose_name="notifikácia 5 minút")
    notification_sent_created = models.BooleanField(default=False, verbose_name="notifikácia vytvorená")

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        from django.urls import reverse
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}">{self.title}</a>'

    class Meta:
        verbose_name = "udalosť"
        verbose_name_plural = "udalosti"
