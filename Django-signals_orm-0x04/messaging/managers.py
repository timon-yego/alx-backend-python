from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return all unread messages for a specific user.
        """
        return self.filter(receiver=user, read=False)

    def unread_count(self, user):
        """
        Return the count of unread messages for a specific user.
        """
        return self.filter(receiver=user, read=False).count()
