from . import views
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.routers import DefaultRouter
from .views import CourierServiceView,ScheduleOrders
router = DefaultRouter()
router.register(r'courier-service', CourierServiceView)
router.register(r'schedule-orders',ScheduleOrders)
urlpatterns = [
    path('', include(router.urls)),
    path("shipment-channel/", views.ShipmentView.as_view(), name="create-shipment"),
    path("shipment-channel/<int:pk>", views.ShipmentView.as_view(), name="details-shipment"),
]
