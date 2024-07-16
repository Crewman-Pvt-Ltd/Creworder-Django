import random
import string
from django.db import models
class Product(models.Model):
    sr = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=100, unique=True,null=True, blank=True)
    product_cat_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_sku = models.CharField(max_length=255)
    product_price = models.CharField(max_length=100)
    product_gst = models.CharField(max_length=20)
    product_hsn = models.CharField(max_length=200)
    product_qty = models.IntegerField()
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    product_availability = models.IntegerField(choices=[(0, 'InStock'), (1, 'OutOfStock')])
    product_status = models.IntegerField(choices=[(0, 'Pending'), (1, 'Active'), (2, 'Suspended'), (3, 'Deleted')])
    product_created = models.DateTimeField(auto_now_add=True)
    product_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'Products'

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = self.generate_unique_product_id()
        super().save(*args, **kwargs)

    def generate_unique_product_id(self):
        length = 8 
        characters = string.ascii_uppercase + string.digits 
        return ''.join(random.choice(characters) for _ in range(length))
