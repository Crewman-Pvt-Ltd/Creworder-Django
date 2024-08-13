from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CreateCloudTelephoneyChannel,CloudTelephoneyChannelDelete)
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('createCloudTelephoneyChannel/', CreateCloudTelephoneyChannel.as_view(), name='create_cloud_telephoney_channel'),
    path('deleteCloudTelephoneyChannel/<int:id>/', CloudTelephoneyChannelDelete.as_view(), name='delete_cloud_telephoney_channel'),


]