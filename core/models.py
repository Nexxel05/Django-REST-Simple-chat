from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name="threads")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.CASCADE
    )
