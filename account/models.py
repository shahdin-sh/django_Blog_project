from django.db import models
from django.contrib.auth import get_user_model


class UserProfilePic(models.Model):
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} profile avatar'

    def get_user_profile_image(self):
        try:
            return self.profile_pic.url
        except ValueError:
            return '/media/default/img_avatar.png'
