from rest_framework import serializers
from .models import *

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"
class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    class Meta:
        model = Room
        fields = "__all__"