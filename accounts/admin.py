from django.contrib import admin

from .models import Company
from .models import Package
from .models import UserRole
from .models import UserProfile
from .models import Notice
from .models import Branch
from .models import Module
from .models import FormEnquiry
from .models import SupportTicket
from .models import Department
from .models import Designation
from .models import Leave
from .models import Holiday
from .models import Award
from .models import Appreciation

admin.site.register(Company)
admin.site.register(Package)
admin.site.register(UserRole)
admin.site.register(UserProfile)
admin.site.register(Notice)
admin.site.register(Branch)
admin.site.register(Module)
admin.site.register(FormEnquiry)
admin.site.register(SupportTicket)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Leave)
admin.site.register(Holiday)
admin.site.register(Award)
admin.site.register(Appreciation)

