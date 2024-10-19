import jwt
import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from users.models import User
from . import serializers


class UserRegister(APIView):

    # create account
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not password or not username:
            return Response(
                {"error": "Username and Password is Required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 이미 있는 username이 있는지 확인하고 있으면 에러 반환
        try:
            is_username_exist = User.objects.get(username=username)
            if is_username_exist:
                return Response(
                    {"error": "This Username is already used"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            is_username_exist = False
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):

    permission_classes = [IsAuthenticated]

    # get user info
    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    # update user info
    def put(self, request):
        user = request.user
        serializer = serializers.UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            if old_password != new_password:
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "error": "Old password and new password is same. Write proper new password"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Old password is wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        # username이 존재하는지 먼저 확인하고 없으면 에러 반환
        try:
            User.objects.get(username=username)
        except:
            return Response(
                {"error": "wrong username"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # user를 확인하고 없으면 이미 username을 확인했기 때문에 password가 잘못된거다
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response(
                {"error": "wrong password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        response = Response({"ok": "bye!"})
        return response
