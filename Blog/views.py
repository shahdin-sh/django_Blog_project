from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


def post_list_view(request):
    post = Post.objects.all()
    form = FavoritePost()
    if form.is_valid():
        form.save()
    dic = {
        'post': post,
        'form': form
    }
    return render(request, 'blog/post_list.html', dic )


def post_detail_view(request, pk):
    post_detail = get_object_or_404(Post, pk=pk)
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
    dic = {
        'post_detail': post_detail,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', dic)


class PostCreatView(generic.CreateView):
    form_class = NewPostFrom
    template_name = 'blog/add_post.html'

    def get_success_url(self):
        return reverse('post_view_of_blog')


class PostEditView(UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = NewPostFrom
    template_name = 'blog/add_post.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(UserPassesTestMixin,generic.DeleteView):
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


