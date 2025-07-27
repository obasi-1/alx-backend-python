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
        This method is called for all requests (list, create, retrieve, update, delete).
        It acts as a first-level check to ensure the user is logged in.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allows access only to participants in a conversation for object-level operations.
        'obj' here will be a Message or Conversation instance.

        This method is called for detail views (retrieve, update, delete) where a specific
        object instance is being accessed. It implicitly covers 'PUT', 'PATCH', and 'DELETE'
        methods by checking if the requesting user is a participant of the conversation
        associated with the object.
        """
        # If the object is a Message instance, check its associated conversation
        if hasattr(obj, 'conversation') and obj.conversation:
            return request.user in obj.conversation.participants.all()
        
        # If the object is a Conversation instance itself
        elif hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # If the object type is not handled or doesn't have relevant attributes
        return False

