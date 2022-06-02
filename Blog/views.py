from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.models import User


def post_list_view(request):
    post = Post.objects.all().order_by('-date_created')
    paginator = Paginator(post, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dic = {
        'post': page_obj,
    }
    return render(request, 'blog/post_list.html', dic)


def post_detail_view(request, pk):
    # post with its pk or id.
    post_detail = get_object_or_404(Post, pk=pk)
    # favorite post Backend for login users.
    fav_form = FavoritePostForm(request.POST or None, initial={'user': request.user,
                                                               'fav_post': post_detail})
    if fav_form.is_valid():
        fav_form.save()
        return redirect('post_detail_view', pk)
    user_fav_post_check = Favorite.objects.all().filter(user_id=request.user.id, fav_post_id=pk)
    # comments section.
    comments = post_detail.comments.all().order_by('-datetime_comment')
    # comment form for logging users
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post_detail
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    # comment form for not logging users
    if request.method == 'POST' and not request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # filtering form values
            new_comment.post = post_detail
            new_comment.user = None
            # saving form values
            new_comment.save()
            # emptying forms section
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
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
        return reverse('post_view_of_blog')


class PostUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'blog/add_post.html'

    def get_success_url(self):
        return reverse('post_view_of_blog')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('post_delete_option')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


@login_required
def comment_update_view(request, pk, comment_id):
    auth = 0
    auth_check = Comment.objects.all().filter(user_id=request.user.id)
    for i in auth_check:
        if i.pk == comment_id:
            auth = i.pk
    if auth != 0:
        books = get_object_or_404(Post, pk=pk)
        comment = books.comments.all().filter(pk=comment_id).get()
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('books_detail_view', pk)
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
        comment = post.comments.all().filter(pk=comment_id).get()
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
    dic = {'user_posts_auth': post_bool,
           'post': page_obj,
           }
    return render(request, 'blog/user_posts_view.html', dic)


def user_fav_view(request):
    current_user = request.user.id
    user_fav_post = Post.objects.all().filter(fav_post__user_id=current_user).order_by('-date_created')
    paginator = Paginator(user_fav_post, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    dic = {
        'user_fav_post': page_obj
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

