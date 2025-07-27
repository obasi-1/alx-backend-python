# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of a conversation to send, view, update, and delete messages within that conversation.
    """

    def has_permission(self, request, view):
        """
        Allows access only to authenticated users.
        """
        # This check is also handled by DEFAULT_PERMISSION_CLASSES in settings.py,
        # but keeping it here for explicit clarity within the custom permission.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allows access only to participants in a conversation for message operations.
        'obj' here will be a Message or Conversation instance.
        """
        # If the object is a Message instance
        if hasattr(obj, 'conversation') and obj.conversation:
            return request.user in obj.conversation.participants.all()
        
        # If the object is a Conversation instance itself
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False
