from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    content = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at}:{self.user.username}:{self.content[:100]}"
