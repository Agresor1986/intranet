from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    url = models.URLField(blank=True, null=True)  # Odkaz na akciu
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)



   
