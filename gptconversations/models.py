from django.db import models
from common.models import CommonModel


# Create your models here.
class Conversation(CommonModel):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="conversations",
    )

    title = models.CharField(
        max_length=150,
    )

    file_name = models.CharField(
        max_length=150,
        default="",
        null=True,
        blank=True,
    )

    file_url = models.URLField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
