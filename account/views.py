from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import UserForm
from django.contrib.auth.models import User


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


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
