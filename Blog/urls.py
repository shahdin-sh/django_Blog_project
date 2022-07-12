from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', post_list_view, name='post_view_of_blog'),
    path('<int:pk>', post_detail_view, name='post_detail_view'),
    path('<int:pk>/liked/comment/<int:comment_id>', liked_user_comment, name='liked_user_comment'),
    path('<int:pk>/delete_like/comment/<int:comment_id>', delete_liked_user_comment, name='delete_liked_user_comment'),
    path('add/', login_required(PostCreateView.as_view()), name='post_view_add'),
    path('<int:pk>/edit/',  csrf_exempt(login_required(PostUpdateView.as_view())), name='post_edit_option'),
    path('<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post_delete_option'),
    path('<int:pk>/update/<int:comment_id>/comment', comment_update_view, name='comment_update_view'),
    path('<int:pk>/delete/<int:comment_id>/comment', comment_delete_view, name='comment_delete_view'),
    path('user_posts/', user_posts_view, name='user_post_view'),
    path('user_fav/', user_fav_view, name='user_fav_post_view'),
    path('<int:pk>/delete_fav_post/', delete_fav_user_post, name='delete_fav_user_post'),
    path('user_posts/draft', draft_user_posts_view, name='draft_user_posts'),
    path('draft/status/<int:pk>/', draft_user_posts_detail, name='draft_user_detail_posts')
]
