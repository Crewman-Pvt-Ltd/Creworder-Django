from django.db import models
from accounts.models import Company, Branch
class ShipmentModel(models.Model):
    status=[
        (1,"Active"),
        (0,"Inactive")
    ]
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    provider_name=models.CharField(max_length=255)
    credential_username=models.CharField(max_length=255,null=True)
    credential_password=models.CharField(max_length=255,null=True)
    credential_email=models.CharField(max_length=255,null=True)
    credential_token=models.CharField(max_length=255,null=True)
    same_provider_priority=models.IntegerField()
    provider_priority=models.IntegerField()
    status=models.IntegerField(choices=status)
    image=models.ImageField(upload_to='shipment_channels_image/')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'shipment_table'
    def __str__(self):
        return f"products {self.id} by {self.name}"