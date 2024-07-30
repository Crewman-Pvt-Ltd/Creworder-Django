from rest_framework import serializers
from .models import Order_Table, OrderDetail
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

class OrderTableSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order_Table
        fields = '__all__'  # Or specify the fields you want to include
    # class Meta:
    #     model = Order_Table
    #     fields = '__all__'
