import os
import random,string
from rest_framework import status
from orders.models import Order_Table, OrderDetail
from rest_framework.response import Response
from orders.serializers import (
    OrderDetailSerializer,
    OrderTableSerializer,
    OrderLogSerializer
)
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound

def orderLogInsert(data):
        orderLogSerializer = OrderLogSerializer(data=data)
        if orderLogSerializer.is_valid():
            orderInsert = orderLogSerializer.save()
        else:
            raise ValueError(orderLogSerializer.errors)

def createOrders(data,user_id):
    orderId = "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
    userData = UserProfile.objects.filter(user_id=user_id).first()
    serializer = UserProfileSerializer(userData)
    serialized_data = serializer.data
    data["branch"] = serialized_data["branch"]
    data["company"] = serialized_data["company"]
    data["order_id"] = "ODR" + str(orderId)
    data["order_created_by"] = user_id
    orderSerializer = OrderTableSerializer(data=data)
    if orderSerializer.is_valid():
        orderSaveResponce = orderSerializer.save()
        for product in data["product_details"]:
            product['order']=orderSaveResponce.id
        orderDetailsSerializer = OrderDetailSerializer(data=data["product_details"],many=True)
        if orderDetailsSerializer.is_valid():
            orderDetailsSaveResponce = orderDetailsSerializer.save()
            orderLogInsert({"order":orderSaveResponce.id,"order_status":data["order_status"],"action_by":user_id,"remark":"Order Created"})
        else:
            order_instance = Order_Table.objects.get(pk=orderSaveResponce.id)
            order_instance.delete()
            raise ValueError(orderDetailsSerializer.errors)
        return orderSaveResponce
    else:
        raise ValueError(orderSerializer.errors)
    

def updateOrders(id, data):
    try:
        updatedData = Order_Table.objects.get(id=id)
        serializer = OrderTableSerializer(updatedData, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise ValueError(serializer.errors)
    except ObjectDoesNotExist:
        return None

def deleteOrder(id):
    try:
        data = Order_Table.objects.get(id=id)
        data.delete()
        return True
    except ObjectDoesNotExist:
        return False


def getOrderDetails(usrid,id=None):
    try:
        userData = UserProfile.objects.filter(user_id=usrid).first()
        serializer = UserProfileSerializer(userData)
        serialized_data = serializer.data
        tableData = ""
        if id is not None:
            tableData = Order_Table.objects.filter(
                branch=serialized_data["branch"], company=serialized_data["company"],id=id
            )
            orderDetailsData = OrderDetail.objects.filter(
                order=id
            )
            orderDetailsTableData = OrderDetailSerializer(orderDetailsData, many=True)
            orderTableData = OrderTableSerializer(tableData, many=True)
            orderTableData.data[0]['product_details']=orderDetailsTableData.data
        else:
            tableData = Order_Table.objects.filter(
                branch=serialized_data["branch"], company=serialized_data["company"]
            )
            orderTableData = OrderTableSerializer(tableData, many=True)
            for row in orderTableData.data:
                orderDetailsData = OrderDetail.objects.filter(order=row['id'])
                orderDetailsTableData = OrderDetailSerializer(orderDetailsData, many=True)
                row['product_details']=orderDetailsTableData.data

        return orderTableData.data
    except ObjectDoesNotExist:
        return False