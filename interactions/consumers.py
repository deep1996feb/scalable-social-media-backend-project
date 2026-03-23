import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Messages
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from jwt import decode as jwt_decode
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        query_string = self.scope["query_string"].decode()
        params = parse_qs(query_string)

        token = params.get("token")

        if token:
            user = await self.get_user_from_token(token[0])
            self.scope["user"] = user
        else:
            self.scope["user"] = AnonymousUser()

        print("USER:", self.scope["user"])

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):

        data = json.loads(text_data)
        message = data["message"]

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.scope["user"].username
            }
        )


    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "sender": event["sender"]
            })
        )


    @database_sync_to_async
    def save_message(self, message):

        user = self.scope["user"]

        print("SAVING MESSAGE:", message)
        print("USER:", user)
        print("USER ID:", user.id)
        print("AUTH:", user.is_authenticated)
        
        if not user.is_authenticated:
            print("User not authenticated. Message not saved.")
            return

        room = ChatRoom.objects.get(id=self.room_id)

        return Messages.objects.create(
            room=room,
            sender_id=user.id,
            message=message
        )
        
    @database_sync_to_async
    def get_user_from_token(self, token):

        try:
            decoded = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = get_user_model().objects.get(id=decoded["user_id"])
            return user
        except:
            return AnonymousUser()