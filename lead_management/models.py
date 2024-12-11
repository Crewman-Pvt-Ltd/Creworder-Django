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
    

class LeadSourceModel(models.Model):
    branch = models.ForeignKey(Branch, related_name="custom_models", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name="custom_models", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lead_source_table'

    def __str__(self):
        return self.name

    # class Lead(models.Model):
    # # Fields as mentioned
    # name = models.CharField(max_length=255)
    # email = models.EmailField(max_length=255)
    # phone = models.CharField(max_length=15)
    # postalcode = models.CharField(max_length=20)
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # address = models.TextField()
    # message = models.TextField()
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE)
    # # Foreign Key to ProductModel
    # product = models.ForeignKey(ProductModel, related_name="leads", on_delete=models.CASCADE)
    # # Select Lead - Could be a choice field or any other logic to mark a lead
    # select_lead = models.BooleanField(default=False)
    # # Timestamps
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"Lead for {self.product.product_name} by {self.name}"

    # class Meta:
    #     db_table = 'leads_table'


    # branch
    # company
    # name 
    # created_at
    # updated_at
    