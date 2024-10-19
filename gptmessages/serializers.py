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


class MessagesIdListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("id",)
