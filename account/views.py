from django.shortcuts import redirect, get_object_or_404, render
from Blog.models import Post
from django.views import generic
from django.urls import reverse
from django.urls import reverse_lazy
from .forms import UserCreateForm, UserForm, UserProfilePicForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import *


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


@login_required
def user_profile(request):
    current_user_id = request.user.id
    user_post = Post.objects.all().filter(author_id=current_user_id)
    user_pic = UserProfilePic.objects.all().filter(user_id=current_user_id)
    dic = {
        'user_post': len(user_post),
        'user_pic': user_pic,
    }
    return render(request, 'account/user_profile.html', dic)


@login_required
def edit_profile(request):
    current_user_id = request.user.id
    user = User.objects.filter(pk=current_user_id).first()
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile_view')
    else:
        form = UserForm(instance=user)
    return render(request, 'account/edit_profile.html', context={'form': form})


