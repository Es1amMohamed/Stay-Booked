from django.urls import path
from.views_api import *
from.views import *


app_name = 'accounts'

urlpatterns = [

    path('register', register, name='register'),
    path('login', login, name='login'),
    path("test", test, name="test"),

    # API
    path('register/api', register_api, name='register'),
    path('login/api', login_api, name='login'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate-account'),
]