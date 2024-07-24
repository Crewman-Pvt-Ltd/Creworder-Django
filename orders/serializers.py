from rest_framework import serializers
from .models import Order_Table, OrderDetail
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

class OrderTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Table
        fields = '__all__'
