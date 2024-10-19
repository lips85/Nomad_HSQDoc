from rest_framework import serializers
from .models import Conversation
from users.serializers import UserConversationSerializer
from gptmessages.serializers import MessagesInConversationSerializer


class ConversationsSerializer(serializers.ModelSerializer):
    owner = serializers.CharField()

    class Meta:
        model = Conversation
        fields = "__all__"


class ConversationSerializer(serializers.ModelSerializer):
    owner = UserConversationSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = "__all__"


class ConversationMessagesSerializer(serializers.ModelSerializer):
    messages = MessagesInConversationSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Conversation
        fields = (
            "id",
            "title",
            "messages",
        )
