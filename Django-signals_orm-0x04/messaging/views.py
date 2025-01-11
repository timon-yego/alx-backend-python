from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def delete_user(request):
    user = request.user
    user.delete()  # Triggers the post_delete signal
    return redirect("logout")  # Redirect to the logout page or a suitable location