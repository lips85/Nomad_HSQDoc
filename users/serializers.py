from rest_framework.serializers import ModelSerializer
from .models import User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class UserSerializer(ModelSerializer):
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
