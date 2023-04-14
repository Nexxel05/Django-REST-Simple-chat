from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User, Thread, Message
from core.serializers import ThreadSerializer


THREAD_CREATE_URL = reverse("core:thread-create")


def user_thread_list_url(user: User) -> str:
    return reverse("core:user-thread-list", args=[user.username])


def user_unread_messages_count_url(user: User) -> str:
    return reverse("core:user-unread-messages-count", args=[user.username])


def thread_delete_url(thread: Thread) -> str:
    return reverse("core:thread-delete", args=[thread])


def thread_message_create_url(thread: Thread) -> str:
    return reverse("core:message-create", args=[thread])


def message_detail_url(message: Message) -> str:
    return reverse("core:message-detail", args=[message])


class UnauthenticatedUser(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = get_user_model().objects.create(
            username="Unauthenticated",
            password="1234qwerty"
        )

    def test_auth_required(self):
        res = self.client.get(user_thread_list_url(self.user))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUser(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = get_user_model().objects.create(
            username="test",
            password="test1234"
        )
        self.client.force_authenticate(self.user)

    def test_user_threads_list(self) -> None:
        thread_with_user = Thread.objects.create()
        thread_with_user.participants.add(self.user)
        thread_without_user = Thread.objects.create()

        serializer_with = ThreadSerializer(thread_with_user)
        serializer_without = ThreadSerializer(thread_without_user)
        res = self.client.get(user_thread_list_url(self.user))

        self.assertEqual(len(res.data), 1)
        self.assertIn(serializer_with.data, res.data)
        self.assertNotIn(serializer_without.data, res.data)

    def test_unread_messages_count(self) -> None:
        thread = Thread.objects.create()
        thread.participants.add(self.user)

        Message.objects.create(
            sender=self.user,
            text="Hello",
            thread=thread,
            is_read=False
        )
        Message.objects.create(
            sender=self.user,
            text="Hello again",
            thread=thread,
            is_read=True
        )

        res = self.client.get(user_unread_messages_count_url(self.user))
        response_str = f"User '{self.user.username}' has 1 unread messages"

        self.assertEqual(res.data, response_str)

    def test_create_thread(self) -> None:
        another_user = get_user_model().objects.create(
            username="user",
            password="user1234"
        )
        data = {
            "participants": [self.user.id, another_user.id]
        }

        res = self.client.post(THREAD_CREATE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["participants"], res.data["participants"])

    def test_return_thread_if_participants_exist(self) -> None:
        threads_before_creation = Thread.objects.count()
        another_user = get_user_model().objects.create(
            username="user",
            password="user1234"
        )
        data = {
            "participants": [self.user.id, another_user.id]
        }
        res = self.client.post(THREAD_CREATE_URL, data)
        self.client.post(THREAD_CREATE_URL, data)
        thread_after_creation = Thread.objects.count()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(threads_before_creation + 1, thread_after_creation)

    def test_delete_thread(self) -> None:
        count_before_creation = Thread.objects.count()
        thread = Thread.objects.create()

        res = self.client.delete(thread_delete_url(thread.id))
        count_after_deletion = Thread.objects.count()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(count_before_creation, count_after_deletion)

    def test_thread_message_create(self) -> None:
        thread = Thread.objects.create()

        data = {
            "sender": self.user.id,
            "text": "This is very unique text",
            "thread": thread,
        }

        res = self.client.post(thread_message_create_url(thread.id), data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["text"], data["text"])

    def test_message_change_status(self) -> None:
        thread = Thread.objects.create()
        message = Message.objects.create(
            thread=thread,
            text="Change status message",
            sender=self.user,
            is_read=False
        )
        data = {"is_read": True}
        res = self.client.put(message_detail_url(message.id), data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, data)
