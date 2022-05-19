from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .forms import UserForm, UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


def signup_view(request):
    form = UserCreateForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('post_view_of_blog')
    return render(request, 'registration/signup.html', {'form': form})


def profile(request):
    current_user_id = request.user.id
    user = User.objects.filter(pk=current_user_id).first()
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('post_view_of_blog')
    else:
        form = UserForm(instance=user)
    return render(request, 'account/showing_users.html', context={'form': form})
