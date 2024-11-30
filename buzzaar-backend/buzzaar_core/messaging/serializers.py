from users.serializers import CustomUserSerializer
from .models import Conversation, Message

from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('conversation_id',)

class ConversationListSerializer(serializers.ModelSerializer):
    initiator_id = serializers.IntegerField(read_only=True)
    receiver_id = serializers.IntegerField(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['initiator_id', 'receiver_id', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message)

class ConversationSerializer(serializers.ModelSerializer):
    initiator_id = serializers.IntegerField(read_only=True)
    receiver_id = serializers.IntegerField(read_only=True)
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Conversation
        fields = ['initiator_id', 'receiver_id', 'message_set']
