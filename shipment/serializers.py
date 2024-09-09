from rest_framework import serializers
from .models import *
class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentModel
        fields = '__all__'  