from rest_framework import serializers
from .models import Conversation
from users.serializers import UserConversationSerializer


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


class ConversationTotalUsageSerializer(serializers.ModelSerializer):

    conv_total_tokens = serializers.SerializerMethodField()
    total_messages = serializers.SerializerMethodField()
    latest_used_model = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "file_name",
            "conv_total_tokens",
            "total_messages",
            "latest_used_model",
        )

    def get_conv_total_tokens(self, conversation):
        return conversation.total_tokens()

    def get_total_messages(self, conversation):
        return conversation.total_messages()

    def get_latest_used_model(self, conversation):
        return conversation.latest_used_model()
