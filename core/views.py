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
    serializer_class = ThreadCreateSerializer


class ThreadDeleteView(generics.RetrieveDestroyAPIView):
    model = Thread
    serializer_class = ThreadSerializer

    def get_object(self):
        return Thread.objects.get(id=self.kwargs["pk"])


class UserThreadListView(generics.ListAPIView):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        return Thread.objects.filter(
            participants__username=self.kwargs["username"]
        )


@api_view(["GET"])
def user_unread_messages_count(request, username):
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
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_serializer_class(self):
        serializer_dict = {
            "retrieve": MessageSerializer,
            "update": MessageChangeStatusSerializer
        }
        return serializer_dict.get(self.action)
