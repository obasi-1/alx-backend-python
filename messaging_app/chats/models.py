from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid # Import uuid for UUIDField

# Custom User Model extending AbstractUser
# This allows you to add custom fields and use a UUID as the primary key.
class User(AbstractUser):
    # Django's AbstractUser already provides:
    # username, password, email, first_name, last_name, is_staff, is_active, is_superuser, last_login, date_joined

    # Define user_id as a UUID primary key
    # default=uuid.uuid4 generates a new UUID for each new user
    # unique=True ensures each user_id is unique
    # primary_key=True sets this field as the primary key for the model
    # editable=False means this field won't be editable in Django Admin forms
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # Add custom fields not defined in AbstractUser
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

# Conversation Model
# Tracks which users are involved in a conversation.
class Conversation(models.Model):
    # Define conversation_id as a UUID primary key
    conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # Many-to-Many relationship with the custom User model.
    # A conversation can have multiple participants, and a user can be in multiple conversations.
    # We use 'User' (the string name of the model) because it's defined in the same app.
    # related_name='conversations' allows accessing conversations from a User instance (e.g., user.conversations.all())
    participants = models.ManyToManyField(User, related_name='conversations')
    # Optional: A name for the conversation, useful for group chats.
    name = models.CharField(max_length=255, blank=True, null=True)
    # Automatically sets the creation timestamp when a conversation is created.
    created_at = models.DateTimeField(auto_now_add=True)
    # Automatically updates the timestamp every time the conversation object is saved.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at'] # Order conversations by most recent activity
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        # Display a meaningful name for the conversation, or list participants
        if self.name:
            return self.name
        # Fallback to listing usernames if no name is provided
        return f"Conversation with {', '.join([p.username for p in self.participants.all()])}"

# Message Model
# Contains the sender, the conversation it belongs to, and the message content.
class Message(models.Model):
    # Define message_id as a UUID primary key
    message_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # Foreign Key to the Conversation model.
    # A message belongs to one conversation. If the conversation is deleted, messages are also deleted (CASCADE).
    # related_name='messages' allows accessing messages from a Conversation instance (e.g., conversation.messages.all())
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    # Foreign Key to the custom User model (sender of the message).
    # A message is sent by one user. If the sender is deleted, messages are also deleted (CASCADE).
    # related_name='sent_messages' allows accessing sent messages from a User instance (e.g., user.sent_messages.all())
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # The actual content of the message, renamed to message_body.
    message_body = models.TextField()
    # Automatically sets the timestamp when the message is created, renamed to sent_at.
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at'] # Order messages chronologically
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        # Display a meaningful string representation for the message
        return f"Message from {self.sender.username} in {self.conversation.name or self.conversation.id} at {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
