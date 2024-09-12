from rest_framework.routers import DefaultRouter
from .views import MenuViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'menu', MenuViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
