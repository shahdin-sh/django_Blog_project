from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', post_list_view, name='post_view_of_blog'),
    path('<int:pk>', post_detail_view, name='post_detail_view'),
    path('add/', login_required(PostCreatView.as_view()), name='post_view_add'),
    path('<int:pk>/edit/',  login_required(PostUpdateView.as_view()), name='post_edit_option'),
    path('<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post_delete_option'),
    path('<int:pk>/update/<int:comment_id>/comment', comment_update_view, name='comment_update_view'),
    path('<int:pk>/delete/<int:comment_id>/comment', comment_delete_view, name='comment_delete_view'),
    path('user_posts/', user_posts_view, name='user_post_view'),
    path('user_fav/', user_fav_view, name='user_fav_post_view'),
    path('<int:pk>/delete_fav_post/', delete_fav_user_post, name='delete_fav_user_post')
]
