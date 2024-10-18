from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
urlpatterns = [
    path(
        "user-dashboard-tiles/",
        views.GetUserDashboardtiles.as_view(),
        name="user-dashboard-tiles",
    ),
]