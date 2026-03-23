from django.db import models
from django.conf import settings
# Create your models here.

class UserStatus(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True,blank=True)
