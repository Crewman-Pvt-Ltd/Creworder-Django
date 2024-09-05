import random,string
import json
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import PermissionDenied
from accounts.models import Company, Branch

class CategoryModel(models.Model):
    STATUS = [
        (0, "Inactive"),
        (1, "Active"),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    description = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="category_images/", null=True, blank=True
    )
    status=models.IntegerField(choices=STATUS)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'category_table'
    def __str__(self):
        return f"category {self.id} by {self.name}"
    
class ProductModel(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=100, unique=True,null=True, blank=True)
    product_name = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_price = models.CharField(max_length=100)
    product_hsn_number = models.CharField(max_length=200)
    product_gst_percent = models.IntegerField(choices=[(0, '0%'),(5, '5%'), (12, '12%'), (18, '18%'), (28, '28%')])
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    product_description = models.TextField()
    product_availability = models.IntegerField(choices=[(0, 'InStock'), (1, 'OutOfStock')])
    product_status = models.IntegerField(choices=[(0, 'Pending'), (1, 'Active'), (2, 'Suspended'), (3, 'Deleted')])
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_created = models.DateTimeField(auto_now_add=True)
    product_updated = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'products_table'
    def __str__(self):
        return f"products {self.id} by {self.product_name}"
    
class Payment_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'payment_types_table'
    def __str__(self):
        return self.name
    
class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'order_status_table'
    def __str__(self):
        return self.name
    
class Payment_Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'payment_status_table'
    def __str__(self):
        return self.name

class Customer_State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'state_table'

    def __str__(self):
        return self.name

class Order_Table(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=100, unique=True,null=True, blank=True)
    network_ip = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=255)
    customer_parent_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=50)
    customer_alter_phone = models.CharField(max_length=50, null=True, blank=True)
    customer_email = models.EmailField(max_length=255, null=True, blank=True)
    customer_address = models.TextField()
    customer_postal = models.CharField(max_length=20)
    customer_city = models.CharField(max_length=255)
    customer_state = models.ForeignKey(Customer_State, on_delete=models.PROTECT)
    customer_country = models.CharField(max_length=150)
    product_details = models.JSONField()
    total_amount = models.FloatField()
    gross_amount = models.FloatField()
    discount = models.FloatField()
    prepaid_amount = models.IntegerField()
    payment_type = models.ForeignKey(Payment_Type, on_delete=models.PROTECT)
    payment_status = models.ForeignKey(Payment_Status, on_delete=models.PROTECT)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    order_ship_by = models.IntegerField(null=True, blank=True)
    order_wayBill = models.CharField(max_length=255, null=True, blank=True)
    order_remark = models.TextField()
    repeat_order = models.IntegerField(choices=[(0, 'New'), (1, 'Repeat')])
    order_created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    is_booked = models.IntegerField(choices=[(0, 'Not Booked'), (1, 'Booked')])
    service_provider = models.CharField(max_length=50, null=True, blank=True)
    call_id = models.CharField(max_length=50, null=True, blank=True)
    course_order = models.IntegerField(default=0)
    product_qty = models.IntegerField(default=0)
    shipping_charges = models.IntegerField(default=0)
    course_order_repeated = models.IntegerField(default=0)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'orders_table'
    

class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order_Table, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT,default=1)
    product_name = models.CharField(max_length=255, default='0')
    product_qty = models.IntegerField()
    product_mrp = models.FloatField(null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    gst_amount = models.FloatField(null=True, blank=True)
    taxeble_amount = models.FloatField(null=True, blank=True)
    product_total_price = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'orders_details_table'
    def __str__(self):
        return self.order
    
class OrderLogModel(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order_Table, on_delete=models.CASCADE)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT)
    action_by = models.ForeignKey(User, on_delete=models.PROTECT)
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'order_log_table'
    def __str__(self):
        return f"category {self.id} by {self.order}"

