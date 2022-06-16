from django.contrib import admin
from .models import Post, Comment, Favorite


class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date_created', 'author')
    ordering = ['-date_created']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'post', 'datetime_comment', 'is_active', 'user', 'name', 'email')
    ordering = ['-datetime_comment']


class FavPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'fav_post')


admin.site.register(Post, Postadmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavPostAdmin)
