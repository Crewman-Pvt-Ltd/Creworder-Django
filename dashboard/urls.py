from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = [
    path("user-dashboard-tiles/",views.GetUserDashboardtiles.as_view(),name="user-dashboard-tiles"),
    path("user-dashboard-team-order-list/",views.TeamOrderListForDashboard.as_view(),name="user-dashboard-team-order-list"),
    path("top-shelling-product-list/",views.TopShellingProduct.as_view(),name="top-shelling-product-list"),
    path("schedule-order-dashboard-chart/",views.ScheduleOrderForDashboard.as_view(),name="schedule-order-dashboard-chart"),
    path("top-buying-state/",views.StateWiseSalesTracker.as_view(),name="top-buying-state"),
    path("invoice-dashboard-data/",views.InvoiceDataForDashboard.as_view(),name="invoice-dashboard-data"),
    path("sales-forecast-dashboard-data/",views.SalesForecastDashboard.as_view(),name="sales-forecast-dashboard-data"),
]