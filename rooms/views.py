from django.shortcuts import render, redirect
from .serializers import *
from .models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required




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
@login_required
def my_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(guest_name=user)
    return render(request, 'reservations/my_reservations.html', {"reservations": reservations})

@login_required
def reservation_detail(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    return render(request, 'reservations/reservation_detail.html', {"reservation": reservation})

@login_required
def cancel_reservation(request, pk):
    reservation = Reservation.objects.get(pk=pk)
    reservation.delete()
    return redirect("rooms:my_reservations")
