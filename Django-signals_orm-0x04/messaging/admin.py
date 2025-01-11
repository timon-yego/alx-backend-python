from django.contrib import admin
from .models import Message, Notification, MessageHistory

# Register your models here.
admin.site.register(Message)
admin.site.register(Notification)
admin.register(MessageHistory)