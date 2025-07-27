# messaging_app/chats/filters.py

import django_filters
from django.contrib.auth import get_user_model # Recommended way to get the User model
from .models import Message, Conversation

User = get_user_model() # Get the currently active User model

class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for Message objects.
    Allows filtering messages by:
    - 'sender__username': Filter by the username of the sender (exact match).
    - 'timestamp_after': Messages sent after a specific datetime.
    - 'timestamp_before': Messages sent before a specific datetime.
    """
    # Filter by sender's username (case-insensitive exact match)
    sender_username = django_filters.CharFilter(
        field_name='sender__username', 
        lookup_expr='iexact', 
        label='Sender Username (case-insensitive)'
    )
    
    # Filter by timestamp range
    timestamp = django_filters.DateTimeFromToRangeFilter(
        field_name='timestamp', 
        label='Timestamp Range (e.g., 2023-01-01T00:00:00 to 2023-01-31T23:59:59)'
    )

    class Meta:
        model = Message
        fields = ['sender_username', 'timestamp'] # Fields available for filtering

