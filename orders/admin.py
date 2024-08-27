from django.contrib import admin
from .models import Order_Table,Payment_Type,Payment_Status,OrderStatus,Customer_State,CategoryModel,ProductModel,OrderLogModel,OrderDetail
# Register your models here.
admin.site.register(Order_Table)
admin.site.register(Payment_Type)
admin.site.register(Payment_Status)
admin.site.register(OrderStatus)
admin.site.register(Customer_State)
admin.site.register(CategoryModel)
admin.site.register(ProductModel)
admin.site.register(OrderLogModel)
admin.site.register(OrderDetail)