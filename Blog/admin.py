from django.contrib import admin
from .models import Post, Comment


class Postadmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'datetime_modified')
    ordering = ['datetime_modified']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment_text', 'post', 'datetime_comment', 'is_active')
    ordering = ['-datetime_comment']


admin.site.register(Post, Postadmin)
admin.site.register(Comment, CommentAdmin)
