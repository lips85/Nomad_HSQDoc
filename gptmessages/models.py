from django.db import models
from common.models import CommonModel


# Create your models here.
class Message(CommonModel):
    conversation = models.ForeignKey(
        "gptconversations.Conversation",
        on_delete=models.CASCADE,
    )

    user_message = models.TextField()

    ai_message = models.TextField()

    # def __str__(self):
    #     return self.name
