from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from accounts .models import *
from django.db.models import Q
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

User = get_user_model()

# Create your views here.

class ChatHistoryAPI(GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request,room_id):
        messages = Messages.objects.filter(room_id=room_id).order_by("created_at")

        serializer = self.get_serializer(messages, many=True)

        return Response(serializer.data)

class StartChatView(APIView):
    @extend_schema(request=StartChatSerializer)
    def post(self, request):

        serializer = StartChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user1 = request.user
        user2_id = serializer.validated_data["user_id"]

        user2 = User.objects.get(id=user2_id)

        room = ChatRoom.objects.filter(
            Q(user1=user1, user2=user2) |
            Q(user1=user2, user2=user1)
        ).first()

        if not room:
            room = ChatRoom.objects.create(user1=user1, user2=user2)

        return Response({"room_id": room.id})
    
class MarkSeenView(APIView):
    
    def post(self,request,room_id):
        Messages.objects.filter(room_id=room_id,is_seen=False).exclude(sender=request.user).update(is_seen=True)
        return Response({"message":"Message marked as seen"})
    
class UnreadCoversation(APIView):
    
    def get(self, request, room_id):
        count = Messages.objects.filter(
            room_id=room_id,
            is_seen=False
        ).exclude(sender=request.user).count()

        return Response({"unread_count": count})
    
class ChatInboxView(APIView):
    def get(self,request):
        user = request.user
        rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
        data = []
        for room in rooms:
            last_msg = Messages.objects.filter(room=room).order_by("-created_at").first()
            if room.user1 == user:
                other_user = room.user2
            else:
                other_user = room.user1
            unread = Messages.objects.filter(
                room=room,
                is_seen=False
            ).exclude(sender=user).count()

            data.append({
                "room_id": room.id,
                "user": other_user.username,
                "last_message": last_msg.message if last_msg else "",
                "unread": unread
            })

        return Response(data)
        
    
    

        
