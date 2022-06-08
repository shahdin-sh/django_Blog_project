from django.shortcuts import redirect, get_object_or_404, render, HttpResponseRedirect
from Blog.models import Post
# from django.views import generic
from django.urls import reverse
from django.urls import reverse_lazy
from .forms import UserCreateForm, UserForm, UserProfilePicForm
# from django.contrib.auth.models import User
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


class UploadUserAvatar(generic.CreateView):
    form_class = UserProfilePicForm
    model = UserProfilePic
    template_name = 'account/upload_user_pic.html'

    def get_success_url(self):
        return reverse('user_profile_view')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdateUserAvatar(generic.UpdateView):
    form_class = UserProfilePicForm
    model = UserProfilePic
    template_name = 'account/update_user_pic.html'

    def get_success_url(self):
        return reverse('user_profile_view')

    def get_object(self, queryset=None):
        pic = get_object_or_404(UserProfilePic.objects.all().filter(user_id=self.request.user.id))
        return pic

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def delete_user_avatar(request):
    current_user_id = request.user.id
    current_user_avatar = get_object_or_404(UserProfilePic.objects.all().filter(user_id=current_user_id))
    if request.method == 'POST':
        current_user_avatar.delete()
        return redirect('user_profile_view')
    return render(request, 'account/delete_current_user_avatar.html', {'current_user_avatar': current_user_avatar})

