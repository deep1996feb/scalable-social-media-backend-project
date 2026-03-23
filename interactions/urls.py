from django.urls import path, include
from .views import *
urlpatterns = [
    path("chat/<int:room_id>/messages/", ChatHistoryAPI.as_view()),
    path("chat/start/", StartChatView.as_view()),
    path("chat/<int:room_id>/seen/", MarkSeenView.as_view()),
    path("chat/unread/<int:room_id>/",UnreadCoversation.as_view()),
    path("chat/inbox/",ChatInboxView.as_view()),
]