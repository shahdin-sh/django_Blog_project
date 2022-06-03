from django.contrib.auth import get_user_model
from django.db import models


class UserProfilePic(models.Model):
    profile_pic = models.ImageField(upload_to='profile/')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
