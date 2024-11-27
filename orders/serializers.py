from rest_framework import serializers
from .models import Order_Table, OrderDetail,CategoryModel,ProductModel,OrderLogModel,Payment_Type,OrderStatus
from django.contrib.auth.models import User
from accounts.serializers import CompanySerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'  
        
class OrderDetailSerializer(serializers.ModelSerializer):
    gst_rate=serializers.SerializerMethodField()
    class Meta:
        model = OrderDetail
        fields = '__all__'
    def get_gst_rate(self ,data):
        return data.product.product_gst_percent if data.product else None


class OrderLogSerializer(serializers.ModelSerializer):
    action_by_username = serializers.SerializerMethodField()
    order_status_name = serializers.SerializerMethodField()
    class Meta:
        model = OrderLogModel
        fields = '__all__'  

    def get_action_by_username(self, auth):
        return auth.action_by.username if auth.action_by else None
    def get_order_status_name(self, auth):
        return auth.order_status.name if auth.order_status else None
    

class OrderTableSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True, source='orderdetail_set')
    # order_logs = OrderLogSerializer(many=True, read_only=True, source='orderlogmodel_set')
    order_created_by_username = serializers.SerializerMethodField()
    last_action_by_name = serializers.SerializerMethodField()
    last_upated_at = serializers.SerializerMethodField()
    payment_mode = serializers.SerializerMethodField()
    order_status_title = serializers.SerializerMethodField()
    class Meta:
        model = Order_Table
        fields = '__all__'  

    def get_order_created_by_username(self, auth):
        return auth.order_created_by.username if auth.order_created_by else None
    def get_order_status_title(self, data):
        return data.order_status.name if data.order_status else None
    def get_last_action_by_name(self, obj):
        recent_log = OrderLogModel.objects.filter(order=obj).order_by('-updated_at').first()
        return OrderLogSerializer(recent_log).data['action_by_username'] if recent_log else None
    def get_payment_mode(self, obj):
        return obj.payment_type.name if obj.payment_type else None
    def get_last_upated_at(self, obj):
        recent_log = OrderLogModel.objects.filter(order=obj).order_by('-updated_at').first()
        return OrderLogSerializer(recent_log).data['updated_at'] if recent_log else None
    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'  

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'  

class InvoiceSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True, source='orderdetail_set')
    order_created_by_username = serializers.SerializerMethodField()
    payment_mode = serializers.SerializerMethodField()
    order_status_title = serializers.SerializerMethodField()
    company_detail = serializers.SerializerMethodField()
    state_name = serializers.SerializerMethodField()
    payment_status_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Order_Table
        fields = '__all__'  

    def get_order_created_by_username(self, auth):
        return auth.order_created_by.username if auth.order_created_by else None

    def get_order_status_title(self, data):
        return data.order_status.name if data.order_status else None

    def get_payment_mode(self, obj):
        return obj.payment_type.name if obj.payment_type else None
    def get_state_name(self, obj):
        return obj.customer_state.name if obj.customer_state else None
    def get_payment_status_title(self, obj):
        return obj.payment_status.name if obj.payment_status else None

    def get_company_detail(self, obj):
        if obj.company:
            return CompanySerializer(obj.company).data
        return None

class FilterOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Table
        fields = '__all__'



    
