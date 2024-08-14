from django.contrib import admin

# Register your models here.
from .models import CloudTelephonyChannel,CloudTelephonyChannelAssign

admin.site.register(CloudTelephonyChannel)
admin.site.register(CloudTelephonyChannelAssign)
