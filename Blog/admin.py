from django.contrib import admin
from .models import Post, Comment, Favorite


class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date_created', 'author', 'image_post', 'comments')
    ordering = ['-date_created']

    def comments(self, obj):
        comment = Comment.objects.all().filter(post_id=obj.id)
        return f'{len(comment)}'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_or_replay', 'comment_text', 'post', 'datetime_comment',
                    'is_active', 'user', 'name', 'email',  'likes', 'parent')
    ordering = ['-datetime_comment']

    def likes(self, obj):
        if obj.user_likes.exists():
            return len(obj.user_likes.all())
        else:
            return '0'

    def comment_or_replay(self, obj):
        if obj.parent:
           return f'Children of Comment {obj.parent.id}'
        else:
            return f'Comment {obj.id}'


class FavPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'fav_post')


# registering Datas in admin panel
admin.site.register(Post, Postadmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavPostAdmin)