from django.urls import path
from . import views

urlpatterns = [
    path('lead/', views.LeadCreateAPIView.as_view(), name='lead-list'),
    path('lead/<int:pk>', views.LeadCreateAPIView.as_view(), name='lead-list'),
    path('lead/create/', views.LeadCreateAPIView.as_view(), name='lead-create'),
]