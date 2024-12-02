from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from accounts.models import Company, Branch


class MenuModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    url = models.TextField()
    icon=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'menu_table'
    def __str__(self):
        return f"{self.id} by {self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        content_type, created = ContentType.objects.get_or_create(
            app_label=self.name.lower().replace(" ", "_"),
            model=self.name.lower().replace(" ", "_")
        )
        permission_names = ["view_all","view_own", "add", "change_all","change_own", "delete_all", "delete_own","export_all","export_own"]
        for perm_name in permission_names:
            Permission.objects.get_or_create(
                name=f"{perm_name.replace('_', ' ').capitalize()} {self.name.replace('_', ' ')}",
                codename=f"{perm_name}_{self.name.lower().replace(' ', '_')}",
                content_type=content_type
            )
    
class SubMenuModel(models.Model):
    id = models.AutoField(primary_key=True)
    menu =models.ForeignKey(MenuModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    url = models.TextField()
    icon = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'submenu_table'
    def __str__(self):
        return f"{self.id} by {self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        content_type, created = ContentType.objects.get_or_create(
            app_label=self.name.lower().replace(" ", "_"),
            model=self.name.lower().replace(" ", "_")
        )
        permission_names = ["view_all","view_own", "add", "change_all","change_own", "delete_all", "delete_own","export_all","export_own"]
        for perm_name in permission_names:
            Permission.objects.get_or_create(
                name=f"{perm_name.replace('_', ' ').capitalize()} {self.name.replace('_', ' ')}",
                codename=f"{perm_name}_{self.name.lower().replace(' ', '_')}",
                content_type=content_type
            )
          
class SettingsMenu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    url = models.TextField()
    icon = models.TextField()
    component_name = models.TextField()
    status = models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)
    for_user = models.CharField(max_length=255,choices=[('superadmin', 'For Super Admin'), ('admin', 'For Admin'),('both', 'Both')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'settings_menu_table'
    def __str__(self):
        return f"{self.id} by {self.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        content_type, created = ContentType.objects.get_or_create(
            app_label=f"settings_{self.name.lower().replace(' ', '_')}",
            model=f"settings_{self.name.lower().replace(' ', '_')}"
        )
        permission_names = ["view","add","change","delete"]
        for perm_name in permission_names:
            Permission.objects.get_or_create(
                name=f"settings_{perm_name.replace('_', ' ').capitalize()} {self.name.replace('_', ' ')}",
                codename=f"settings_{perm_name}_{self.name.lower().replace(' ', '_')}",
                content_type=content_type
            )

class PixelCodeModel(models.Model):
    google_analytics_code = models.TextField()
    meta_pexel_code = models.TextField()
    other_pexel_code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pixelcode_table'
    def __str__(self):
        return f"{self.id} by {self.name}"
    
class BennerModel(models.Model):
    banner_img = models.ImageField(upload_to="banner_images/")
    link = models.TextField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'banner_table'
    def __str__(self):
        return f"{self.id} by {self.link}"
    
class TheamSettingModel(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    dark_logo = models.ImageField(upload_to="theam_setting_images/")
    light_logo = models.ImageField(upload_to="theam_setting_images/")
    favicon_logo = models.ImageField(upload_to="theam_setting_images/")
    invoice_logo = models.ImageField(upload_to="theam_setting_images/")
    signature = models.ImageField(upload_to="theam_setting_images/")
    primary_color_code = models.CharField(max_length=255, blank=False, null=False)
    page_theam = models.CharField(max_length=255,choices=[('dark', 'Dark'), ('light', 'Light')], default='light')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,related_name='theam_branch')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='theam_company')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'theam_setting_table'
    def __str__(self):
        return f"{self.id} by {self.name}"