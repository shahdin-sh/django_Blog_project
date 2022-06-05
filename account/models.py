from django.contrib.auth import get_user_model
from django.db import models


class UserProfilePic(models.Model):
    profile_pic = models.ImageField(upload_to='profile/', blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} profile pic'
