from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')


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
    template_name = 'blog/delete_post_view'
    success_url = reverse_lazy('post_delete_option')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user



