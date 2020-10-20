from django.db import models 
from django.contrib.auth.models import User
from django.core.cache import cache 
from django.conf import settings
import datetime
from src import settings
from PIL import Image
import random


class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", default="default.jpg", blank=True, null=True)

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
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

    def update_image(self, image):
        _x = list(range(0, 10)) + 'A a B b C c D d E e F f G g H h I i J j K k L l M m N n O o P p Q q R r S s T t U u V v W w X x Y y Z z'.split(' ')
        _x = [str(item) for item in _x]
        random.shuffle(_x)

        im = Image.open(image)
        im_name = f"{''.join(_x)[:20]}.{im.tile[0][0]}"
        width, height = im.size
        
        if width > 200 or height > 200:
            im.thumbnail((200, 200), Image.ANTIALIAS)
            
        im.save(settings.BASE_DIR/f'media/profile_pics/{im_name}')
        self.image = f"profile_pics/{im_name}"

        self.save()
