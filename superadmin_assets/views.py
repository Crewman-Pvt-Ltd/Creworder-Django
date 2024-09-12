from django.shortcuts import render
from .serializers import MenuSerializer,SubMenuSerializer
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import MenuModel,SubMenuModel

# Create your views here.
class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuModel.objects.all()
    serializer_class = MenuSerializer


class SubMenuViewSet(viewsets.ModelViewSet):
    queryset = SubMenuModel.objects.all()
    serializer_class = SubMenuSerializer