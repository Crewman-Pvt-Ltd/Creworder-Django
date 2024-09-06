from . import views
from django.urls import path, include
from rest_framework.views import APIView

urlpatterns = [
    path("shipment-channel/", views.ShipmentView.as_view(), name="create-shipment"),
    path("shipment-channel/<int:pk>", views.ShipmentView.as_view(), name="details-shipment"),
]
