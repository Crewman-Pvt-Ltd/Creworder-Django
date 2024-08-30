from django.db import models
from accounts.models import Company, Branch
from django.contrib.auth.models import User

class LeadModel(models.Model):
    status=[
        (1,"Read"),
        (0,"Unread")
    ]
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=50)
    customer_number = models.CharField(max_length=50)
    customer_call_id = models.CharField(max_length=50)
    assign_user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.IntegerField(choices=status,default=0)
    remark = models.TextField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'lead_table'
    def __str__(self):
        return self.customer_name