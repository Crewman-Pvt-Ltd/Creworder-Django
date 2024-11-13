from rest_framework.routers import DefaultRouter
from .views import MenuViewSet,SubMenuViewSet,SettingMenuViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'menu', MenuViewSet)
router.register(r'submenu', SubMenuViewSet)
router.register(r'setting_menu', SettingMenuViewSet, basename='settingmenu')

urlpatterns = [
    path('', include(router.urls)),
]
