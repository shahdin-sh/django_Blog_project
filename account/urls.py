from django.urls import path
from .views import *


urlpatterns = [
    path('signup', signup_view, name='signup'),
    path('profile', user_profile, name='user_profile_view'),
    path('profile/edit/', edit_profile, name='edit_user_profile_view')
]
