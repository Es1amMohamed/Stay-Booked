from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models.functions import Ceil
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from rest_framework.response import Response
import numpy as np
from sklearn.linear_model import LinearRegression


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


@api_view(["POST"])
@login_required
def create_reservation_api(request, room_id):
    serializer = ReservationSerializer(data=request.data, context={"request": request, "room_id": room_id})
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"data": serializer.data}, status=201)
    return JsonResponse({"errors": serializer.errors}, status=400)

@login_required
@api_view(["GET"])
def my_reservations_api(request):
    reservations = Reservation.objects.filter(user=request.user)
    data = ReservationSerializer(reservations, many=True, context={"request": request}).data
    return JsonResponse({"data": data})
@api_view(['GET'])
def recommend_rooms(request):
    budget = request.GET.get("budget")  
    if not budget:
        return JsonResponse({"error": "Please provide budget"}, status=400)

    try:
        budget = float(request.GET.get("budget"))
    except ValueError:
        return JsonResponse({"error": "Budget must be a number"}, status=400)  
      
    rooms = Room.objects.all()
    if not rooms.exists():
        return JsonResponse({"error": "No rooms available"}, status=404)

    X = np.array([[r.price] for r in rooms])
    y = np.array([r.price for r in rooms])

    model = LinearRegression()
    model.fit(X, y)

    predicted_price = model.predict([[budget]])[0]

    recommended = sorted(
        rooms,
        key=lambda r: abs(r.price - predicted_price)
    )[:5]

    data = [
        {
            "id": r.id,
            "name": r.name,
            "price": r.price,
            "image": r.image.url if r.image else None
        }
        for r in recommended
    ]

    return JsonResponse({"recommended_rooms": data})

@api_view(["GET"])
def hotels_list_api(request):
    hotels = Hotel.objects.annotate(avg_price_calc=Ceil(Avg("room_hotel__price"))).order_by("name")
    hotel = Hotel.objects.get(name= "Hotel1")
    print(hotel.hotel_subscribed.all())
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if min_price:
        hotels = hotels.filter(avg_price_calc__gte=min_price)
    if max_price:
        hotels = hotels.filter(avg_price_calc__lte=max_price)

    paginator = PageNumberPagination()
    paginator.page_size = 5 
    result_page = paginator.paginate_queryset(hotels, request)
    serializer = HotelSerializer(result_page, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)
@api_view(["GET"])
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