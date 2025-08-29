from django.shortcuts import render
from .serializers import *
from .models import *
from accounts.models import *




def rooms_list(request):
    return render(request, 'rooms/rooms_list.html')  

def room_detail(request, pk):
    return render(request, 'rooms/room_detail.html', {"room_id": pk}) 

def recommend_rooms_view(request):
    return render(request, 'rooms/recommend_rooms.html')

def hotels_list(request):
    return render(request, "hotels/hotels_list.html")

def hotels_detail(request, pk):
    return render(request, 'hotels/hotel_detail.html', {"hotel_id": pk})

