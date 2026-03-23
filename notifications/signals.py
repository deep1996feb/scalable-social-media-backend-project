from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import *
from .models import *
from accounts.models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from accounts.models import *

@receiver(post_save, sender=PostLikes)

def like_notifications(sender,instance,created, **kwargs):
        if created:
            Notification.objects.create(
                sender=instance.user,
                receiver=instance.post.user,
                post = instance.post,
                notification_type="like"
            )
        
@receiver(post_save, sender=PostComments)

def comment_notifications(sender,instance,created, **kwargs):
    
        if created:
            Notification.objects.create(
                sender=instance.user,
                receiver=instance.post.user,
                post = instance.post,
                notification_type="comment"
            )
        
@receiver(post_save, sender=Follow)

def follow_notifications(sender,instance,created, **kwargs):
    if created and instance.follower != instance.following:
        if created:
            Notification.objects.create(
                sender=instance.follower,
                receiver=instance.following,
                notification_type="follow"
            )
            
@receiver(post_save, sender=PostLikes)
def like_notifications(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.user,
            post=instance.post,
            notification_type="like"
        )

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "test_notifications",   # 👈 same group name
            {
                "type": "send_notification",
                "message": f"{instance.user.username} liked your post"
            }
        )
        
@receiver(post_save, sender=PostComments)
def comment_notifications(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            sender=instance.user,
            receiver=instance.post.user,
            post=instance.post,
            notification_type="comment"
        )

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "test_notifications",
            {
                "type": "send_notification",
                "message": f"{instance.user.username} commented on your post"
            }
        )
        
@receiver(post_save, sender=Follow)
def follow_notifications(sender, instance, created, **kwargs):

    if created:

        Notification.objects.create(
            sender=instance.follower,
            receiver=instance.following,
            notification_type="follow"
        )

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "test_notifications",
            {
                "type": "send_notification",
                "message": f"{instance.follower.username} started following you"
            }
        )
        
