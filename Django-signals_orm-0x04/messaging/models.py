from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, related_name="edited_messages", null=True, blank=True, on_delete=models.SET_NULL
    )
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )  # Self-referential field for replies
    read = models.BooleanField(default=False)  # Track if the message has been read

    # Add the custom manager
    objects = models.Manager()  # Default manager
    unread_objects = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
    
    def get_all_replies(self):
        """
        Recursively fetch all replies to this message.
        """
        all_replies = []

        def fetch_replies(message):
            replies = message.replies.all().select_related("sender", "receiver").prefetch_related("replies")
            for reply in replies:
                all_replies.append(reply)
                fetch_replies(reply)

        fetch_replies(self)
        return all_replies

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} regarding message {self.message.id}"
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id} edited at {self.edited_at}"

