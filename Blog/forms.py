from django import forms
from .models import *
from django.contrib.auth.models import User


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'status', 'image_post']

    def __init__(self, *args, **kwargs,):
        super(NewPostForm, self).__init__(*args, **kwargs)
        if self.initial['status'] == 'drf':
            self.fields['status'].widget = forms.HiddenInput()


class DraftPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('title', 'text', 'author', 'status', 'image_post')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']


class NoneUserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment_text']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('this email has given before!')
        else:
            return email


class FavoritePostForm(forms.ModelForm):
    class Meta:
        model = Favorite
        exclude = ('fav_post', 'user',)