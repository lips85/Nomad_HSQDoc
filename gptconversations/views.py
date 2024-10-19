import jwt
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import ConversationsSerializer
from .models import Conversation
from users.models import User


class GetConversations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        owner = User.objects.get(username=request.user)
        conversations = owner.conversations.all()
        # conversations = Conversation.objects.filter(owner=owner)
        serializer = ConversationsSerializer(conversations, many=True)
        return Response(serializer.data)
