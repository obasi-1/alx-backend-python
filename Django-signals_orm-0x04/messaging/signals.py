# messaging/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create a notification
    when a new Message instance is saved.
    """
    if created:
        # Create a notification for the message's receiver
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal handler to log message edits before the message is saved.
    """
    # Check if the message is being updated, not created
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            # Check if the content has actually changed
            if old_instance.content != instance.content:
                # Create a history entry with the old content
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_instance.content
                )
                # Mark the message as edited
                instance.edited = True
        except sender.DoesNotExist:
            pass # Message is new, so no history to log
