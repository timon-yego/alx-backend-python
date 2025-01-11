from django.db.models.signals import post_save, pre_save, post_delete 
from django.dispatch import receiver
from .models import Message, Notification,MessageHistory 
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the receiver
        Notification.objects.create(user=instance.receiver, message=instance)

receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Ensure this is an update, not a creation
        original_message = Message.objects.filter(pk=instance.pk).first()
        if original_message and original_message.content != instance.content:
            # Save old content in MessageHistory
            MessageHistory.objects.create(
                message=original_message,
                old_content=original_message.content
            )
            # Mark the message as edited
            instance.edited = True
            # Ensure edited_by is updated if not already set
            if not instance.edited_by:
                instance.edited_by = original_message.edited_by

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete all messages where the user is the sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications associated with the user
    Notification.objects.filter(user=instance).delete()

    # Message history will be automatically deleted due to CASCADE
    # No additional cleanup is necessary for MessageHistory