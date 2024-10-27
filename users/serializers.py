from rest_framework import serializers
from .models import User


class UserConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "last_login",
            "date_joined",
            "groups",
            "user_permissions",
        )


class UserStatsSerializer(serializers.ModelSerializer):

    user_total_conversations = serializers.SerializerMethodField()
    user_total_messages = serializers.SerializerMethodField()
    user_total_tokens = serializers.SerializerMethodField()
    user_total_cost = serializers.SerializerMethodField()
    total_files = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "user_total_conversations",
            "user_total_tokens",
            "user_total_cost",
            "user_total_messages",
            "total_files",
            "openai_tokens",
            "claude_tokens",
        )

    def get_user_total_conversations(self, user):
        return user.total_conversations()

    def get_user_total_messages(self, user):
        return user.total_messages()

    def get_user_total_tokens(self, user):
        return user.total_tokens()

    def get_user_total_cost(self, user):
        return user.total_cost()

    def get_total_files(self, user):
        return user.total_files()
