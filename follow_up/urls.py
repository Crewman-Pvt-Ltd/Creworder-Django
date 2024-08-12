from django.urls import path
from .views import (CreateFollowUp,
                    FollowUpList,
                    FollowUpDelete,
                    FollowUpUpdate)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('createFollowUp/', CreateFollowUp.as_view(), name='create_follow_up'),
    path('getFollowUps/', FollowUpList.as_view(), name='get_follow_ups'),
    path('delFollowUp/<int:follow_up_id>/', FollowUpDelete.as_view(), name='delete_follow_up'),
    path('updateFollowUp/<int:follow_up_id>/', FollowUpUpdate.as_view(), name='delete_follow_up'),
]

