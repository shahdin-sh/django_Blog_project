from django.shortcuts import redirect, get_object_or_404, render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.urls import reverse_lazy
from .forms import UserCreateForm, UserForm, UserProfilePicForm
from Blog.models import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import *
from django.contrib.auth.models import User


class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        data = super(SignUpView, self).get_context_data(*args, **kwargs)
        data['page_title'] = 'Sign In'
        return data

    def form_valid(self, form):
        user = form.save()
        UserProfilePic.objects.create(user=user)
        return redirect(self.success_url)


@login_required
def user_profile(request):
    current_user_id = request.user.id
    # user posts, favorite posts, draft inbox and user profile avatar for showing in profile section!
    user_post = Post.objects.all().filter(author_id=current_user_id)
    user_fav_post = Favorite.objects.all().filter(user_id=current_user_id)
    user_draft_inbox = Post.objects.all().filter(author_id=current_user_id, status='drf')
    user_pic = UserProfilePic.objects.all().filter(user_id=current_user_id)
    page_title = 'Profile'
    dic = {
        'user_post': len(user_post),
        'user_fav_post': len(user_fav_post),
        'user_draft_inbox': len(user_draft_inbox),
        'user_pic': user_pic,
        'page_title': page_title,
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
    page_title = 'Edit Profile'
    return render(request, 'account/edit_profile.html', context={'form': form,
                                                                 'page_title': page_title})


class UpdateUserAvatar(generic.UpdateView):
    form_class = UserProfilePicForm
    model = UserProfilePic
    template_name = 'account/update_user_pic.html'

    def get_success_url(self):
        return reverse('user_profile_view')

    def get_object(self, queryset=None):
        pic = get_object_or_404(UserProfilePic.objects.all().filter(user_id=self.request.user.id))
        return pic

    def get_context_data(self, *args, **kwargs):
        data = super(UpdateUserAvatar, self).get_context_data(*args, **kwargs)
        data['page_title'] = 'Edit User Pic'
        return data


@login_required
def delete_user_avatar(request):
    # limiting accesses to the delete section for users who don't have profile picture
    try:
        user = request.user
        user_avatar = user.userprofilepic.profile_pic.url
        if user_avatar:
            current_user_id = request.user.id
            current_user_avatar = get_object_or_404(UserProfilePic.objects.all().filter(user_id=current_user_id))
            if request.method == 'POST':
                current_user_avatar.profile_pic.delete()
                return redirect('user_profile_view')
            page_title = 'Delete Avatar'
            return render(request, 'account/delete_current_user_avatar.html', {'current_user_avatar': current_user_avatar,
                                                                               'page_title': page_title})
    except ValueError:
        raise Http404()

