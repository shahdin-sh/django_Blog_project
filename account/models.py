from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserProfilePic(models.Model):
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True, auto_created=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, auto_created=True)

    def __str__(self):
        return f'{self.user} profile pic'

