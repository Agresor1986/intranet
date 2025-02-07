from django.contrib import admin
from .models import SentEmail


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'timestamp')
    list_filter = ('sender', 'timestamp')
    search_fields = ('recipient', 'subject', 'message')
