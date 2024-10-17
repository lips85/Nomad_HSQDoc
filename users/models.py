from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(
        max_length=150,
        default="",
    )
    last_name = models.CharField(
        max_length=150,
        default="",
    )
    # name = models.CharField(
    #     max_length=150,
    #     default="",
    # )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default="",
    )
