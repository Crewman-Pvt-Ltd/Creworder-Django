from django.contrib import admin

from .models import Company
from .models import Package
from .models import UserRole
from .models import UserProfile
from .models import Notice
from .models import Branch
from .models import Module

admin.site.register(Company)
admin.site.register(Package)
admin.site.register(UserRole)
admin.site.register(UserProfile)
admin.site.register(Notice)
admin.site.register(Branch)
admin.site.register(Module)
