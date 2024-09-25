from rest_framework import serializers
from .models import MenuModel,SubMenuModel


class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenuModel
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    sub_menu_list = serializers.SerializerMethodField()
    class Meta:
        model = MenuModel
        fields = '__all__'

    def get_sub_menu_list(self, menu):
        sub_menus = SubMenuModel.objects.filter(menu_id=menu.id)
        return SubMenuSerializer(sub_menus, many=True).data
