from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('orders/', views.OrderAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderAPIView.as_view(), name='order-detail'),
]