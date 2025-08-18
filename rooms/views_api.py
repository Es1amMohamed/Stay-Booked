from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.response import Response


@api_view(["GET"])
def rooms_list_api(request):
    rooms = Room.objects.all()
    data = RoomSerializer(rooms, many=True, context={"request": request}).data
    return Response({"data": data})

@api_view(["GET"])
def room_detail_api(request, pk):
    room = get_object_or_404(Room, pk=pk)
    data = RoomSerializer(room, context={"request": request}).data
    return JsonResponse({"data": data})