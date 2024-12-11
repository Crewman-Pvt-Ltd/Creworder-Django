from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadSourceModelViewSet

router = DefaultRouter()
router.register(r'lead_sources', LeadSourceModelViewSet)
urlpatterns = [
    path('lead/', views.LeadCreateAPIView.as_view(), name='lead-list'),
    path('lead/<int:pk>', views.LeadCreateAPIView.as_view(), name='lead-list'),
    path('lead/create/', views.LeadCreateAPIView.as_view(), name='lead-create'),
    path('', include(router.urls)),
]