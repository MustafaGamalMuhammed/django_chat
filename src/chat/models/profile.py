from django.db import models 
from django.contrib.auth.models import User
from django.core.cache import cache 
import datetime
from src import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen:
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                        seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False 

    def __str__(self):
        return f"{self.user.username}'s profile"