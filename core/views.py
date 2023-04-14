from rest_framework import viewsets, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.models import Thread, Message
from core.serializers import (
    ThreadSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    MessageChangeStatusSerializer,
    ThreadCreateSerializer,
)


class ThreadCreateView(
    generics.CreateAPIView
):
    """
    Thread creation or retrieve if a thread with particular users exist.
    """
    serializer_class = ThreadCreateSerializer


class ThreadDeleteView(generics.RetrieveDestroyAPIView):
    """
    Retrieving and deletion thread
    """
    model = Thread
    serializer_class = ThreadSerializer

    def get_object(self):
        return Thread.objects.get(id=self.kwargs["pk"])


class UserThreadListView(generics.ListAPIView):
    """
    Retrieving the list of threads for any user
    """
    serializer_class = ThreadSerializer

    def get_queryset(self):
        return Thread.objects.filter(
            participants__username=self.kwargs["username"]
        )


@api_view(["GET"])
def user_unread_messages_count(request, username):
    """
    Retrieving a number of unread messages for the user
    """
    unread_messages_count = Message.objects.filter(
        sender__username=username,
        is_read=False
    ).count()
    return Response(
        f"User '{username}' has {unread_messages_count} unread messages"
    )


class ThreadMessageCreateView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    """
    Creation of a message and retrieving message list for the thread
    """
    model = Message

    def get_serializer_class(self) -> Serializer:
        serializer_dict = {
            "list": MessageSerializer,
            "create": MessageCreateSerializer
        }
        return serializer_dict.get(self.action, MessageSerializer)

    def get_queryset(self) -> Message:
        return Message.objects.filter(thread__id=self.kwargs["pk"])

    def perform_create(self, serializer: Serializer) -> None:
        thread = Thread.objects.get(id=self.kwargs["pk"])
        serializer.save(
            sender=self.request.user,
            thread=thread
        )


class MessageDetailChangeStatusView(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    """
    Retrieve message detail or marking the message as read
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_serializer_class(self):
        serializer_dict = {
            "retrieve": MessageSerializer,
            "update": MessageChangeStatusSerializer
        }
        return serializer_dict.get(self.action)
