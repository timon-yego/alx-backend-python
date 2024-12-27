from rest_framework.permissions import BasePermission

class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission to ensure users can access only their own conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming obj has participants field listing users in the conversation
        return request.user in obj.participants.all()