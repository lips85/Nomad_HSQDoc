from rest_framework import serializers
from .models import Message


class MessagesSerializer(serializers.ModelSerializer):
    conversation = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "message_role",
            "message_content",
            "model",
            "token",
        )


class MessagesInConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "message_role",
            "message_content",
            "model",
            "token",
        )
