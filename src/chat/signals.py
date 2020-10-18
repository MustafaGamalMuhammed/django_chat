from django.contrib.auth.models import User
from django.db.models.signals import post_save
from chat.models import Profile


def create_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)  


post_save.connect(create_profile, sender=User)