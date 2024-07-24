from django.contrib import admin

from .models import Company
from .models import Package
from .models import UserRole
from .models import UserProfile

admin.site.register(Company)
admin.site.register(Package)
admin.site.register(UserRole)
admin.site.register(UserProfile)
