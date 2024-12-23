from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from messaging_app.chats.views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
