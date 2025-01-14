from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of a conversation to access and perform actions on messages.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        is_participant = request.user in obj.conversation.participants.all()

        # Allow access only if the user is a participant
        if request.method in SAFE_METHODS:  # Read-only operations (e.g., GET)
            return is_participant

        # Allow modification (POST, PUT, DELETE) if the user is a participant
        return is_participant
