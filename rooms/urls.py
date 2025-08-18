from django.urls import path
from .views import *
from .views_api import *


app_name = 'rooms'

urlpatterns = [
    
    path('rooms/list', rooms_list, name='rooms_list_view'),
    path('rooms/<int:pk>', room_detail, name='room_detail_view'),

    ## API
    path('api/rooms/list/', rooms_list_api, name='rooms_list'),
    path('api/rooms/<int:pk>/', room_detail_api, name='room_detail'),
    ]