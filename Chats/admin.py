from django.contrib import admin
from .models import Message, BlockedUser

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'sender_delete', 'receiver_delete', 'timestamp')

admin.site.register(Message, MessageAdmin)
admin.site.register(BlockedUser)
