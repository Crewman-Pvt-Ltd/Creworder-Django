import json
import requests
import logging
from accounts.models import UserProfile, PickUpPoint
from accounts.serializers import UserProfileSerializer, PickUpPointSerializer
from shipment.models import ShipmentModel
from shipment.serializers import ShipmentSerializer
from orders.models import Order_Table,OrderLogModel
from orders.serializers import OrderTableSerializer
from django.core.exceptions import ObjectDoesNotExist
from utils.custom_logger import setup_logging

logger = logging.getLogger(__name__)
setup_logging(log_file='logs/shipment_service.log', log_level=logging.WARNING)

class ShiprocketScheduleOrder:
    """
    A class to handle Shiprocket scheduling orders.
    """
    LOGIN_URL='https://apiv2.shiprocket.in/v1/external/auth/login'
    SERVICEABILITY='https://apiv2.shiprocket.in/v1/external/courier/serviceability/'
    CREATE_ORDER='https://apiv2.shiprocket.in/v1/external/orders/create/adhoc'
    GET_AWB='https://apiv2.shiprocket.in/v1/external/courier/assign/awb'
    base_url="https://apiv2.shiprocket.in/v1"
    token=''
    def __init__(self,email:str,password:str):
        """
        Initializes the ShiprocketScheduleOrder class with API credentials.

        :param api_key: API key for authenticating requests.
        :param base_url: Base URL for Shiprocket API.
        """
        self.email=email
        self.password=password
        self.base_url = self.base_url
        self.token=self._get_token(self.email,self.password)
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def _get_token(self, email: str, password: str) -> str:
        """
        Private method to get the Shiprocket token.
        """
        url = f"{self.base_url}/external/auth/login"
        payload = json.dumps({
            "email": email,
            "password": password
        })

        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, data=payload)
            response.raise_for_status()
            return response.json().get('token')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching token: {e}")
            return None

    @staticmethod
    def makeJsonForApi(order_data: dict) -> bool:
        """
        Static method to validate order data before scheduling.
        :param order_data: Dictionary containing order details.
        :return: True if valid, False otherwise.
        """
        _itemsList = []
        if order_data['order_details']:
            for _item in order_data['order_details']:
                _itemDict = { 
                    "name": _item["product_name"],
                    "sku": _item["product_sku"],
                    "selling_price": _item["product_price"],
                    "units": _item["product_qty"],
                }
                _itemsList.append(_itemDict)
            
        _RequestJson = {
            "order_id": f"{order_data['order_id']}",
            "order_date": f"{order_data['created_at']}",
            "pickup_location": "Home",
            "channel_id": "",
            "comment": f"{order_data['order_remark']}",
            "billing_customer_name": f"{order_data['customer_name']}",
            "billing_last_name": "",
            "billing_address": f"{order_data['customer_address']}",
            "billing_address_2": "",
            "billing_city": f"{order_data['customer_city']}",
            "billing_pincode": f"{order_data['customer_postal']}",
            "billing_state": f"{order_data['customer_state_name']}",
            "billing_country": order_data['customer_country'],
            "billing_email": "",
            "billing_phone": f"{order_data['customer_phone']}",
            "shipping_is_billing": True,
            "shipping_customer_name": f"{order_data['customer_name']}",
            "shipping_last_name": "",
            "shipping_address": f"{order_data['customer_address']}",
            "shipping_address_2": "",
            "shipping_city": order_data['customer_city'],
            "shipping_pincode": f"{order_data['customer_postal']}",
            "shipping_country": order_data['customer_country'],
            "shipping_state": f"{order_data['customer_state_name']}",
            "shipping_email": "",
            "shipping_phone": f"{order_data['customer_phone']}",
            "order_items": _itemsList,
            "payment_method": f"{order_data['payment_type_name']}",
            "shipping_charges": 0,
            "giftwrap_charges": 0,
            "transaction_charges": 0,
            "total_discount": 0,
            "sub_total": order_data['total_amount'],
            "length": "13",
            "breadth": "13",
            "height": "8",
            "weight": "0.5"
        }
        return  _RequestJson

    def schedule_order(self, order_list:list, branch_id:int ,company_id:int):
        """
        Public method to schedule an order using the Shiprocket API.

        :param order_data: Dictionary containing order details.
        :return: Response from the Shiprocket API.
        """
        OrdersData = Order_Table.objects.filter(branch=branch_id,company=company_id,id__in=order_list)
        OrdersDataSerializer = OrderTableSerializer(OrdersData, many=True)
        _OrderLogJson=[]
        _ResponsesDict=[]
        for order in OrdersDataSerializer.data:
            _request_json=self.makeJsonForApi(order)
            response = requests.post(self.CREATE_ORDER, headers=self.headers, data=json.dumps(_request_json))
            if response.status_code == 200:
                if response.json()['status']=='NEW':
                    _awbJson = {
                            "shipment_id": response.json()['shipment_id'],
                            "courier_id": "",
                            "status": ""
                        }
                    try:
                        response = requests.post(self.GET_AWB, headers=self.headers, json=_awbJson)
                        response.raise_for_status()
                        result1 = response.json()
                        UpdateInstance = Order_Table.objects.filter(branch=branch_id, company=company_id, id=order['id'])
                        UpdateInstance.update(order_wayBill='232442442424242', order_ship_by='another_value', is_booked=1)
                        _logJson = { 
                            'order':order['id'] ,
                            'order_status' : 5,
                            'action_by' : 1,
                            'remark' :'order schedule',
                            }
                        _OrderLogJson.append(_logJson)
                        print("Response:", result1)
                    except requests.exceptions.RequestException as e:
                        _ResponsesDict.append({"order":f"{order['order_id']}","massage":f"{e}"})
                        print("An error occurred:", e)
                else:
                    _ResponsesDict.append({"order":f"{order['order_id']}","massage":f"Created but order status on shiprocket {response.json()['status']}"})
            else:
                _ResponsesDict.append({"order":f"{order['order_id']}","massage":f"{response.text}"})
                print("Request Failed")
                print(f"Status Code: {response.status_code}")
                print(response.text)
        # OrderLogModel
        return _ResponsesDict