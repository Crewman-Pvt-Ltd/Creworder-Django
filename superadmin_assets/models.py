from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


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
                codename=f"can_{perm_name}_{self.name.lower().replace(' ', '_')}",
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
                codename=f"can_{perm_name}_{self.name.lower().replace(' ', '_')}",
                content_type=content_type
            )