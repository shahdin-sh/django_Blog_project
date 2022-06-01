from django import forms
from .models import *
from django.contrib.auth.models import User


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', 'recommended']


class FavoritePostForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['fav_post', 'user']


class NoneLoginUserCommentForm(forms.ModelForm):
    class Meta:
        model = NoneUserComment
        fields = ['name', 'email', 'comment_text', 'recommended']
