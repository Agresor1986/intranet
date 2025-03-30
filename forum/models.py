from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
    topic = models.CharField(max_length=300, verbose_name="téma")
    description = models.CharField(max_length=1000, blank=True, verbose_name="popis")
    link = models.CharField(max_length=100, blank=True, null=True, verbose_name="odkaz")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="čas vytvorenia")
    file = models.FileField(upload_to='files/', blank=True, null=True, verbose_name="súbor")

    class Meta:
        verbose_name = "diskusné fórum"
        verbose_name_plural = "diskusné fóra"

    def __str__(self):
        return self.topic

    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None

class Discussion(models.Model):
    forum = models.ForeignKey(Forum, null=True, blank=True, on_delete=models.CASCADE, verbose_name="fórum")
    discuss = models.CharField(max_length=1000, blank=True, null=True, verbose_name="diskusia")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="autor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="čas vytvorenia")
    link = models.CharField(max_length=100, blank=True, null=True, verbose_name="odkaz")
    file = models.FileField(upload_to='files/', blank=True, null=True, verbose_name="súbor")

    class Meta:
        verbose_name = "diskusia"
        verbose_name_plural = "diskusie"

    def __str__(self):
        return f"Diskusia v {self.forum.topic} od {self.author.username}"

    def file_name(self):
        return self.file.name.split('/')[-1] if self.file else None
