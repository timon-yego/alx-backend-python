from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message

# Create your views here.
@login_required
def delete_user(request):
    user = request.user
    user.delete()  # Triggers the post_delete signal
    return redirect("logout")  # Redirect to the logout page or a suitable location

def message_thread(request, message_id):
    # Use select_related for foreign key fields and prefetch_related for replies
    message = Message.objects.filter(id=message_id).select_related('sender', 'receiver').prefetch_related('replies').first()

    if not message:
        return render(request, 'messaging/error.html', {'message': 'Message not found'})

    # Recursive query to get all replies, including nested replies
    def get_replies(message):
        replies = message.replies.all()
        for reply in replies:
            reply.replies = get_replies(reply)  # Recursively fetch replies
        return replies
    replies = get_replies(message)
    
    return render(request, 'messaging/message_thread.html', {'message': message, 'replies': replies})
