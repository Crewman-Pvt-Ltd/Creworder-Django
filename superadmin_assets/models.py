from django.db import models

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
    
class SubMenuModel(models.Model):
    id = models.AutoField(primary_key=True)
    menu =models.ForeignKey(MenuModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=255,unique=True)
    url = models.TextField()
    icon=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'submenu_table'
    def __str__(self):
        return f"{self.id} by {self.name}"