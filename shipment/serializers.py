from rest_framework import serializers
from .models import *
class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentModel
        fields = '__all__'  

class CourierServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierServiceModel
        fields = '__all__'  