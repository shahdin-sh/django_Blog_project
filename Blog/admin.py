from django.contrib import admin
from .models import Post, Comment, Favorite


class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date_created', 'author', 'image_post')
    ordering = ['-date_created']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'post', 'datetime_comment', 'is_active', 'user', 'name', 'email', 'likes')
    ordering = ['-datetime_comment']

    def likes(self, obj):
        if obj.user_likes.exists():
            return len(obj.user_likes.all())
        else:
            return '0'


class FavPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'fav_post')

# registering Datas in admin panel
admin.site.register(Post, Postadmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavPostAdmin)
