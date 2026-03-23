from accounts.models import *
from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password"
        ]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )
        return value

    def validate_username(self, value):

        if len(value) < 3:
            raise serializers.ValidationError(
                "Username must be at least 3 characters"
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists"
            )

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user
    
class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "profile_picture",
            "location",
            "website",
            "created_at",
        ]
        read_only_fields = ["id", "email", "created_at"]
        
class UpdateProfileSerializer(serializers.ModelSerializer):

    profile_picture = serializers.ImageField(required=False)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "bio",
            "profile_picture",
            "profile_picture_url",
            "location",
            "website",
        ]

    def get_profile_picture_url(self, obj):

        request = self.context.get("request")

        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url)

        return None
    
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,min_length=6)
    
    class Meta:
        model = User
        fields = ["old_password","new_password",]
    
    def validate_old_password(self, value):

        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")

        return value
    
class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, attrs):

        self.token = attrs["refresh"]
        return attrs

    def save(self):

        refresh_token = self.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            raise serializers.ValidationError(
                {"detail": "Token is already blacklisted"})
            
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist"
            )

        return value
    
class ResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(min_length=6)
    
class FollowSerializer(serializers.ModelSerializer):

    follower = serializers.CharField(source="follower.username", read_only=True)
    following = serializers.CharField(source="following.username", read_only=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
    
    