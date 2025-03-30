import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="názov")
    file = models.FileField(upload_to='files/', verbose_name="súbor")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="čas nahratia")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="používateľ")

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "dokument"
        verbose_name_plural = "dokumenty"
