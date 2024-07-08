from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import PermissionDenied


class UserRole(models.Model):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('agent', 'Agent'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.role


class Company(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.created_by.role.role != 'superadmin':
            raise PermissionDenied("Only superadmins can create companies.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.created_by.role.role != 'superadmin':
            raise PermissionDenied("Only superadmins can create packages.")
        super().save(*args, **kwargs)

    def __str__(self):
        self.name
