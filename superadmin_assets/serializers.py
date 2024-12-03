from rest_framework import serializers
from .models import MenuModel,SubMenuModel,SettingsMenu,PixelCodeModel,BennerModel,ThemeSettingModel


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


class SettingMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsMenu
        fields = '__all__'

class PixelCodeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=PixelCodeModel
        fields='__all__'

class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=BennerModel
        fields='__all__'

class ThemeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=ThemeSettingModel
        fields='__all__'
        