from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from . import serializers
from users.models import User
from gptconversations.models import Conversation
from users.serializers import UserStatsSerializer
from utils.constants import AI_MODEL


class MessagesLists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        owner = User.objects.get(username=request.user)
        conversations = owner.conversations.all()
        messages = []
        for conversation in conversations:
            messages += conversation.messages.all()
        serializer = serializers.MessagesSerializer(messages, many=True)
        return Response(serializer.data)


class ConversationMessages(APIView):

    permission_classes = [IsAuthenticated]

    def get_conversation(self, id):
        try:
            return Conversation.objects.get(id=id)
        except:
            raise NotFound

    def get_user(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except:
            raise NotFound

    def get_token_data(self, user, token, model):
        if model == AI_MODEL[1]:
            token_data = {
                "openai_tokens": user.openai_tokens + token,
                "claude_tokens": user.claude_tokens,
            }
        elif model == AI_MODEL[2]:
            token_data = {
                "openai_tokens": user.openai_tokens,
                "claude_tokens": user.claude_tokens + token,
            }
        return token_data

    def get(self, request, id):
        conversation = self.get_conversation(id)
        if conversation.owner != request.user:
            raise PermissionDenied
        messages = conversation.messages.all()
        serializer = serializers.MessagesInConversationSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        conversation = self.get_conversation(id)
        if conversation.owner != request.user:
            raise PermissionDenied
        message_role = request.data.get("message_role")
        message_content = request.data.get("message_content")
        token = request.data.get("token")
        model = request.data.get("model")
        user = self.get_user(request.user)
        token_data = self.get_token_data(user, token, model)

        if not (message_role and message_content):
            return Response(
                {"error": "Please Give Message Role and Content"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        message_serializer = serializers.MessagesSerializer(data=request.data)
        stats_serializer = UserStatsSerializer(
            user,
            data=token_data,
            partial=True,
        )
        if message_serializer.is_valid() and stats_serializer.is_valid():
            updated_stats = stats_serializer.save()
            stats_serializer = UserStatsSerializer(updated_stats)
            new_message = message_serializer.save(conversation=conversation)
            message_serializer = serializers.MessagesSerializer(new_message)
            return Response(message_serializer.data)
        else:
            return Response(
                message_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
