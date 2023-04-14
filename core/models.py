from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name="threads")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            "Participants: "
            f"{[user.username for user in self.participants.all()]}"
        )


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.CASCADE
    )
    text = models.TextField()
    thread = models.ForeignKey(
        Thread,
        related_name="messages",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        return (
            f"From {self.sender.username} "
            f"on {self.created.strftime('%d/%m/%Y %H:%M:%S')}"
        )
