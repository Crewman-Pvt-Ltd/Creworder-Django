from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import PermissionDenied
from phonenumber_field.modelfields import PhoneNumberField


class Package(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=20, choices=[('free', 'Free'), ('paid', 'Paid')], blank=False, null=False,
                            default='free')
    monthly_price = models.IntegerField(blank=False, null=False, default=100)
    annual_price = models.IntegerField(blank=False, null=False, default=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    max_employees = models.IntegerField(blank=False, null=False, default=5)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.created_by.role.role != 'superadmin':
            raise PermissionDenied("Only superadmins can create packages.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100, blank=False)
    company_email = models.EmailField(max_length=100, blank=False, unique=True, null=False, default="abc@gmail.com")
    company_phone = PhoneNumberField(null=False, unique=True, blank=False, default="123456789")
    company_website = models.CharField(max_length=100, blank=False, null=False, default="abc@gmail.com")
    company_address = models.CharField(max_length=200, blank=False, null=False, default="company address")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=1)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if self.created_by.role.role != 'superadmin':
            raise PermissionDenied("Only superadmins can create companies.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username
