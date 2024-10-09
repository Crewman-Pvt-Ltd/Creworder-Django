from . import views
from django.urls import path, include
from rest_framework.views import APIView

urlpatterns = [
    path("shipment-channel/", views.ShipmentView.as_view(), name="create-shipment"),
    path("check-serviceability/", views.CheckServiceability.as_view(), name="check-serviceability"),
    path("shipment-channel/<int:pk>", views.ShipmentView.as_view(), name="details-shipment"),
]
