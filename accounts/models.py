from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
User = settings.AUTH_USER_MODEL

class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profiles/",null=True,blank=True)
    location = models.CharField(max_length=100, null=True,blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE,related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"
