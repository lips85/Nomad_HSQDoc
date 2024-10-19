import jwt
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from . import serializers
from .models import Message
from users.models import User
from gptconversations.models import Conversation


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

    def get(self, request, id):
        conversation = self.get_conversation(id)
        messages = conversation.messages.all()
        serializer = serializers.MessagesInConversationSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        conversation = self.get_conversation(id)
        if conversation.owner != request.user:
            raise PermissionDenied
        user_message = request.data.get("user_message")
        ai_message = request.data.get("ai_message")
        if not (user_message and ai_message):
            return Response(
                {"error": "Please Give User and AI Message"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.MessagesSerializer(data=request.data)
        if serializer.is_valid():
            new_message = serializer.save(conversation=conversation)
            serializer = serializers.MessagesSerializer(new_message)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
