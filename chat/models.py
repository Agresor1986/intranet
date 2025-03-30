from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", verbose_name="používateľ")
    content = models.TextField(blank=True, null=True, verbose_name="obsah")
    file = models.FileField(upload_to='files/', blank=True, null=True, verbose_name="súbor")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="čas")

    def __str__(self):
        return f"{self.user.username}: {self.content}"
    
    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None

    class Meta:
        verbose_name = "správa"
        verbose_name_plural = "správy"

class PrivateConversation(models.Model):
    user1 = models.ForeignKey(User, related_name="conversations_as_user1", on_delete=models.CASCADE, verbose_name="používateľ 1")
    user2 = models.ForeignKey(User, related_name="conversations_as_user2", on_delete=models.CASCADE, verbose_name="používateľ 2")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="čas vytvorenia")

    class Meta:
        unique_together = ("user1", "user2")
        verbose_name = "súkromná konverzácia"
        verbose_name_plural = "súkromné konverzácie"

    def __str__(self):
        return f"Konverzácia medzi {self.user1.username} a {self.user2.username}"

    @staticmethod
    def get_conversation(user1, user2):
        return PrivateConversation.objects.filter(
            (models.Q(user1=user1) & models.Q(user2=user2)) |
            (models.Q(user1=user2) & models.Q(user2=user1))
        ).first()

class PrivateMessage(models.Model):
    conversation = models.ForeignKey(PrivateConversation, on_delete=models.CASCADE, related_name="messages", verbose_name="konverzácia")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="odosielateľ")
    content = models.TextField(blank=True, null=True, verbose_name="obsah")
    file = models.FileField(upload_to='files/', blank=True, null=True, verbose_name="súbor")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="čas")

    def __str__(self):
        return f"{self.sender.username} to {self.conversation}: {self.content[:20]} ({self.timestamp})"
    
    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None

    class Meta:
        verbose_name = "súkromná správa"
        verbose_name_plural = "súkromné správy"
