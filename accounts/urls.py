from django.urls import path, include
from .views import *
urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginView.as_view()),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/update/", UpdateProfileView.as_view(), name="update-profile"),
    path("change-password/", ChangePasswordView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("reset-password/<uidb64>/<token>/",ResetPasswordView.as_view()),
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow-user"),
    path("followers/", FollowersListView.as_view(), name="followers-list"),
    path("following/", FollowingListView.as_view(), name="following-list"),
]
