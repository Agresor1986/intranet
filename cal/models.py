from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField(db_index=True)  # Index pre rýchlejšie vyhľadávanie
    end_time = models.DateTimeField(db_index=True)  # Index pre rýchlejšie vyhľadávanie
    COLOR_CHOICES = [
        ('#FF0000', 'Dôležité'),  # Dôležité udalosti
        ('#00FF00', 'Pripomienky'),   # Bežné pripomienky
        ('#0000FF', 'Porady'),    # Stretnutia
    ]
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#FF0000')
    is_global = models.BooleanField(default=False)  # Ak je udalosť globálna, vidia ju všetci
    notification_sent_today = models.BooleanField(default=False)  # Zamedzí opakovaným notifikáciám
    notification_sent_five_minutes = models.BooleanField(default=False)  # Notifikácia 5 minút pred začiatkom

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        """ Vráti HTML odkaz na editáciu udalosti. """
        from django.urls import reverse
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}">{self.title}</a>'
