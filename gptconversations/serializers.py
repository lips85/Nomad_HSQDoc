from rest_framework import serializers
from .models import Conversation
from users.serializers import UserSerializer
from gptmessages.serializers import MessagesIdListSerializer


class ConversationsSerializer(serializers.ModelSerializer):
    messages = MessagesIdListSerializer(many=True)

    class Meta:
        model = Conversation
        fields = (
            "id",
            "pdf",
            "messages",
        )
