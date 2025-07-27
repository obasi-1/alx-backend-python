from rest_framework import permissions

class IsParticipantInConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    This permission checks if the requesting user is part of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation object.
        
        This method is called by DRF for detail views (GET, PUT, DELETE on /conversations/{id}/).
        The `obj` here is an instance of the `Conversation` model.
        """
        # We assume the `Conversation` model has a ManyToManyField named 'participants'
        # that links to the User model.
        # The permission is granted if the user making the request is in the set of participants.
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # If the object is a Message, we check the conversation it belongs to.
        # This assumes your Message model has a ForeignKey to Conversation named 'conversation'.
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
            
        return False
