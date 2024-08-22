import random,string
from django.contrib.auth.models import User
from django.db import models
from product.models import Product
from django.core.exceptions import PermissionDenied
from accounts.models import Company, Branch


class Payment_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Payment_Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer_State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
    product_details = models.TextField()
    total_amount = models.FloatField()
    gross_amount = models.FloatField()
    discount = models.FloatField()
    prepaid_amount = models.IntegerField()
    payment_type = models.ForeignKey(Payment_Type, on_delete=models.PROTECT)
    payment_status = models.ForeignKey(Payment_Status, on_delete=models.PROTECT)
    order_status = models.ForeignKey(Status, on_delete=models.PROTECT)
    order_ship_by = models.IntegerField(null=True, blank=True)
    order_wayBill = models.CharField(max_length=255, null=True, blank=True)
    order_remark = models.TextField()
    repeat_order = models.IntegerField(choices=[(0, 'New'), (1, 'Repeat')])
    order_created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    is_booked = models.IntegerField(choices=[(0, 'Not Booked'), (1, 'Booked')])
    service_provider = models.CharField(max_length=50, null=True, blank=True)
    call_id = models.CharField(max_length=50, null=True, blank=True)
    course_order = models.IntegerField(default=0)
    course_order_repeated = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Orders'

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_unique_product_id()
        super().save(*args, **kwargs)

    def generate_unique_product_id(self):
        prefix = "ODR"
        length = 10 - len(prefix)  # Adjust the total length based on prefix length
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        random_suffix = ''.join(random.choice(characters) for _ in range(length))
        return prefix + random_suffix
    

class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order_Table, on_delete=models.CASCADE,related_name='order_details')
    product_id = models.CharField(max_length=200, default='0')
    product_name = models.CharField(max_length=255, default='0')
    product_qty = models.IntegerField()
    product_price = models.FloatField()
    product_total = models.FloatField()
    order_status = models.ForeignKey(Status, on_delete=models.PROTECT)
    class Meta:
        db_table = 'order_details'
    def __str__(self):
        return self.order_id
    

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

