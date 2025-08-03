# messaging/admin.py
from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Message model.
    """
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'receiver__username', 'content')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Notification model.
    """
    list_display = ('user', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('user__username', 'message__content')
