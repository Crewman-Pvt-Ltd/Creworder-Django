from django.contrib import admin
from .models import Order_Table,Payment_Type,Payment_Status,Status,Customer_State
# Register your models here.

admin.site.register(Order_Table)
admin.site.register(Payment_Type)
admin.site.register(Payment_Status)
admin.site.register(Status)
admin.site.register(Customer_State)