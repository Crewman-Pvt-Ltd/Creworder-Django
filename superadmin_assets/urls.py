from rest_framework.routers import DefaultRouter
from .views import MenuViewSet,SubMenuViewSet,SettingMenuViewSet,PixelCodeView,BannerView,ThemeSetting
from django.urls import path, include

router = DefaultRouter()
router.register(r'menu', MenuViewSet)
router.register(r'submenu', SubMenuViewSet)
router.register(r'setting_menu', SettingMenuViewSet, basename='settingmenu')
router.register(r'pixel-code',PixelCodeView,basename='pixel-code')
router.register(r'banner',BannerView,basename='banner')
router.register(r'theme-setting',ThemeSetting,basename='theam-setting')
urlpatterns = [
    path('', include(router.urls)),
]
