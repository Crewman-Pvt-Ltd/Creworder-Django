from django.contrib import admin
from .models import Company
from .models import Package
from .models import PackageDetailsModel
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
from .models import Shift
from .models import Attendance
from .models import AllowedIP
from .models import ShiftRoster
from .models import PickUpPoint
from .models import UserTargetsDelails
from .models import AdminBankDetails

                                       
admin.site.register(Company)
admin.site.register(Package)
admin.site.register(PackageDetailsModel)
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
admin.site.register(Shift)
admin.site.register(Attendance)
admin.site.register(AllowedIP)
admin.site.register(ShiftRoster)
admin.site.register(PickUpPoint)
admin.site.register(UserTargetsDelails)
admin.site.register(AdminBankDetails)