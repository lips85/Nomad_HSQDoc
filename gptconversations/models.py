from django.db import models
from common.models import CommonModel


# Create your models here.
class Conversation(CommonModel):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    pdf = models.FileField()

    # def __str__(self):
    #     return self.name
