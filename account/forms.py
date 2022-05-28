from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name",
                  "email", "username", "password1", "password2")
        for i in fields:
            help_texts = {
                'i': None
            }
