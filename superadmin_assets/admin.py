from django.contrib import admin
from django.contrib import admin
from .models import SubMenuModel,MenuModel,SettingsMenu
admin.site.register(MenuModel)
admin.site.register(SubMenuModel)
admin.site.register(SettingsMenu)

