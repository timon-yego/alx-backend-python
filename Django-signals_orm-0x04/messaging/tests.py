from django.test import TestCase
from .models import Message, Notification
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