from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"


class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"

    def create(self, validated_data):
        if len(validated_data["participants"]) > 2:
            raise ValidationError("Thread can not have more than 2 participants")
        else:
            participants = validated_data.pop("participants")
            threads = Thread.objects.all()

            for participant in participants:
                threads = threads.filter(participants__username=participant)

            if not threads:
                thread = Thread.objects.create(**validated_data)
                thread.participants.set(participants)
                return thread
            return threads[0]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("text",)


class MessageChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("is_read",)
