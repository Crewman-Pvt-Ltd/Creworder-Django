from rest_framework import serializers
from .models import Order_Table, OrderDetail,CategoryModel,ProductModel,OrderLogModel,Payment_Type
from django.contrib.auth.models import User
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

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
    order_details = OrderDetailSerializer(many=True, read_only=True, source='orderdetail_set')  # Use related name if defined
    # order_logs = OrderLogSerializer(many=True, read_only=True, source='orderlogmodel_set')  # Use related name if defined
    order_created_by_username = serializers.SerializerMethodField()
    last_action_by_name = serializers.SerializerMethodField()
    last_upated_at = serializers.SerializerMethodField()
    payment_mod = serializers.SerializerMethodField()
    class Meta:
        model = Order_Table
        fields = '__all__'  

    def get_order_created_by_username(self, auth):
        return auth.order_created_by.username if auth.order_created_by else None
    
    def get_last_action_by_name(self, obj):
        recent_log = OrderLogModel.objects.filter(order=obj).order_by('-updated_at').first()
        return OrderLogSerializer(recent_log).data['action_by_username'] if recent_log else None
    def get_payment_mod(self, obj):
        return obj.payment_type.name if obj.payment_type else None
    def get_last_upated_at(self, obj):
        recent_log = OrderLogModel.objects.filter(order=obj).order_by('-updated_at').first()
        return OrderLogSerializer(recent_log).data['updated_at'] if recent_log else None
    


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'  

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'  