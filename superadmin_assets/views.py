from django.shortcuts import render
from .serializers import MenuSerializer
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .models import MenuModel

# Create your views here.
class MenuViewSet(viewsets.ModelViewSet):
    queryset = MenuModel.objects.all()
    serializer_class = MenuSerializer