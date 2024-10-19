import jwt
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import MessagesSerializer
from .models import Message
from users.models import User
from gptconversations.models import Conversation


class GetMessages(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        owner = User.objects.get(username=request.user)
        conversations = owner.conversations.all()
        messages = []
        for conversation in conversations:
            messages += conversation.messages.all()
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data)
