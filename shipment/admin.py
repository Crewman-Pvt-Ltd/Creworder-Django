from django.contrib import admin
from .models import ShipmentModel
from .models import CourierServiceModel
admin.site.register(CourierServiceModel)
admin.site.register(ShipmentModel)

