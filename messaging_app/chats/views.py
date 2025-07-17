from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Q # For complex lookups

from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

# Conversation ViewSet
# Provides CRUD operations for Conversation objects.
class ConversationViewSet(viewsets.ModelViewSet):
    # Set the serializer class for this viewset.
    serializer_class = ConversationSerializer
    # Ensure only authenticated users can access these endpoints.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of conversations that the requesting user is a participant of.
        """
        # Filter conversations to only show those where the current user is a participant.
        # This ensures users only see conversations they are part of.
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        """
        Overrides the default create behavior to add the current user as a participant
        and handle additional participants if provided.
        """
        # Save the conversation instance without committing to the database yet.
        # This allows us to add participants before saving.
        conversation = serializer.save()
        # Add the requesting user as a participant to the new conversation.
        conversation.participants.add(self.request.user)

        # If the request includes 'participants_ids' in the data, add them.
        # This allows creating conversations with other users.
        # Expects a list of user_ids (UUIDs).
        participant_ids = self.request.data.get('participants_ids')
        if participant_ids:
            # Filter for valid users based on the provided IDs.
            # Exclude the requesting user if they are also in the list to avoid duplicates.
            new_participants = User.objects.filter(user_id__in=participant_ids).exclude(user_id=self.request.user.user_id)
            conversation.participants.add(*new_participants)

        # Save the conversation again to persist the participants.
        conversation.save()

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Custom action to list all messages within a specific conversation.
        Accessed via /conversations/{conversation_id}/messages/
        """
        # Get the conversation object based on the primary key (pk).
        conversation = get_object_or_404(Conversation, pk=pk)

        # Check if the requesting user is a participant in this conversation.
        # This enforces security: users can only see messages in conversations they belong to.
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get all messages related to this conversation, ordered by timestamp.
        messages = conversation.messages.all()
        # Serialize the messages. 'many=True' because there can be multiple messages.
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Custom action to send a new message to a specific conversation.
        Accessed via /conversations/{conversation_id}/send_message/
        """
        conversation = get_object_or_404(Conversation, pk=pk)

        # Check if the requesting user is a participant in this conversation.
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create a mutable copy of the request data to add sender and conversation.
        data = request.data.copy()
        data['sender'] = self.request.user.user_id # Set the sender to the current authenticated user's ID
        data['conversation'] = conversation.conversation_id # Link to the current conversation's ID

        # Initialize the MessageSerializer with the modified data.
        serializer = MessageSerializer(data=data, context={'request': request})

        # Validate the serializer data. If invalid, return errors.
        if serializer.is_valid():
            # Save the new message.
            serializer.save()
            # Return the created message data with HTTP 201 Created status.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If validation fails, return the errors with HTTP 400 Bad Request status.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Message ViewSet (for general message listing/retrieval, though often accessed via conversation)
# Provides read-only operations for Message objects.
# Note: For creating messages, the 'send_message' action on ConversationViewSet is preferred.
class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    # Set the serializer class for this viewset.
    serializer_class = MessageSerializer
    # Ensure only authenticated users can access these endpoints.
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of messages that belong to conversations the requesting user is a part of.
        """
        # Filter messages to only show those where the message's conversation
        # has the current user as a participant.
        # This prevents users from seeing messages in conversations they are not part of.
        return Message.objects.filter(conversation__participants=self.request.user).order_by('sent_at')
