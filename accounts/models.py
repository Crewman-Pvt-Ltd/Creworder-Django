import hashlib
import pdb
import random
import string

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
from superadmin_assets.models import SubMenuModel,MenuModel


# from django.utils import timezone

class Module(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False, unique=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=20, choices=[('free', 'Free'), ('paid', 'Paid')], blank=False, null=False,
                            default='free')
    monthly_price = models.IntegerField(blank=False, null=False, default=100)
    annual_price = models.IntegerField(blank=False, null=False, default=100)
    quarterly_price = models.IntegerField(blank=False, null=False, default=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    max_employees = models.IntegerField(blank=False, null=False, default=5)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    max_admin = models.IntegerField(blank=True, null=True)
    setup_fees = models.IntegerField(blank=True, null=True)
    # modules = models.ManyToManyField(Module, related_name='packages')

    def save(self, *args, **kwargs):
        if self.created_by.role.role != 'superadmin':
            raise PermissionDenied("Only superadmins can create packages.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class PackageDetailsModel(models.Model):
    package=models.ForeignKey(Package,on_delete=models.CASCADE,related_name="packagedetails")
    menu=models.ForeignKey(MenuModel,on_delete=models.PROTECT,related_name="menu",blank=True, null=True)
    submenu=models.ForeignKey(SubMenuModel,on_delete=models.PROTECT,related_name="submunuid",blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "package_detail_table"
    def __str__(self):
        return f"{self.id}"


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"
        permissions = (
            ('can_view_own_company', 'Can view own company'),
            ('can_edit_own_company', 'Can edit own company'),
            ('can_delete_own_company', 'Can delete own company'),
            ('can_manage_own_company', 'Can manage own company'),
            ('can_change_company_status', 'Can change company status')
        )

    payment_freq = [('month', 'Monthly'), ('quarter', "Quarterly"), ('annual', 'Annually')]
    account_type_choices = [('current', 'Current Account'), ('savings', 'Savings Account')]

    name = models.CharField(max_length=100, blank=False)
    company_email = models.EmailField(max_length=100, blank=False, unique=True, null=False)
    company_phone = PhoneNumberField(null=False, unique=True, blank=False)
    company_website = models.CharField(max_length=100, blank=False, null=False)
    company_address = models.CharField(max_length=200, blank=False, null=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    company_id = models.CharField(max_length=50, blank=True, null=True)
    company_image = models.ImageField(upload_to='company_images/', blank=True, null=True)
    payment_mode = models.CharField(max_length=20, blank=True, null=True, choices=payment_freq)
    next_payment_date = models.DateField(null=True, blank=True)
    gst = models.CharField(max_length=60, null=True, blank=True)
    pan = models.CharField(max_length=60, null=True, blank=True)
    cin = models.CharField(max_length=60, null=True, blank=True)
    fssai = models.CharField(max_length=60, null=True, blank=True)
    bank_account_no = models.IntegerField(null=True, blank=True)
    bank_account_type = models.CharField(max_length=20, null=True, blank=True, choices=account_type_choices)
    bank_name = models.CharField(max_length=120, null=True, blank=True)
    bank_branch_name = models.CharField(max_length=120, null=True, blank=True)
    bank_ifsc_code = models.CharField(max_length=40, null=True, blank=True)
    support_email = models.EmailField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.created_by.role.role != 'superadmin':
            raise PermissionDenied("Only superadmins can create companies.")
        if not self.company_id:
            self.company_id = self.generate_company_id()
        super().save(*args, **kwargs)
        if not self.branches.exists():
            Branch.objects.create(name="Default Branch", company=self, address=self.company_address)

    def generate_company_id(self):
        while True:
            hash_object = hashlib.sha256(self.name.encode())
            company_id = f"{hash_object.hexdigest()[:5]}{get_random_string(length=5, allowed_chars='0123456789')}"
            if not Company.objects.filter(company_id=company_id).exists():
                return company_id.upper()

    def __str__(self):
        return self.name


class Branch(models.Model):
    class Meta:
        verbose_name_plural = "Branches"
    name = models.CharField(max_length=80, blank=False, null=False)
    branch_id = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=False, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="branches")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def generate_branch_id(self):
        prefix = self.company.company_id
        characters = string.digits
        random_suffix = ''.join(random.choice(characters) for _ in range(5))
        return prefix + random_suffix

    def save(self, *args, **kwargs):
        if not self.branch_id:
            self.branch_id = self.generate_branch_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.branch_id} ({self.company.name})'


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class UserStatus(models.IntegerChoices):
    inactive = 0, "Inactive"
    active = 1, "Active"
    suspended = 2, "Suspended"
    deleted = 3, "Deleted"

class Shift(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    branch = models.ForeignKey(Branch, null=False, blank=False, related_name="shifts", on_delete=models.CASCADE)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)

    def __str__(self):
        return f'{self.name} - {self.branch.branch_id}'
    
class UserProfile(models.Model):
    gender_choices = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('t', 'Transgender')
    ]

    employment_choices = [
        ('full', 'Full Time'),
        ('part', 'Part Time'),
        ('trainee', 'Trainee'),
        ('intern', 'Internship')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    status = models.IntegerField(choices=UserStatus.choices, default=UserStatus.active)
    gender = models.CharField(max_length=2, choices=gender_choices, default="m")
    contact_no = PhoneNumberField(null=False, unique=True, blank=False)
    marital_status = models.CharField(max_length=20, choices=[('married', "Married"), ('unmarried', "Unmarried")],
                                      default="unmarried")
    date_of_joining = models.DateField(auto_now_add=True)
    daily_order_target = models.IntegerField(blank=True, null=True)
    reporting = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    professional_email = models.EmailField(null=True, blank=True)
    # shift = models.ForeignKey(Shift, on_delete=models.PROTECT, null=True, blank=True, related_name='shift')
    enrolment_id = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.PROTECT, related_name="department_wise_users",
                                   null=True, blank=True)
    designation = models.ForeignKey('Designation', on_delete=models.PROTECT, related_name='designation_wise_users',
                                    null=True, blank=True)
    login_allowed = models.BooleanField(default=False)
    employment_type = models.CharField(max_length=30, null=True, blank=True, choices=employment_choices)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()
        super().save(*args, **kwargs)

    def generate_employee_id(self):
        prefix = ""
        if self.user.role.role == "superadmin":
            prefix = "SUPER"
        elif self.user.role.role == "admin" or self.user.role.role == "agent":
            prefix = str(self.user.profile.company.company_id).upper()[:4]

        length = 8 - len(prefix)
        characters = string.digits
        random_suffix = ''.join(random.choice(characters) for _ in range(length))
        return prefix + random_suffix

    def __str__(self):
        return self.user.username


class Notice(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)
    users = models.ManyToManyField(User, related_name='notices')

    def __str__(self):
        return self.title


class FormEnquiry(models.Model):
    class Meta:
        verbose_name_plural = "Form Enquiries"

    name = models.CharField(max_length=70, blank=False, null=False)
    phone = PhoneNumberField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.id


class SupportTicketStatus(models.IntegerChoices):
    open = 0, "Open"
    pending = 1, "Pending"
    resolved = 2, "Resolved"
    closed = 3, "Closed"


class SupportTicket(models.Model):
    priority_choices = [
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('low', 'Low'),
        ('medium', 'Medium')
    ]
    company = models.ForeignKey(Company, blank=False, null=False, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(blank=False, null=False)
    status = models.IntegerField(null=False, blank=False, default=SupportTicketStatus.open,
                                 choices=SupportTicketStatus.choices)
    ticket_id = models.CharField(max_length=80, null=True, blank=True)
    agent = models.ForeignKey(User, blank=False, null=False, related_name="support_tickets", on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=[('ques', 'Question'), ('problem', 'Problem'),
                                                    ('gen_query', 'General Query')], blank=False, null=False)
    priority = models.CharField(max_length=15, blank=True, null=True, choices=priority_choices)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()
        super().save(*args, **kwargs)

    def generate_ticket_id(self):
        characters = string.ascii_uppercase + string.digits
        ticket_id = ''.join(random.choice(characters) for _ in range(10))

        while SupportTicket.objects.filter(ticket_id=ticket_id).exists():
            ticket_id = ''.join(random.choice(characters) for _ in range(10))

        return ticket_id

    def __str__(self):
        return self.ticket_id


class Department(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, related_name="designations")

    def __str__(self):
        return self.name


class Leave(models.Model):
    duration_choices = [
        ('full', 'Full Day'),
        ('first', 'First Half'),
        ('second', 'Second Half')
    ]

    type_choices = [
        ('casual', 'Casual'),
        ('sick', 'Sick'),
        ('earned', 'Earned')
    ]

    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('disapprove','Disapprove')
    ]

    user = models.ForeignKey(User, related_name="leaves", on_delete=models.CASCADE, null=False, blank=False)
    duration = models.CharField(max_length=30, null=True, blank=True, choices=duration_choices)
    type = models.CharField(max_length=30, null=False, blank=False, choices=type_choices)
    status = models.CharField(max_length=30, null=False, blank=False, choices=status_choices)
    reason = models.CharField(max_length=500, null=False, blank=False)
    date = models.DateField(null=True, blank=True)
    attachment = models.ImageField(upload_to='leave_attachments/', blank=True, null=True)
    class Meta:
        permissions = (
            ('can_approve_disapprove_leave', 'Can approve disapprove leave'),
        )

    def __str__(self):
        return f'{self.user.username} - {self.reason}'


class Holiday(models.Model):
    occasion = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.PROTECT)
    designation = models.ForeignKey(Designation, null=False, blank=False, on_delete=models.PROTECT)
    branch = models.ForeignKey(Branch, null=True, blank=True, related_name="holidays", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.occasion} - {self.date}'


class Award(models.Model):
    title = models.CharField(max_length=120, null=False, blank=False, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, related_name="awards")
    summary = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.branch.branch_id}'


class Appreciation(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(User, related_name="appreciations", null=False, blank=False, on_delete=models.CASCADE)
    date_given = models.DateField(null=False, blank=False)
    summary = models.CharField(max_length=500, null=True, blank=True)
    award_image = models.ImageField(upload_to='award_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.award.title} - {self.user.username}'
    

class ShiftRoster(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, related_name="shift_rosters", on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, null=False, blank=False, related_name="shift_rosters", on_delete=models.CASCADE)

    monday_shift = models.ForeignKey(Shift, null=True, blank=True, related_name="monday_shift_rosters", on_delete=models.PROTECT)
    monday_shift_remark = models.TextField(null=True, blank=True)
    
    tuesday_shift = models.ForeignKey(Shift, null=True, blank=True, related_name="tuesday_shift_rosters", on_delete=models.PROTECT)
    tuesday_shift_remark = models.TextField(null=True, blank=True)
    
    wednesday_shift = models.ForeignKey(Shift, null=True, blank=True, related_name="wednesday_shift_rosters", on_delete=models.PROTECT)
    wednesday_shift_remark = models.TextField(null=True, blank=True)
    
    thursday_shift = models.ForeignKey(Shift, null=True, blank=True, related_name="thursday_shift_rosters", on_delete=models.PROTECT)
    thursday_shift_remark = models.TextField(null=True, blank=True)
    
    friday_shift = models.ForeignKey(Shift, null=True, blank=True, related_name="friday_shift_rosters", on_delete=models.PROTECT)
    friday_shift_remark = models.TextField(null=True, blank=True)
    
    saturday_shift = models.ForeignKey(Shift, null=True, blank=True, related_name="saturday_shift_rosters", on_delete=models.PROTECT)
    saturday_shift_remark = models.TextField(null=True, blank=True)
    
    sunday_shift = models.ForeignKey(Shift, null=True, blank=True, related_name="sunday_shift_rosters", on_delete=models.PROTECT)
    sunday_shift_remark = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shift_roster_table'

    def __str__(self):
        return f'{self.user.username} - {self.branch.branch_id}'



class Attendance(models.Model):
    working_choices = [
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other')
    ]
    attendance = [
        ('A', 'A'),
        ('P', 'P'),
    ]
    date = models.DateField(null=False, blank=False)
    shift = models.ForeignKey(Shift, on_delete=models.PROTECT, related_name="shift_wise_attendances", null=True)
    user = models.ForeignKey(User, related_name="attendances", null=False, blank=False, on_delete=models.CASCADE)
    clock_in = models.TimeField(null=False, blank=False)
    clock_out = models.TimeField(null=True, blank=True)
    working_from = models.CharField(max_length=80, null=False, blank=False, choices=working_choices, default="office")
    attendance = models.CharField(choices=attendance, max_length=80, default="A", null=False, blank=False, )

    def __str__(self):
        return f'{self.user.username} - {self.date}'


class AllowedIP(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="allowed_ip")
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.ip_address} for {self.branch.branch_id}"
