from django.db import models
from common.models import CommonModel


# Create your models here.
class Message(CommonModel):

    class MessageRoleChoices(models.TextChoices):
        HUMAN = ("human", "human")
        AI = ("ai", "ai")

    conversation = models.ForeignKey(
        "gptconversations.Conversation",
        on_delete=models.CASCADE,
        related_name="messages",
    )

    message_role = models.CharField(
        max_length=10,
        choices=MessageRoleChoices.choices,
        null=True,
        blank=True,
    )

    message_content = models.TextField(
        null=True,
        blank=True,
    )

    # def __str__(self):
    #     return self.name
