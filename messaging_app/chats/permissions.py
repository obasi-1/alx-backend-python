from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    
    This permission ensures that:
    1. The user is authenticated.
    2. The user is a participant in the conversation object being accessed.
    """

    def has_permission(self, request, view):
        """
        Global permission check.
        
        This ensures that the user is authenticated before any other checks are made.
        """
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        
        This method is called for detail views (GET, PUT, DELETE) and checks if
        the user is a participant of the specific `obj` instance.
        
        - If `obj` is a Conversation, it checks `obj.participants`.
        - If `obj` is a Message, it checks the participants of `obj.conversation`.
        """
        # Check for Conversation objects. Assumes a 'participants' ManyToManyField.
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        # Check for Message objects. Assumes a 'conversation' ForeignKey.
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
            
        return False
