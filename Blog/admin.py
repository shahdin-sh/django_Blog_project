from django.contrib import admin
from .models import Post, Comment, Favorite


class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'datetime_modified')
    ordering = ['datetime_modified']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'post', 'datetime_comment', 'is_active')
    ordering = ['-datetime_comment']


class FavPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'fav_post')


admin.site.register(Post, Postadmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavPostAdmin)
