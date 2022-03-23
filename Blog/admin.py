from django.contrib import admin
from .models import Post

# Register your models here.


class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'datetime_modified')
    ordering = ['datetime_modified']

# register means displaying on the screen.
admin.site.register(Post, Postadmin)
