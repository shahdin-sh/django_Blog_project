from .models import UserProfilePic
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_pic', 'profile_pic_status']

    def profile_pic_status(self, obj):
        try:
            return obj.profile_pic.url
        except ValueError:
            return f'no avatar for {obj.user}'


admin.site.register(UserProfilePic, UserProfileAdmin)
