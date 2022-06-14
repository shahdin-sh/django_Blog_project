from .models import UserProfilePic
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_pic']


admin.site.register(UserProfilePic, UserProfileAdmin)
