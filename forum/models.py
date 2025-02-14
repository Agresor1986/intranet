from django.db import models
from django.contrib.auth.models import User
    
class Forum(models.Model):
    topic = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, blank=True)
    link = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    class Meta:
        verbose_name = "Diskusné fórum"
        verbose_name_plural = "Diskusné fóra"

    def __str__(self):
        return self.topic

    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None


class Discussion(models.Model):
    forum = models.ForeignKey(Forum, null=True, blank=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)

    class Meta:
        verbose_name = "Diskusia"
        verbose_name_plural = "Diskusie"

    def __str__(self):
        return f"Diskusia v {self.forum.topic} od {self.author.username}"

    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None
