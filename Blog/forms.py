from django import forms
from .models import *


class NewPostFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'status']
