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
        self.sender = User.objects.create_user(username="sender", password="password")
        self.receiver = User.objects.create_user(username="receiver", password="password")
        self.editor = User.objects.create_user(username="editor", password="password")
        self.message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Original content")

    def test_message_edit_logs_history_and_editor(self):
        self.message.content = "Updated content"
        self.message.edited_by = self.editor
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original content")
        self.assertTrue(self.message.edited)
        self.assertEqual(self.message.edited_by, self.editor)

class UserDeletionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Test message")
        self.notification = Notification.objects.create(user=self.user2, message=self.message, content="Test notification")

    def test_user_deletion_cleans_up_related_data(self):
        self.user1.delete()
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 0)
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)

        self.user2.delete()
        self.assertEqual(Message.objects.filter(receiver=self.user2).count(), 0)
        self.assertEqual(Notification.objects.filter(user=self.user2).count(), 0)

class ThreadedConversationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.user3 = User.objects.create_user(username="user3", password="password")

        self.message1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello!")
        self.reply1 = Message.objects.create(
            sender=self.user2, receiver=self.user1, content="Hi!", parent_message=self.message1
        )
        self.reply2 = Message.objects.create(
            sender=self.user1, receiver=self.user2, content="How are you?", parent_message=self.reply1
        )
    def test_recursive_replies(self):
        replies = self.message1.get_all_replies()
        self.assertIn(self.reply1, replies)
        self.assertIn(self.reply2, replies)