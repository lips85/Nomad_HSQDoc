from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    first_name = models.CharField(
        max_length=150,
        default="",
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        default="",
        blank=True,
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
