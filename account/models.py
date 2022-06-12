from django.db import models
from django.contrib.auth.models import User


class UserProfilePic(models.Model):
    profile_pic = models.ImageField(upload_to='profile/', default='profile/img_avatar.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} profile pic'

