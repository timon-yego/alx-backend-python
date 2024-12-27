from rest_framework.permissions import BasePermission, IsAuthenticated

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with its messages.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow access if the user is a participant in the conversation
        return request.user in obj.conversation.participants.all()
