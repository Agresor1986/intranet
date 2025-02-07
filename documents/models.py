import os
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # Odstráni súbor zo systému
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.title
