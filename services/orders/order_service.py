import os
import pycountry
import random,string
from rest_framework import status
from orders.models import Order_Table, OrderDetail,ProductModel,OrderLogModel
from rest_framework.response import Response
from orders.serializers import (
    OrderDetailSerializer,
    OrderTableSerializer,
    OrderLogSerializer,
    ProductSerializer,
    InvoiceSerializer
)
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from phonenumbers.phonenumberutil import country_code_for_region,region_code_for_number,parse
from phonenumbers import NumberParseException
from utils.custom_logger import get_logger
from django.db.models import Q
from datetime import datetime,time
logger = get_logger(os.path.abspath(__file__).split("/")[-1][:-3])
def check_country_code_exists(number):
    try:
        parsed_number = parse(number, None)
        country_code = parsed_number.country_code
        region_code = region_code_for_number(parsed_number)
        if region_code:
            country = pycountry.countries.get(alpha_2=region_code)
            if country:
                country_name = country.name
                return True, country_code, region_code, country_name
            else:
                return False, None, None, None
        else:
            return False, None, None, None
    except NumberParseException:
        return False, None, None, None


def orderLogInsert(data):
        logData = OrderLogModel.objects.filter(order=data['order'],order_status=data['order_status']).first()
        if logData is None:
            orderLogSerializer = OrderLogSerializer(data=data)
            if orderLogSerializer.is_valid():
                orderInsert = orderLogSerializer.save()
            else:
                raise ValueError(orderLogSerializer.errors)
        
def createOrderDetailsJson(data):
    grossTotalAmount=0
    product_qty=0
    for product in data["product_details"]:
        try:
            products = ProductModel.objects.filter(id=product['product']).first()
            productSerializerData = ProductSerializer(products)
            productData = productSerializerData.data
            total_product_amount=int(productData['product_price']) * int(product['product_qty'])
            product_actual_price=int(total_product_amount) / (1 + (int(productData['product_gst_percent']) / 100))
            product['product_name']=productData['product_name']
            product['product_price']=int(product_actual_price)
            product['product_total_price']=int(int(total_product_amount) / (1 + (int(productData['product_gst_percent']) / 100)))
            product['product_mrp']=int(total_product_amount)
            product['gst_amount']=int(total_product_amount)-int(product_actual_price)
            product['taxeble_amount']=int(total_product_amount)-int(product_actual_price)
            grossTotalAmount+=float(productData['product_price']) * int(product['product_qty'])
            product_qty+=int(product['product_qty'])
        except:
            print("error")
    data['gross_amount']=grossTotalAmount
    data['product_qty']=product_qty
    data['total_amount']=float(grossTotalAmount)-float(data['discount'])-float(data['prepaid_amount'])
    return data

def updateOrderDetailsJson(data,id):
    grossTotalAmount=0
    orderDetailsData = OrderDetail.objects.filter(order=id)
    orderDetailsData.delete()
    discount=0
    prepaid_amount=0
    product_qty=0
    if 'discount' not in data or 'prepaid_amount' not in data:
        orderData = Order_Table.objects.filter(id=id).first()
        orderSerializerData = OrderTableSerializer(orderData)
        orderData = orderSerializerData.data
        discount=orderData['discount']
        prepaid_amount=orderData['prepaid_amount']
    else:
        discount=data['discount']
        prepaid_amount=['prepaid_amount']
    for product in data["product_details"]:
        try:
            products = ProductModel.objects.filter(id=product['product']).first()
            productSerializerData = ProductSerializer(products)
            productData = productSerializerData.data
            total_product_amount=int(productData['product_price']) * int(product['product_qty'])
            product_actual_price=int(total_product_amount) / (1 + (int(productData['product_gst_percent']) / 100))
            product['order']=id
            product['product_name']=productData['product_name']
            product['product_price']=int(product_actual_price)
            product['product_total_price']=int(int(total_product_amount) / (1 + (int(productData['product_gst_percent']) / 100)))
            product['product_mrp']=int(total_product_amount)
            product['gst_amount']=int(total_product_amount)-int(product_actual_price)
            product['taxeble_amount']=int(total_product_amount)-int(product_actual_price)
            grossTotalAmount+=float(productData['product_price']) * int(product['product_qty'])
            product_qty+=int(product['product_qty'])
        except:
            print("error")
    data['gross_amount']=grossTotalAmount
    data['product_qty']=product_qty
    data['total_amount']=float(grossTotalAmount)-float(discount)-float(prepaid_amount)
    return data

def createOrders(data,user_id):
    has_country_code, country_code, region_code, country_name = check_country_code_exists(data['customer_phone'])
    if has_country_code:
        if data['customer_country'].lower()!=country_name.lower():
            raise ValueError("country code or country name not match.")
    else:
        raise ValueError("Phone number does not contain a valid country code.")

    if int(data['repeat_order'])!=1:
        repeatMobileNumber = Order_Table.objects.filter(customer_phone=data['customer_phone']).first()
        if repeatMobileNumber:
            raise ValueError("Phone number exists")
        
    data=createOrderDetailsJson(data)

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
            products = ProductModel.objects.filter(id=product['product']).first()
            productSerializerData = ProductSerializer(products)
            productData = productSerializerData.data
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
    

def updateOrders(id, data,user_id):
    try:
        if 'product_details' in data:
            data=updateOrderDetailsJson(data,id)
        updatedData = Order_Table.objects.get(id=id)
        serializer = OrderTableSerializer(updatedData, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            orderDetailsSerializer = OrderDetailSerializer(data=data["product_details"],many=True)
            if orderDetailsSerializer.is_valid():
                orderDetailsSaveResponce = orderDetailsSerializer.save()
            if 'order_status' in data:
                orderLogInsert({"order":id,"order_status":data["order_status"],"action_by":user_id,"remark":"order updated"})
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
        
def exportOrders(user_id, data):
    userData = UserProfile.objects.filter(user_id=user_id).first()
    if not userData:
        return {"error": "User not found"}
    serializer = UserProfileSerializer(userData)
    userSerializedData = serializer.data
    date_range = data.get('data_range', '').split(' - ')
    if len(date_range) != 2:
        return {"error": "Invalid date range format"}
    try:
        start_date = datetime.strptime(date_range[0], '%m/%d/%Y')
        end_date = datetime.strptime(date_range[1], '%m/%d/%Y')
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)
    except ValueError as e:
        return {"error": f"Invalid date format: {str(e)}"}
    
    if data.get('date_type') == 'created_at':
        date_filter = Q(created_at__range=(start_datetime, end_datetime))
    else:
        date_filter = Q(updated_at__range=(start_datetime, end_datetime))

    filters = Q(branch=userSerializedData.get("branch")) & Q(company=userSerializedData.get("company"))
    filters &= date_filter
    if data.get('status') != 0:
        filters &= Q(order_status=data.get('status'))

    tableData = Order_Table.objects.filter(filters)
    orderTableData = OrderTableSerializer(tableData, many=True)
    return orderTableData.data


def ivoiceDeatail(user_id, data):
    tableData = Order_Table.objects.filter(order_id__in=data['invoices'])
    orderTableData = InvoiceSerializer(tableData, many=True)
    return orderTableData.data