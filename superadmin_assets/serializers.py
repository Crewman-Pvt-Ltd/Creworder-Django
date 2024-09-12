from rest_framework import serializers
from .models import MenuModel,SubMenuModel

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = '__all__'  


class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenuModel
        fields = '__all__'  