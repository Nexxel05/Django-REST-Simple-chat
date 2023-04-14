from django.urls import path

from core.views import (
    ThreadCreateView,
    ThreadDeleteView,
    UserThreadListView,
    ThreadMessageCreateView,
    user_unread_messages_count,
    MessageDetailChangeStatusView
)

thread_messages = ThreadMessageCreateView.as_view(
    actions={
        "get": "list",
        "post": "create"
    }
)

messages = MessageDetailChangeStatusView.as_view(
    actions={
        "get": "retrieve",
        "put": "update"
    }
)

urlpatterns = [
    path(
        "user/<str:username>/thread/",
        UserThreadListView.as_view(),
        name="user-thread-list"
    ),
    path(
        "user/<str:username>/message/",
        user_unread_messages_count,
        name="user-unread-messages-count"
    ),
    path(
        "thread/create/",
        ThreadCreateView.as_view(),
        name="thread-create"
    ),
    path(
        "thread/delete/<int:pk>/",
        ThreadDeleteView.as_view(),
        name="thread-delete"
    ),
    path(
        "thread/<int:pk>/message/",
        thread_messages,
        name="message-create"
    ),
    path(
        "message/<int:pk>/",
        messages,
        name="message-detail"
    )

]

app_name = "core"
