from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnreadMessagesView, MessageViewSet

# Create a DefaultRouter instance
router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Automatically includes the routes for the views
    path('unread/', UnreadMessagesView.as_view(), name='unread-messages'),  # For unread messages
]
