from django.urls import path
from .views import *


urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('', showing_accounts_list, name='accounts_view')
]
