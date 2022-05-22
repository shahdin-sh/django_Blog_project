from django import forms
from .models import *


class NewPostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'status', 'favorite']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', 'recommended']


class FavoritePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['favorite']