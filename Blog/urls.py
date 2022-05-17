from django.urls import path
from .views import *


urlpatterns = [
    path('', PostListView.as_view(), name='post_view_of_blog'),
    path('<int:pk>', post_detail_view, name='post_detail_view'),
    path('add/', PostCreatView.as_view(), name='post_view_add'),
    path('<int:pk>/edit/', PostEditView.as_view(), name='post_edit_option'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete_option'),
]
