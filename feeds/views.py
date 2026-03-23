from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from posts.models import *
from posts.serializers import *
from accounts .models import *
from .pagination import FeedPagination
from django.db.models import Q
# Create your views here.

class UserFeedView(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FeedPagination
    
    def get(self,request):
        following_users = Follow.objects.filter(follower=request.user).values_list("following",flat=True)
        posts = Post.objects.filter(Q(user__in=following_users) | Q(user=request.user)).select_related("user").order_by("-created_at")
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts,request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
