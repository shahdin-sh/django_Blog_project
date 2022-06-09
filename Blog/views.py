from django.shortcuts import redirect, get_object_or_404, render, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.core.paginator import Paginator
from account.models import UserProfilePic


def post_list_view(request):
    post = Post.objects.all().order_by('-date_created')
    paginator = Paginator(post, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # get user profile pic
    user_pic = UserProfilePic.objects.all()
    # dic
    dic = {
        'post': page_obj,
        'user_pic': user_pic,
    }
    return render(request, 'blog/post_list.html', dic)


def post_detail_view(request, pk):
    # post with its pk or id.
    post_detail = get_object_or_404(Post, pk=pk)
    # comments section.
    comments = post_detail.comments.all().order_by('-datetime_comment')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post_detail
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    # favorite post Backend for login users.
    if request.method == 'POST':
        fav_form = FavoritePostForm(request.POST)
        if fav_form.is_valid():
            new_fav = fav_form.save(commit=False)
            new_fav.user = request.user
            new_fav.fav_post = post_detail
            fav_form.save()
            fav_form = FavoritePostForm()
            return redirect('post_detail_view', pk)
    else:
        fav_form = FavoritePostForm()
    user_fav_post_check = Favorite.objects.all().filter(user_id=request.user.id, fav_post_id=pk)
    # a dictionary as a context
    dic = {
        'post_detail': post_detail,
        'comments': comments,
        'comment_form': comment_form,
        'fav_form': fav_form,
        'fav': user_fav_post_check
    }
    # rendering the request.
    return render(request, 'blog/post_detail.html', dic)


class PostCreatView(generic.CreateView):
    form_class = NewPostForm
    template_name = 'blog/add_post.html'

    def get_success_url(self):
        return reverse('post_detail_view', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'blog/add_post.html'

    def get_success_url(self):
        return reverse('post_detail_view', kwargs={'pk': self.object.pk})

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        return reverse('post_view_of_blog')


@login_required
def comment_update_view(request, pk, comment_id):
    auth = 0
    auth_check = Comment.objects.all().filter(user_id=request.user.id)
    for i in auth_check:
        if i.pk == comment_id:
            auth = i.pk
    if auth != 0:
        post = get_object_or_404(Post, pk=pk)
        comment = get_object_or_404(post.comments.all().filter(pk=comment_id))
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail_view', pk)
        return render(request, 'blog/comment_update_view.html', {'form': form})
    else:
        raise Http404()


@login_required
def comment_delete_view(request, pk, comment_id):
    auth = 0
    auth_check = Comment.objects.all().filter(user_id=request.user.id)
    for i in auth_check:
        if i.pk == comment_id:
            auth = i.pk
    if auth != 0:
        post = get_object_or_404(Post, pk=pk)
        comment = get_object_or_404(post.comments.all().filter(pk=comment_id))
        if request.method == 'POST':
            comment.delete()
            return redirect('post_detail_view', pk)
        return render(request, 'blog/comment_delete_view.html', {'comment': comment,
                                                                 'post': post})
    else:
        raise Http404()


def user_posts_view(request):
    current_user = request.user.id
    post_bool = Post.objects.all().filter(author=current_user).exists()
    posts_pg = Post.objects.all().filter(author=current_user).order_by('-date_created')
    paginator = Paginator(posts_pg, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # get user profile pic
    user_pic = UserProfilePic.objects.all()
    dic = {'user_posts_auth': post_bool,
           'post': page_obj,
           'user_pic': user_pic
           }
    return render(request, 'blog/user_posts_view.html', dic)


def user_fav_view(request):
    current_user = request.user.id
    user_fav_post = Post.objects.all().filter(fav_post__user_id=current_user).order_by('-date_created')
    paginator = Paginator(user_fav_post, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # get user profile pic
    user_pic = UserProfilePic.objects.all()
    dic = {
        'user_fav_post': page_obj,
        'user_pic': user_pic,
    }
    return render(request, 'blog/user_fav_posts_view.html', dic)


def delete_fav_user_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    current_user = request.user.id
    fav_user_post = Favorite.objects.all().filter(user_id=current_user, fav_post_id=pk)
    if request.method == 'POST':
        fav_user_post.delete()
        return redirect('post_detail_view', pk)
    dic = {
        'fav_user_post': fav_user_post,
        'post': post
    }
    return render(request, 'blog/remove_fav_user_post.html', dic)

