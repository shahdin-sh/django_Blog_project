from django.shortcuts import redirect, get_object_or_404, render, HttpResponseRedirect
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.core.paginator import Paginator
from django.urls import reverse_lazy


def post_list_view(request):
    post = Post.objects.all().order_by('-datetime_modified').filter(status='pub')
    paginator = Paginator(post, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # dic
    page_title = 'HomePage'
    dic = {
        'post': page_obj,
        'page_title': page_title,
    }
    return render(request, 'blog/post_list.html', dic)


def post_detail_view(request, pk):
    # post with its pk or id
    post_detail = get_object_or_404(Post.objects.all().filter(status='pub'), pk=pk)
    # comments section for authenticated users
    comments = post_detail.comments.all().filter(is_active=True, parent__isnull=True).order_by('-datetime_modified')
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                # managing reply for authenticated users
                parent_obj = None
                try:
                    parent_id = int(request.POST.get('parent_id'))
                except:
                    parent_id = None
                if parent_id:
                    parent_obj = Comment.objects.get(id=parent_id)
                    if parent_obj:
                        replay_comment = comment_form.save(commit=False)
                        replay_comment.parent = parent_obj
                # normal comment form
                new_comment = comment_form.save(commit=False)
                new_comment.post = post_detail
                new_comment.user = request.user
                new_comment.save()
                comment_form = CommentForm()
        else:
            comment_form = CommentForm()
    # comment section for anonymous users
    else:
        if request.method == 'POST':
            comment_form = NoneUserCommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post_detail
                new_comment.user = None
                new_comment.save()
                comment_form = NoneUserCommentForm()
        else:
            comment_form = NoneUserCommentForm()
    # favorite post Backend for login users.
    if request.method == 'POST' and request.user.is_authenticated:
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
    page_title = f'Post Detail id:{pk}'
    dic = {
        'post_detail': post_detail,
        'comments': comments,
        'comment_form': comment_form,
        'fav_form': fav_form,
        'fav': user_fav_post_check,
        'page_title': page_title,
    }
    # rendering the request.
    return render(request, 'blog/post_detail.html', dic)


class PostCreateView(generic.CreateView):
    form_class = NewPostForm
    template_name = 'blog/add_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        if self.object.status == 'pub':
            return HttpResponseRedirect(reverse('post_detail_view', kwargs={'pk': self.object.pk}))
        elif self.object.status == 'drf':
            return HttpResponseRedirect(reverse('draft_user_detail_posts', kwargs={'pk': self.object.pk}))

    def get_context_data(self, *args, **kwargs):
        data = super(PostCreateView, self).get_context_data(*args, **kwargs)
        data['page_title'] = 'Add Post'
        return data


class PostUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = NewPostForm
    template_name = 'blog/add_post.html'

    def get_success_url(self):
        if self.get_object().status == 'pub':
            return reverse('post_detail_view', kwargs={'pk': self.object.pk})
        elif self.get_object().status == 'drf':
            return reverse('draft_user_detail_posts', kwargs={'pk': self.object.pk})

    def test_func(self):
        obj = self.get_object()
        if obj.author == self.request.user:
            return True

    def get_context_data(self, *args, **kwargs):
        data = super(PostUpdateView, self).get_context_data(*args, **kwargs)
        data['page_title'] = 'Edit Post'
        return data


class PostDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def get_context_data(self, *args, **kwargs):
        data = super(PostDeleteView, self).get_context_data(*args, **kwargs)
        data['page_title'] = f'Delete Post {self.object.pk}'
        return data


@login_required
def comment_update_view(request, pk, comment_id):
    auth = 0
    auth_check = Comment.objects.all().filter(user_id=request.user.id)
    for i in auth_check:
        if i.pk == comment_id:
            auth = i.pk
    if auth != 0:
        post = get_object_or_404(Post.objects.all().filter(status='pub'), pk=pk)
        comment = get_object_or_404(post.comments.all().filter(pk=comment_id))
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail_view', pk)
        page_title = f'Update Comment {comment_id}'
        return render(request, 'blog/comment_update_view.html', {'form': form, 'page_title': page_title})
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
        post = get_object_or_404(Post.objects.all().filter(status='pub'), pk=pk)
        comment = get_object_or_404(post.comments.all().filter(pk=comment_id))
        if request.method == 'POST':
            comment.delete()
            return redirect('post_detail_view', pk)
        page_title = f'Delete Comment {comment_id}'
        return render(request, 'blog/comment_delete_view.html', {'comment': comment,
                                                                 'post': post,
                                                                 'page_title': page_title})
    else:
        raise Http404()


def user_posts_view(request):
    current_user = request.user.id
    post_bool = Post.objects.all().filter(author=current_user, status='pub').exists()
    posts_pg = Post.objects.all().filter(author=current_user, status='pub').order_by('-date_created')
    paginator = Paginator(posts_pg, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_title = "Your Published Posts"
    dic = {'user_posts_auth': post_bool,
           'post': page_obj,
           'page_title': page_title,
           }
    return render(request, 'blog/user_posts_view.html', dic)


def user_fav_view(request):
    current_user = request.user.id
    user_fav_post = Post.objects.all().filter(fav_post__user_id=current_user, status='pub').order_by('-date_created')
    paginator = Paginator(user_fav_post, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_title = "Your Favorite Posts"
    dic = {
        'user_fav_post': page_obj,
        'page_title': page_title,
    }
    return render(request, 'blog/user_fav_posts_view.html', dic)


def delete_fav_user_post(request, pk):
    post = get_object_or_404(Post.objects.all().filter(status='pub'), pk=pk)
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


@login_required
def draft_user_posts_detail(request, pk):
    current_user_id = request.user.id
    draft_post_detail = Post.objects.all().filter(author_id=current_user_id, status='drf')
    draft_user_post = get_object_or_404(draft_post_detail, pk=pk)
    draft_title = ''
    draft_text = ''
    post_image_url = ''
    for i in draft_post_detail:
        if i.title:
            draft_title = i.title
        if i.text:
            draft_text = i.text
        if i.image_post:
            post_image_url = i.image_post
    if request.method == 'POST':
        draft_form = DraftPostForm(request.POST)
        if draft_form.is_valid():
            publish_form = draft_form.save(commit=False)
            publish_form.status = 'pub'
            publish_form.author = request.user
            publish_form.title = draft_title
            publish_form.text = draft_text
            publish_form.image_post = post_image_url
            publish_form.save()
            draft_post_detail.delete()
            draft_form = DraftPostForm()
            return redirect('draft_user_posts')
    else:
        draft_form = DraftPostForm()
    page_title = f'Draft Post:{pk}'
    dic = {
        'post_detail': draft_user_post,
        'form': draft_form,
        'page_title': page_title
    }
    return render(request, 'blog/drf_user_post_detail_view.html', dic)


@login_required
def draft_user_posts_view(request):
    current_user_id = request.user.id
    draft_user_posts = Post.objects.all().filter(status='drf', author_id=current_user_id).order_by('-date_created')
    paginator = Paginator(draft_user_posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_title = f'{len(draft_user_posts)} In Draft Inbox'
    dic = {
        'post': page_obj,
        'page_title': page_title,
    }
    return render(request, 'blog/drf_user_posts_view.html', dic)


def liked_user_comment(request, comment_id, pk):
    comment = get_object_or_404(Comment, pk=comment_id)
    user = request.user
    if user.is_authenticated:
        if comment.user not in comment.user_likes.all():
            comment.user_likes.add(user)
            return redirect('post_detail_view', pk)


def delete_liked_user_comment(request, comment_id, pk):
    comment = get_object_or_404(Comment, pk=comment_id)
    user = request.user
    if user.is_authenticated:
        if comment.user in comment.user_likes.all():
            comment.user_likes.remove(user)
            return redirect('post_detail_view', pk)