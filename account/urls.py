from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('profile', user_profile, name='user_profile_view'),
    path('profile/edit/', edit_profile, name='edit_user_profile_view'),
    path('profile/add/avatar', login_required(UploadUserAvatar.as_view()), name='add_user_profile_pic'),
    path('profile/update/avatar', login_required(UpdateUserAvatar.as_view()), name='update_user_profile_pic')
]
