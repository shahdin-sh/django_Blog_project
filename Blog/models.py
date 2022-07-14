from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from account.models import UserProfilePic
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Post(models.Model):
    STATUS_CHOICES = (
        ('pub', 'published'),
        ('drf', 'draft'),
    )
    title = models.CharField(max_length=100)
    text = RichTextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)
    image_post = models.ImageField(upload_to='post_pic/', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail_view', args=[self.id])

    def get_each_post_author_profile_image(self):
        try:
            return self.author.userprofilepic.profile_pic.url
        except ValueError:
            return '/media/default/img_avatar.png'


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    comment_text = models.CharField(null=True, max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    datetime_comment = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    # this section is for comments(replies) that they are inside the main comment or their parent
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    user_likes = models.ManyToManyField(get_user_model(), blank=True, related_name='liked_comments_by_user')
    # showing how many users like the particular comment

    def get_likes(self):
        return self.user_likes.count()

    def __str__(self):
        return self.comment_text

    def get_each_post_user_profile_image(self):
        try:
            if self.user:
                return self.user.userprofilepic.profile_pic.url
        except ValueError:
            return '/media/default/img_avatar.png'
        if self.name not in UserProfilePic.objects.all():
            return '/media/default/img_avatar.png'


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fav_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='fav_post')
