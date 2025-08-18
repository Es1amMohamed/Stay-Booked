from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import *
from .models import *




def rooms_list(request):
    return render(request, 'rooms/rooms_list.html')  

def room_detail(request, pk):
    return render(request, 'rooms/room_detail.html', {"room_id": pk}) 