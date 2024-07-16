from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
]