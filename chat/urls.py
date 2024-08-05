from django.urls import path
from .views import getChatDetail,createChat,chat_count
from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path('getChatDetail/', getChatDetail.as_view(), name='get_chat_detail'),
    path('createChat/', createChat.as_view(), name='create_chat'),
    path('getChatCount/', chat_count.as_view(), name='chat_count'),
]
