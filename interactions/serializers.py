from rest_framework import serializers
from .models import *

class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.CharField(source="sender.username")

    class Meta:
        model = Messages
        fields = ["id","sender","message","created_at"]
        
class StartChatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    