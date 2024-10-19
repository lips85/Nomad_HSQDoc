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
from .models import Conversation
from users.models import User


class ConversationsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        owner = User.objects.get(username=request.user)
        conversations = owner.conversations.all()
        serializer = serializers.ConversationsSerializer(conversations, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get("title")
        if not title:
            return Response(
                {"error": "Please Write a Title for the Conversation"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.ConversationSerializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save(owner=request.user)
            serializer = serializers.ConversationSerializer(conversation)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_conversation(self, id):
        try:
            return Conversation.objects.get(id=id)
        except:
            raise NotFound

    def get(self, request, id):
        conversation = self.get_conversation(id)
        serializer = serializers.ConversationSerializer(conversation)
        return Response(serializer.data)

    def put(self, request, id):
        conversation = self.get_conversation(id)
        if conversation.owner != request.user:
            raise PermissionDenied
        serializer = serializers.ConversationSerializer(
            conversation,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_conversation = serializer.save()
            serializer = serializers.ConversationSerializer(updated_conversation)
            return Response(serializer.data)

    def delete(self, request, id):
        conversation = self.get_conversation(id)
        if conversation.owner != request.user:
            raise PermissionDenied
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
