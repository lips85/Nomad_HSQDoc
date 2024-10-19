from rest_framework import serializers
from .models import Message


class MessagesSerializer(serializers.ModelSerializer):
    conversation = serializers.CharField()

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "user_message",
            "ai_message",
        )


class MessagesInConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            "user_message",
            "ai_message",
        )
