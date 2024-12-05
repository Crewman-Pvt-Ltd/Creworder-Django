from django.utils import timezone
from django.db import models

# Slider Section Model
class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=255)
    button1 = models.CharField(max_length=255)
    button2 = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading

# Product Feature Model
class ProductFeature(models.Model):
    heading = models.CharField(max_length=255)
    subheading = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_feature_images/')
    url = models.URLField()
    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading

# Testimonial Model
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    profile_img = models.ImageField(upload_to='testimonial_images/')
    message = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Client Model
class Client(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    logo = models.ImageField(upload_to='client_logos/')
    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# About Company Model
class AboutCompany(models.Model):
    about = models.TextField()
    company = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='about_company_logos/')
    socialmedia = models.JSONField(default=list)  # To store social media data
    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company

# Highlight Section Model
class Highlight(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='highlight_images/')
    description = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
