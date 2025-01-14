from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'full_name']

    def get_full_name(self, obj):
        """
        Returns the full name of the user.
        """
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Includes sender information as a nested object and validates message_body length.
    """
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField(min_length=1, max_length=1000)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        """
        Custom validation for the message_body field.
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty or whitespace only.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    Includes participants and nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages_set')
    total_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'total_messages']

    def get_total_messages(self, obj):
        """
        Returns the total number of messages in the conversation.
        """
        return obj.messages.count()
