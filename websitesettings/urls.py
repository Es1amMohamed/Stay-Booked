from django.urls import path
from .views import *
from .views_api import *


app_name = 'websitesettings'

urlpatterns = [
    path("", home, name="home"),
    path("services", services, name="services"),
    path("about_us", about_us, name="about_us"),
]