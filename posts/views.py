from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import *
from .serializers import *
from accounts .models import *

class CreatePost(GenericAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @extend_schema(
        request=PostSerializer,
        responses=PostSerializer
    )

    def post(self, request):

        serializer = self.get_serializer(data=request.data,context={"request": request})

        if serializer.is_valid():

            post = serializer.save(user=request.user)

            return Response(
                {
                    "message": "Post created successfully",
                    "data": PostSerializer(post).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)
    
class UserPosts(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        posts = Post.objects.filter(user=request.user).order_by("-created_at")
        serializer = self.get_serializer(posts,many=True)
        return Response(
            {
                "count": posts.count(),
                "posts": serializer.data
            }
        )
        
class DeletePosts(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self,request,post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response(
                {"error": "You can delete only your posts"},
                status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(
            {"message": "Post deleted successfully"},
            status=status.HTTP_200_OK)
        
class UpdatePost(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,FormParser)
    
    def put(self,request,post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND)
        if post.user != request.user:
            return Response(
                {"error": "You can update only your posts"},
                status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(post, data=request.data,partial=True)
        if serializer.is_valid():
            image = serializer.validated_data.get("image", post.image)
            video = serializer.validated_data.get("video", post.video)
            if not image and not video:
                return Response(
                    {"error": "Post must contain image or video"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()

            return Response(
                {
                    "message": "Post updated successfully",
                    "data": serializer.data
                }
            )

        return Response(serializer.errors, status=400)
    
class FeedAPI(GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        following_users = Follow.objects.filter(follower=request.user).values_list("following",flat=True)
        posts = Post.objects.filter(user__in=following_users).select_related("user").order_by("-created_at")
        serializer = self.get_serializer(posts, many=True)

        return Response(
            {
                "count": posts.count(),
                "feed": serializer.data
            }
        )
        
class PostLikesView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=404
            )
        like, created = PostLikes.objects.get_or_create(user=request.user,post=post)
        if not created:
            return Response(
                {"message": "Post already liked"},
                status=400
            )
        return Response(
            {"message": "Post liked successfully"}
        )
        
class UnlikePostView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,post_id):
        try:
            like = PostLikes.objects.get(user=request.user,post_id=post_id)
        except PostLikes.DoesNotExist:
            return Response(
                {"error": "Like not found"},
                status=404
            )
        like.delete()
        return Response(
            {"message": "Post unliked successfully"}
        )
        
class TotalLikes(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=404
            )
        likes_count = post.likes.count()
        return Response(
            {
                "post_id": post.id,
                "total_likes": likes_count
            }
        )
        
class PostCommentsView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self,request,post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=404
            )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,post=post)
            return Response(
                {
                    "message": "Comment added successfully",
                    "data": serializer.data
                },
                status=201
            )
        return Response(serializer.errors, status=400)
    
class DeleteCommentView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self,request,comment_id):
        try:
            comment = PostComments.objects.get(id=comment_id)
        except PostComments.DoesNotExist:
            return Response(
                {"error": "Comment not found"},
                status=404
            )
        if comment.user != request.user:
            return Response(
                {"error": "You can delete only your comments"},
                status=403
            )
        comment.delete()
        return Response(
            {"message": "Comment deleted successfully"}
        )
        
class UpdateCommentView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated] 
    
    def put(self,request,comment_id):
        try:
            comment = PostComments.objects.get(id=comment_id)
        except PostComments.DoesNotExist:
            return Response(
                {"error": "Comment not found"},
                status=404
            )
        if comment.user != request.user:
            return Response(
                {"error": "You can update only your comments"},
                status=403
            )
        serializer = self.get_serializer(comment,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Comment updated successfully",
                    "data": serializer.data
                }
            )

        return Response(serializer.errors, status=400)
    
class CommentsonPostView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request,post_id):
        comment = PostComments.objects.filter(post_id=post_id).select_related("user").order_by("-created_at")
        serializer = self.get_serializer(comment,many=True)
        return Response(
            {
                "count": comment.count(),
                "comments": serializer.data
            }
        )
        
class MyPostsComment(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        comments = PostComments.objects.filter(post__user=request.user).select_related("user","post").order_by("-created_at")
        serializer = self.get_serializer(comments,many=True)
        return Response(
            {
                "count": comments.count(),
                "comments": serializer.data
            }
        )
        
       

