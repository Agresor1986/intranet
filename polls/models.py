from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Choice(models.Model):
    name = models.CharField(max_length=20, verbose_name="názov")

    def __str__(self):
        return self.name

    def vote_count(self):
        return self.votes.count()

    class Meta:
        verbose_name = "možnosť"
        verbose_name_plural = "možnosti"

class Poll(models.Model):
    name = models.CharField(max_length=50, verbose_name="názov")
    description = models.TextField(verbose_name="popis")
    choices = models.ManyToManyField(Choice, related_name='related_polls', blank=True, verbose_name="možnosti")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="čas vytvorenia")
    end_date = models.DateTimeField(verbose_name="koniec hlasovania")  # Opravené: iba verbose_name
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_polls', verbose_name="vytvoril")
    notified_closed = models.BooleanField(default=False, verbose_name="notifikácia uzavretá")

    def __str__(self):
        return self.name

    def is_active(self):
        if timezone.is_naive(self.end_date):
            self.end_date = timezone.make_aware(self.end_date, timezone.get_current_timezone())
        return timezone.now() < self.end_date

    class Meta:
        verbose_name = "hlasovanie"
        verbose_name_plural = "hlasovania"

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True, verbose_name="hlasovanie")
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True, verbose_name="možnosť")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="používateľ")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="čas")

    def __str__(self):
        return f"{self.poll.name} - {self.choice.name}"

    class Meta:
        verbose_name = "hlas"
        verbose_name_plural = "hlasy"
