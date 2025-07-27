# messaging_app/chats/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation # Import your custom permission

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Conversation objects.
    Ensures only authenticated users who are participants can access conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    # IsAuthenticated is applied here as part of the permission_classes
    permission_classes = [IsAuthenticated, IsParticipantOfConversation] 

    def get_queryset(self):
        """
        Restricts the returned conversations to only those the
        current user is a participant of.
        """
        # Filter conversations to only include those where the requesting user is a participant
        if self.request.user.is_authenticated:
            return self.queryset.filter(participants=self.request.user).distinct()
        return self.queryset.none() # Return an empty queryset if user is not authenticated

    def perform_create(self, serializer):
        """
        When creating a new conversation, automatically add the creator as a participant.
        """
        # Save the conversation instance
        conversation = serializer.save()
        # Add the current authenticated user as a participant
        conversation.participants.add(self.request.user)
        # Ensure the conversation creator is also a participant
        # This assumes the 'participants' field is a ManyToManyField to User
        # and it's not set in the serializer's create method, allowing us to add it here.

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Message objects.
    Ensures only authenticated users who are participants of the message's conversation
    can send, view, update, and delete messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # IsAuthenticated is applied here as part of the permission_classes
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Restricts the returned messages to only those within conversations
        the current user is a participant of.
        """
        if self.request.user.is_authenticated:
            # Get all conversations the current user is a participant of
            user_conversations = Conversation.objects.filter(participants=self.request.user)
            # Filter messages that belong to these conversations
            # self.queryset is Message.objects.all(), so this is effectively Message.objects.filter(...)
            return self.queryset.filter(conversation__in=user_conversations) 
        return self.queryset.none() # Return an empty queryset if user is not authenticated

    def perform_create(self, serializer):
        """
        When creating a message, ensure the user is a participant of the target conversation.
        """
        conversation_id = self.request.data.get('conversation')
        if not conversation_id:
            return Response({"detail": "Conversation ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # This uses Conversation.objects.filter internally via get_object_or_404
            conversation = get_object_or_404(Conversation, pk=conversation_id)
        except Exception:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the requesting user is a participant of the conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Save the message, linking it to the conversation and the sender
        serializer.save(sender=self.request.user, conversation=conversation)

