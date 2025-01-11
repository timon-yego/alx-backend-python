from django.test import TestCase
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

# Create your tests here.
class MessageNotificationTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')

    def test_notification_created_on_message(self):
        # Send a message
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")

        # Check that a notification was created
        notification = Notification.objects.get(user=self.receiver, message=message)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.read)

class MessageEditTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Original message")

    def test_message_edit_creates_history(self):
        self.message.content = "Edited message"
        self.message.save()
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original message")