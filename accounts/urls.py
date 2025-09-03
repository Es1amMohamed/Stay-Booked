from django.urls import path
from.views_api import *
from.views import *


app_name = 'accounts'

urlpatterns = [

    path('register', register, name='register'),
    path('login/', login, name='login'),
    path('password/change', change_password_view, name='change_password_view'),
    path("password/reset/", password_reset, name="password_reset_view"),
    path("password/confirm/<uidb64>/<token>/", password_reset_confirm, name="password_reset_confirm_view"),

    # API
    path('register/api', register_api, name='register_api'),
    path('login/api', login_api, name='login_api'),
    path('password/change/api', change_password, name='change-password'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate-account'),
    path("password/reset/api", reset_password_request, name="password-reset"),
    path("password/reset/confirm/<uidb64>/<token>/", confirm_password_reset, name="password-reset-confirm"),
]