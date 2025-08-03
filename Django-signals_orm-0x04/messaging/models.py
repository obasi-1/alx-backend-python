# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter for unread messages for a specific user.
    """
    def for_user(self, user):
        """
        Returns a queryset of unread messages for the specified user.
        """
        return self.filter(receiver=user, is_read=False).only('sender', 'content', 'timestamp')

class Message(models.Model):
    """
    Represents a message sent from one user to another.
    Includes a self-referential foreign key for threaded conversations.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')
    parent_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    is_read = models.BooleanField(default=False)

    objects = models.Manager() # The default manager
    unread_messages = UnreadMessagesManager() # Our custom manager

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

class MessageHistory(models.Model):
    """
    Represents a log of previous versions of a message.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Message histories'
        ordering = ['timestamp']

    def __str__(self):
        return f"History for message {self.message.id} at {self.timestamp}"
