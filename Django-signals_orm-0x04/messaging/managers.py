# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter for unread messages for a specific user.
    """
    def for_user(self, user):
        """
        Returns a queryset of unread messages for the specified user.
        """
        return self.filter(receiver=user, is_read=False).only('sender', 'content', 'timestamp')
      
