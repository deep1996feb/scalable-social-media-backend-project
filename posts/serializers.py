from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )
    image = serializers.FileField(required=False)
    video = serializers.FileField(required=False)
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Post
        fields = [
            "id",
            "username",
            "caption",
            "image",
            "video",
        ]

    def validate(self, data):

        image = data.get("image")
        video = data.get("video")

        if not image and not video:
            raise serializers.ValidationError(
                "Post must contain either image or video"
            )

        return data
    
    def get_profile_picture_url(self, obj):

        request = self.context.get("request")

        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url)

        return None
    
class PostSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    likes_count = serializers.IntegerField(
        source="likes.count",
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "username",
            "caption",
            "image",
            "video",
            "likes_count"
        ]
        
class CommentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    created_at = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M",
        read_only=True
    )

    class Meta:
        model = PostComments
        fields = [
            "id",
            "username",
            "comment",
            "created_at"
        ]

    def validate_comment(self, value):

        if len(value.strip()) == 0:
            raise serializers.ValidationError(
                "Comment cannot be empty"
            )

        if len(value) > 300:
            raise serializers.ValidationError(
                "Comment too long"
            )

        return value