from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Choice(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Poll(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    choices = models.ManyToManyField(Choice, related_name='related_polls', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField('end date')  # Pridané pole pre dátum ukončenia hlasovania

    def __str__(self):
        return self.name

    def is_active(self):
        return timezone.now() < self.end_date  # Metóda na kontrolu, či je hlasovanie aktívne

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.poll.name} - {self.choice.name}"
