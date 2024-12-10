import base64
import json
import secrets
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.base import ContentFile

from users.models import CustomUser as User

from .models import Conversation, Message
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        text_data_json = json.loads(text_data_json)

        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        await self.channel_layer.group_send(self.room_group_name, return_dict)

    async def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        message = text_data_json["message"]
        attachment = text_data_json.get("attachment")
        conversation = await database_sync_to_async(Conversation.objects.get)(
            id=int(self.room_name)
        )

        sender = self.scope["user"]

        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]

            file_data = ContentFile(
                base64.b64decode(file_str, name=f"{secrets.token_hex(8)}.{file_ext}")
            )

            _message = await database_sync_to_async(Message.objects.create)(
                sender=sender,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
            )
        else:
            _message = await database_sync_to_async(Message.objects.create)(
                sender=sender, text=message, conversation_id=conversation
            )
        serializer = MessageSerializer(instance=_message)
        await self.send(text_data=json.dumps(serializer.data))
