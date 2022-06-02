from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class Post(models.Model):
    STATUS_CHOICES = (
        ('pub', 'published'),
        ('drf', 'draft'),
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail_view', args=[self.id])


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200, null=True)
    comment_text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    datetime_comment = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    recommended = models.BooleanField(default=True)

    def __str__(self):
        return self.comment_text


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fav_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='fav_post')

