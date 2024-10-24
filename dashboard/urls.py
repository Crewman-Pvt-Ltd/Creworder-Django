from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = [
    path("user-dashboard-tiles/",views.GetUserDashboardtiles.as_view(),name="user-dashboard-tiles",),
    path("user-dashboard-team-order-list/",views.TeamOrderListForDashboard.as_view(),name="user-dashboard-team-order-list"),
    path("top-shelling-product-list/",views.TopShellingProduct.as_view(),name="top-shelling-product-list")
]