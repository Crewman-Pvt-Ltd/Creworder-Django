from django.urls import path
from .views import getChatDetail,createChat,chat_count,GetGroups,CreateGroup,getUserListChat
from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('getChatDetail/', getChatDetail.as_view(), name='get_chat_detail'),
    path('createChat/', createChat.as_view(), name='create_chat'),
    path('getChatCount/', chat_count.as_view(), name='chat_count'),
    path('getChatgroups/', GetGroups.as_view(), name='chat_groups'),
    path('createGroup/', CreateGroup.as_view(), name='create_group'),
    path('getUserListChat/', getUserListChat.as_view(), name='get_user_list'),
]
