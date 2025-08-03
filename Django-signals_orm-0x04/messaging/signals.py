# messaging/signals.py
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User
from django.utils import timezone

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
                # Mark the message as edited and set the edit time and user.
                # In a real-world scenario, you would pass the current user
                # to the signal, but for this example, we assume the sender is the editor.
                instance.edited = True
                instance.edited_at = timezone.now()
                instance.edited_by = instance.sender
        except sender.DoesNotExist:
            pass # Message is new, so no history to log

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal handler to delete all messages, notifications, and
    message histories associated with a user after they are deleted.
    
    Note: Foreign key constraints with CASCADE on the models will
    handle most of this automatically, but this signal provides a clear,
    explicit way to ensure all related data is cleaned up.
    """
    # Delete all sent and received messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Message histories are linked to messages, so they will be deleted
    # when the corresponding messages are deleted due to CASCADE.
    # This explicit check is for clarity and robustness.
    for message in Message.objects.filter(sender=instance) | Message.objects.filter(receiver=instance):
        MessageHistory.objects.filter(message=message).delete()# messaging/signals.py
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User
from django.utils import timezone

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
                # Mark the message as edited and set the edit time and user.
                # In a real-world scenario, you would pass the current user
                # to the signal, but for this example, we assume the sender is the editor.
                instance.edited = True
                instance.edited_at = timezone.now()
                instance.edited_by = instance.sender
        except sender.DoesNotExist:
            pass # Message is new, so no history to log

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal handler to delete all messages, notifications, and
    message histories associated with a user after they are deleted.
    
    Note: Foreign key constraints with CASCADE on the models will
    handle most of this automatically, but this signal provides a clear,
    explicit way to ensure all related data is cleaned up.
    """
    # Delete all sent and received messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Message histories are linked to messages, so they will be deleted
    # when the corresponding messages are deleted due to CASCADE.
    # This explicit check is for clarity and robustness.
    for message in Message.objects.filter(sender=instance) | Message.objects.filter(receiver=instance):
        MessageHistory.objects.filter(message=message).delete()
