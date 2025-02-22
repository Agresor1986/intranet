from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.user.username}'s Profile"

class SentEmail(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_emails")
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    file = models.FileField(upload_to='files/', blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Email from {self.sender.username} to {self.recipient}"

    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None
