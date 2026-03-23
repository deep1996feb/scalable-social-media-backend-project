import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import UserStatus
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

class StatusConsumer(AsyncWebsocketConsumer):
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

        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.set_user_online(True)
        await self.accept()


    async def disconnect(self, close_code):

        if self.scope["user"].is_authenticated:
            await self.set_user_online(False)


    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return get_user_model().objects.get(id=decoded["user_id"])
        except Exception:
            return AnonymousUser()


    @database_sync_to_async
    def set_user_online(self, status):

        user = self.scope["user"]

        UserStatus.objects.update_or_create(
            user=user,
            defaults={
                "is_online": status,
                "last_seen": timezone.now()
            }
        )