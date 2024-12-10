from rest_framework import serializers

from users.serializers import CustomUserSerializer

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ("conversation_id",)


class ConversationListSerializer(serializers.ModelSerializer):
    initiator_id = serializers.IntegerField(read_only=True)
    receiver_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "initiator_id", "receiver_id"]


class ConversationSerializer(serializers.ModelSerializer):
    initiator_id = serializers.IntegerField(read_only=True)
    receiver_id = serializers.IntegerField(read_only=True)
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ["id", "initiator_id", "receiver_id", "message_set"]
