from django.db import models
from common.models import CommonModel


# Create your models here.
class Conversation(CommonModel):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="conversations",
    )

    # later change to file
    pdf = models.CharField(
        max_length=150,
    )

    def __str__(self):
        return f"{self.owner}'s {self.pdf} conversation"
