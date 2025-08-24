from rest_framework import serializers
from .models import *

class HotelSerializer(serializers.ModelSerializer):
    avg_price = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = "__all__"
    
    def get_avg_price(self, obj):
        return obj.avg_price
class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    class Meta:
        model = Room
        fields = "__all__"