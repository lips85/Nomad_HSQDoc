from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from . import serializers
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
        if not (message_role and message_content):
            return Response(
                {"error": "Please Give Message Role and Content"},
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
