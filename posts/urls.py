from django.urls import path, include
from .views import *

urlpatterns = [
    path("create-post/", CreatePost.as_view(), name="create-post"),
    path("my-posts/", UserPosts.as_view()),
    path("delete-post/<int:post_id>/", DeletePosts.as_view()),
    path("update-post/<int:post_id>/", UpdatePost.as_view()),
    path("feed/", FeedAPI.as_view()),
    path("like/<int:post_id>/", PostLikesView.as_view()),
    path("unlike/<int:post_id>/", UnlikePostView.as_view()),
    path("total-likes/<int:post_id>/", TotalLikes.as_view()),
    path("add-comment/<int:post_id>/", PostCommentsView.as_view()),
    path("delete-comment/<int:comment_id>/", DeleteCommentView.as_view()),
    path("update-comment/<int:comment_id>/", UpdateCommentView.as_view()),
    path("post-comments/<int:post_id>/", CommentsonPostView.as_view()),
    path("my-posts-comments/",MyPostsComment.as_view(),
),
]