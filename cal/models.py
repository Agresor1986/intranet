from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    COLOR_CHOICES = [
        ('#FF0000', 'Dôležité'),
        ('#00FF00', 'Pripomienky'),
        ('#0000FF', 'Porady'),
    ]
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FF0000')
    is_global = models.BooleanField(default=False)
    notification_sent_today = models.BooleanField(default=False)  # Pridané pole
    notification_sent_five_minutes = models.BooleanField(default=False)  # Nové pole

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
