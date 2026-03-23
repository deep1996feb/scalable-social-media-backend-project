from django.urls import path
from .views import *

urlpatterns = [
    path("notifications/", NotificatonListView.as_view()),
    path("notifications/unread-count/", UnreadNotificationCountAPI.as_view()),
    path("notifications/<int:pk>/read/",MarkNotificationReadView.as_view()),
    path("notifications/read-all/",MarkAllNotificationReadAPI.as_view()),
]