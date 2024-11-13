from django.shortcuts import render
from .serializers import MenuSerializer,SubMenuSerializer,SettingMenuSerializer
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import MenuModel,SubMenuModel,SettingsMenu
from django.db.models import Q

class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuModel.objects.all()
    serializer_class = MenuSerializer
    pagination_class = None 


class SubMenuViewSet(viewsets.ModelViewSet):
    queryset = SubMenuModel.objects.all()
    serializer_class = SubMenuSerializer
    pagination_class = None

class SettingMenuViewSet(viewsets.ModelViewSet):
    queryset = SettingsMenu.objects.all()
    serializer_class = SettingMenuSerializer
    pagination_class = None

    def get_queryset(self):
        user_type = self.request.user.profile.user_type
        return SettingsMenu.objects.filter(
            Q(for_user=user_type) | Q(for_user='both'), 
            status=1
        )