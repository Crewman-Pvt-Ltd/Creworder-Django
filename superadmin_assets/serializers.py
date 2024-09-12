from rest_framework import serializers
from .models import MenuModel

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = '__all__'  
