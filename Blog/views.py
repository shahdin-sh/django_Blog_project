
from django.urls import reverse_lazy
from .forms import *
from django.views import generic


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_modified')


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreatView(generic.CreateView):
    form_class = NewPostFrom
    template_name = 'blog/add_post.html'

    def get_success_url(self):
        return reverse('post_view_of_blog')


class PostEditView(generic.UpdateView):
    model = Post
    form_class = NewPostFrom
    template_name = 'blog/add_post.html'


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/delete_post_view'
    success_url = reverse_lazy('post_delete_option')



