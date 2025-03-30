from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name="používateľ")

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "profil používateľa"
        verbose_name_plural = "profily používateľov"

class SentEmail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_emails", verbose_name="odosielateľ")
    recipient = models.EmailField(verbose_name="príjemca")
    subject = models.CharField(max_length=255, verbose_name="predmet")
    message = models.TextField(verbose_name="správa")
    file = models.FileField(upload_to='files/', blank=True, null=True, verbose_name="súbor")
    timestamp = models.DateTimeField(default=now, verbose_name="čas odoslania")

    def __str__(self):
        return f"Email od {self.sender.username} pre {self.recipient}"

    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None

    class Meta:
        verbose_name = "odoslaný email"
        verbose_name_plural = "odoslané emaily"
