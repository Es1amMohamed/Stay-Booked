from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
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

@api_view(["GET"])
def hotels_list_api(request):
    hotels = Hotel.objects.all()
    paginator = PageNumberPagination()
    paginator.page_size = 5 
    result_page = paginator.paginate_queryset(hotels, request)
    serializer = HotelSerializer(result_page, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)

def hotels_detail_api(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    hotel_rooms = Room.objects.filter(hotel=hotel.id)
    data = RoomSerializer(hotel_rooms, many=True,context={"request": request}).data
    return JsonResponse({"data": data})

@api_view(["GET"])
def hotelsearch(request):
    q = request.GET.get('q', '').strip()
    results = []

    if q:
        results = Hotel.objects.filter(
            name__icontains=q
        ).order_by("name")[:10]

    data = [
        {
            "id": result.id,
            "name": result.name,
        }
        for result in results
    ]

    return JsonResponse({"results": data})