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

def threaded_conversation(request):
    # Fetch top-level messages (no parent)
    top_level_messages = Message.objects.filter(parent_message__isnull=True).select_related(
        "sender", "receiver"
    ).prefetch_related("replies")

    context = {"messages": top_level_messages}
    return render(request, "messaging/threaded_conversation.html", context)