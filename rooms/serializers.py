from rest_framework import serializers
from .models import *
from datetime import date

class HotelSerializer(serializers.ModelSerializer):
    avg_price = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ["name", "image", "image", "description", "avg_price","subscribers_count"]
    
    def get_avg_price(self, obj):
        return obj.avg_price
    
    def get_subscribers_count(self, obj):
        return obj.hotel_subscribed.count()
class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    class Meta:
        model = Room
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [ "adults", "children", "check_in", "check_out"]

    def validate_check_in(self, value):
        today = date.today()
        if value <= today:
            raise serializers.ValidationError("Check-in must be at least from tomorrow onwards.")
        return value
    
    def validate(self, attrs):
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")
        room = self.context.get("room_id")

        if check_out <= check_in:
            raise serializers.ValidationError("Check-out must be after check-in.")

        overlapping = Reservation.objects.filter(
            room_id=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()

        if overlapping:
            raise serializers.ValidationError("This room is already booked for the selected dates.")

        return attrs
    
    def create(self, validated_data):
        request = self.context["request"]
        validated_data["guest_name"] = request.user  
        validated_data["room_id"] = self.context.get("room_id")

        return super().create(validated_data)