from django.contrib import admin
from chat import models
# Register your models here.

admin.site.register([
    models.Room, 
    models.Message, 
    models.Contact, 
    models.FriendRequest,
    models.Profile])