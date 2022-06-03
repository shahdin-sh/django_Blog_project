from .models import UserProfile
from django.contrib import admin


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_pic', )


admin.site.register(UserProfile, UserProfileAdmin)
