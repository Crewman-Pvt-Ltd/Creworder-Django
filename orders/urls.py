from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
    path("orders/", views.OrderAPIView.as_view(), name="order-list-create"),
    path("orders/<int:pk>/", views.OrderAPIView.as_view(), name="order-detail"),
    path("category/", views.CategoryView.as_view(), name="category-create"),
    path("category/<int:pk>", views.CategoryView.as_view(), name="update-create"),
    path("product/", views.ProductView.as_view(), name="product-create"),
    path("getproduct/<int:pk>", views.ProductView.as_view(), name="product-create"),
    path("product/<int:pk>", views.ProductView.as_view(), name="product-update-delete"),
    path(
        "products/<int:pk>/",
        views.ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    path("products/", views.ProductListCreateAPIView.as_view(), name="product-detail"),
    path(
        "getCategory/<int:pk>",
        views.CategorytDetailAPIView.as_view(),
        name="category-detail",
    ),
    path(
        "getCategory/",
        views.CategoryListCreateAPIView.as_view(),
        name="category-detail",
    ),
    path("export-order/", views.orderExport.as_view(), name="export-order"),
    path("invoice-deatails/", views.invoiceDetails.as_view(), name="invoice-deatails"),
    path(
        "check-serviceability/",
        views.CheckServiceability.as_view(),
        name="check-serviceability",
    ),
    path(
        "user-performance/", views.GetUserPerformance.as_view(), name="user-performance"
    ),
]
