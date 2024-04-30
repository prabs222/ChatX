from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import Message, Room

User = get_user_model()

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_user = self.scope['user']
        if request_user.is_authenticated:
            room = self.scope['url_route']['kwargs']['id']
            self.room_group_name = f"chat_{room}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        id = data.get('id', None)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "id": id
            }
        )
        await self.save_message_to_db(id, self.room_group_name, message)

    async def chat_message(self, event):
        message = event['message']
        id = event['id']
        await self.send(text_data=json.dumps({
            "message":message,
            "id":id
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message_to_db(self, user_id, chat_room_id, message):
        room_id = chat_room_id.split('_')[1]
        user = User.objects.get(id=user_id)
        room = Room.objects.get(id=room_id)
        
        chat_obj = Message.objects.create(user=user, room=room, message=message)