from django.db import models
from django.contrib.auth.models import User
from accounts.models import Company, Branch


class CloudTelephonyChannel(models.Model):
    AUTH_TOKEN_CHOICES = [
        (0, "No Auth"),
        (1, "Bearer Token"),
        (2, "JWT Bearer"),
        (3, "Basic Auth"),
    ]
    STATUS = [
        (0, "Inactive"),
        (1, "Active"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    cloud_celephony_provider_name = models.CharField(
        max_length=255, null=True, blank=True
    )
    logo = models.ImageField(
        upload_to="cloudtelephoney_channel_images/", null=True, blank=True
    )
    creadentials_json = models.TextField()
    auth_tokent_ype = models.IntegerField(choices=AUTH_TOKEN_CHOICES)
    status = models.IntegerField(choices=STATUS)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cloud_telephony_channel_table"

    def __str__(self):
        return f"Note {self.id} by {self.name}"

class CloudTelephonyChannelAssign(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    cloud_telephony_channel_table = models.ForeignKey(CloudTelephonyChannel, on_delete=models.CASCADE, default=1)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cloud_celephony_provider_name = models.CharField(max_length=255, null=True, blank=True)
    priority=models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "telephony_channals_assign_table"
    def __str__(self):
        return f"Note {self.id} by {self.cloud_celephony_provider_name}"
    


class UserMailSetup(models.Model):
    name=models.CharField(max_length=255,null=False)
    email=models.EmailField(max_length=255,null=False)
    username=models.CharField(max_length=255,null=False)
    password=models.CharField(max_length=25,null=False)
    hostname=models.CharField(max_length=255,null=False)
    mail_smtp=models.CharField(max_length=255,null=False)
    mail_port=models.IntegerField(max_length=6,null=False)
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='user_mail_setup_table'
    def __str__(self):
        return f"{self.name} {self.email} {self.company.name} {self.branch.name}"


