from django import forms
from .models import *


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'status']


class DraftPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('title', 'text', 'author', 'status')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', 'recommended']


class FavoritePostForm(forms.ModelForm):
    class Meta:
        model = Favorite
        exclude = ('fav_post', 'user',)

