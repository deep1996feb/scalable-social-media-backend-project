from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
# Create your views here.

class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )
        return Response(serializer.errors)
    
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(username=user.username, password=password)

        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        })
        
class ProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.get_serializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateProfileView(GenericAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser)  
    @swagger_auto_schema(
        request_body=UpdateProfileSerializer,
        consumes=["multipart/form-data"]
    )
    
    def put(self,request):
        user = request.user
        serializer = self.get_serializer(user,data=request.data,partial=True,context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Profile updated successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
        
class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )
        
class LogoutView(GenericAPIView):

    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Logout successful"
            },
            status=status.HTTP_200_OK
        )
        
class ForgotPasswordView(GenericAPIView):

    serializer_class = ForgotPasswordSerializer

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"http://127.0.0.1:8000/api/reset-password/{uid}/{token}/"

        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_link}",
            "noreply@example.com",
            [email],
            fail_silently=False
        )

        return Response(
            {"message": "Password reset link sent to email"},
            status=status.HTTP_200_OK
        )
        
class ResetPasswordView(GenericAPIView):

    serializer_class = ResetPasswordSerializer
    # permission_classes = [AllowAny]

    def post(self, request, uidb64, token):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            print("UIDB64:", uidb64)

            uid = force_str(urlsafe_base64_decode(uidb64))

            print("Decoded UID:", uid)

            user = User.objects.get(pk=uid)

        except Exception as e:

            print("ERROR:", e)

            return Response(
                {"error": "Invalid user"},
                status=400
            )

        if not PasswordResetTokenGenerator().check_token(user, token):

            return Response(
                {"error": "Invalid or expired token"},
                status=400
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"message": "Password reset successful"}
        )
        
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'},status=status.HTTP_404_NOT_FOUND)
        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself'},status=status.HTTP_400_BAD_REQUEST)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            follow.delete()
            return Response({'message': 'User Unfollowed'},status=status.HTTP_200_OK)
        return Response(
            {"message": "User followed"},
            status=status.HTTP_201_CREATED
        )
        
class FollowersListView(generics.ListAPIView):

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)
    
class FollowingListView(generics.ListAPIView):

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

        
        