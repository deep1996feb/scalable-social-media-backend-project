from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .pagination import NotificationPagination
from .models import Notification
from .serializers import NotificationSerializer
# Create your views here.

class NotificatonListView(GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination
    
    def get(self,request):
        notifications = Notification.objects.filter(receiver=request.user).select_related("sender").order_by("-created_at")
        serializer = self.get_serializer(notifications,many=True)
        return Response(serializer.data)
    
class UnreadNotificationCountAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        count = Notification.objects.filter(receiver=request.user,is_read=False).count()
        return Response(
            {
                "unread_count": count
            }
        )
        
class MarkNotificationReadView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self,request,pk):
        notification = get_object_or_404(Notification,id=pk,receiver=request.user)
        notification.is_read =True
        notification.save()
        
        return Response(
            {"message": "Notification marked as read"},
            status=status.HTTP_200_OK
        )
        
class MarkAllNotificationReadAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self,request):
        Notification.objects.filter(receiver=request.user,is_read=False).update(is_read=True)
        return Response(
            {"message": "All notifications marked as read"}
        )
        
