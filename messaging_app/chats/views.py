from rest_framework import viewsets
from .models import Conversation, Message # Assuming these models exist in chats/models.py
from .serializers import ConversationSerializer, MessageSerializer # Assuming these serializers exist
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    Access is restricted to participants of the conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation] # Apply custom permission here

    def get_queryset(self):
        """
        This view should return a list of all conversations
        for the currently authenticated user.
        """
        user = self.request.user
        # The queryset is filtered to only include conversations where the user is a participant.
        return Conversation.objects.filter(participants=user)

    def perform_create(self, serializer):
        """
        When creating a new conversation, automatically add the creator
        to the list of participants.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or created within a conversation.
    This view assumes it is used with nested routing, like '/conversations/<conversation_pk>/messages/'.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation] # The same permission protects messages

    def get_queryset(self):
        """
        This view returns messages only from the specific conversation
        defined in the URL, and only if the user is a participant.
        """
        # Get the conversation_pk from the URL
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            # The permission class will already have run and verified the user can access
            # the parent conversation. We just need to filter the messages.
            return Message.objects.filter(conversation_id=conversation_pk)
        # If no conversation is specified in the URL, return no messages.
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        When creating a message, automatically set the sender to the current user
        and associate it with the conversation from the URL.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        try:
            conversation = Conversation.objects.get(pk=conversation_pk)
            # The IsParticipantOfConversation permission has already verified the user
            # is part of this conversation, so we can safely save the message.
            serializer.save(sender=self.request.user, conversation=conversation)
        except Conversation.DoesNotExist:
            # This case should ideally not be reached if routing is correct and permissions are checked.
            pass
