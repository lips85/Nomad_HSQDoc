from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

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
        try:
            is_title_already_used = Conversation.objects.get(title=title)
            if is_title_already_used:
                return Response(
                    {"error": "This Title is already used"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            is_title_already_used = False
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
        if conversation.owner != request.user:
            raise PermissionDenied
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
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, id):
        conversation = self.get_conversation(id)
        if conversation.owner != request.user:
            raise PermissionDenied
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
