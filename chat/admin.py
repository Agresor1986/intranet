from django.contrib import admin
from .models import Message, PrivateMessage

admin.site.register(Message)
admin.site.register(PrivateMessage)

