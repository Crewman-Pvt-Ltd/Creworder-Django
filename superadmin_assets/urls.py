from rest_framework.routers import DefaultRouter
from .views import MenuViewSet,SubMenuViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'menu', MenuViewSet)
router.register(r'submenu', SubMenuViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
