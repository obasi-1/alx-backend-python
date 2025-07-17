from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model extending AbstractUser
# This allows you to add custom fields to the User model later if needed,
# without modifying Django's built-in User model directly.
class User(AbstractUser):
    # Add any additional fields here if necessary, e.g.:
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # bio = models.TextField(blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

# Conversation Model
# Tracks which users are involved in a conversation.
class Conversation(models.Model):
    # Many-to-Many relationship with the custom User model.
    # A conversation can have multiple participants, and a user can be in multiple conversations.
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
        return f"Conversation with {', '.join([p.username for p in self.participants.all()])}"

# Message Model
# Contains the sender, the conversation it belongs to, and the message content.
class Message(models.Model):
    # Foreign Key to the Conversation model.
    # A message belongs to one conversation. If the conversation is deleted, messages are also deleted (CASCADE).
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    # Foreign Key to the custom User model (sender of the message).
    # A message is sent by one user. If the sender is deleted, messages are also deleted (CASCADE).
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # The actual content of the message.
    content = models.TextField()
    # Automatically sets the timestamp when the message is created.
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # Order messages chronologically
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation.name or self.conversation.id}"
