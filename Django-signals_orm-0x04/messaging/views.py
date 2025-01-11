from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm


# Create your views here.
@login_required
def delete_user(request):
    user = request.user
    user.delete()  # Triggers the post_delete signal
    return redirect("logout")  # Redirect to the logout page or a suitable location

def threaded_conversation(request):
    """
    Fetch and display all top-level messages (parent_message is NULL) 
    where the logged-in user is either the sender or the receiver.
    """
    # Fetch all top-level messages where the logged-in user is the sender
    sent_messages = Message.objects.filter(
        parent_message__isnull=True, sender=request.user
    ).select_related("sender", "receiver").prefetch_related("replies")

    # Fetch all top-level messages where the logged-in user is the receiver
    received_messages = Message.objects.filter(
        parent_message__isnull=True, receiver=request.user
    ).select_related("sender", "receiver").prefetch_related("replies")

    # Combine sent and received messages (optional, can be displayed separately if needed)
    messages = sent_messages | received_messages

    return render(request, "messaging/threaded_conversation.html", {
        "messages": messages
    })


def send_message(request):
    """
    Handle sending a new message. The logged-in user will automatically be set as the sender.
    """
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            # Create the message but don't save it yet
            message = form.save(commit=False)
            # Set the sender as the logged-in user
            message.sender = request.user
            # Save the message
            message.save()
            # Redirect to the threaded conversation view after saving
            return redirect("messaging:threaded_conversation")
    else:
        form = MessageForm()

    return render(request, "messaging/send_message.html", {"form": form})

