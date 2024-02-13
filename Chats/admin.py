from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'seder_delete', 'receiver_delete', 'timestamp')

admin.site.register(Message, MessageAdmin)
