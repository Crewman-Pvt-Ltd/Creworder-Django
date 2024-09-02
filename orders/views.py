import pdb

from rest_framework import status
from rest_framework.response import Response
from .models import Order_Table, OrderDetail, CategoryModel,ProductModel
from .serializers import OrderTableSerializer, OrderDetailSerializer, CategorySerializer,ProductSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from utils.custom_logger import get_logger
import traceback
from services.category.category_service import (
    createCategory,
    updateCategory,
    deleteCategory,
    getCategory,
)
from services.products.products_service import (
    createProduct,
    updateProduct,
    deleteProduct,
    getProduct,
)
from services.orders.order_service import createOrders,updateOrders,deleteOrder,getOrderDetails,exportOrders
logger = get_logger('ordersView')
class OrderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            orderSerializer = OrderTableSerializer(data=request.data)
            if orderSerializer.is_valid():
                createOrdersResponse = createOrders(request.data, request.user.id)
                return Response(
                    {
                        "Success": True,
                        "data": OrderTableSerializer(createOrdersResponse).data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            logger.error(f"{traceback.format_exc()}")
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


    def get(self, request, pk=None):
        try:
            data = getOrderDetails(request.user.id,pk)
            return Response(
                {"Success": True, "Data": data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    
    def delete(self, request, pk):
        success = deleteOrder(pk)
        if success:
            return Response(
                {"Success": True, "Message": "Deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"Success": False, "Error": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
    def put(self, request, pk):
        try:
            updatedData = updateOrders(pk, request.data)
            if updatedData:
                return Response(
                    {
                        "Success": True,
                        "data": OrderTableSerializer(updatedData).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Success": False,
                        "Error": "Order not found or invalid data provided.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except CategoryModel.DoesNotExist:
            return Response(
                {
                    "Success": False,
                    "Error": "Order not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order_Table.objects.all()
    serializer_class = OrderTableSerializer


class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            createCategoryResponse = createCategory(request.data, request.user.id)
            return Response(
                {
                    "Success": True,
                    "data": CategorySerializer(createCategoryResponse).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk):  # Changed from 'id' to 'pk'
        try:
            updatedData = updateCategory(pk, request.data)
            if updatedData:
                return Response(
                    {
                        "Success": True,
                        "data": CategorySerializer(updatedData).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Success": False,
                        "Error": "Category not found or invalid data provided.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except CategoryModel.DoesNotExist:
            return Response(
                {
                    "Success": False,
                    "Error": "Category not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        success = deleteCategory(pk)
        if success:
            return Response(
                {"Success": True, "Message": "Deleted successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"Success": False, "Error": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get(self, request, pk=None):
        try:
            data = getCategory(request.user.id, pk)
            serializer = CategorySerializer(data, many=True)
            return Response(
                {"Success": True, "Data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            createCategoryResponse = createProduct(request.data, request.user.id)
            return Response(
                {
                    "Success": True,
                    "data": ProductSerializer(createCategoryResponse).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request, pk):
        try:
            updatedData = updateProduct(pk, request.data)
            if updatedData:
                return Response(
                    {
                        "Success": True,
                        "data": ProductSerializer(updatedData).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Success": False,
                        "Error": "Product not found or invalid data provided.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except ProductModel.DoesNotExist:
            return Response(
                {
                    "Success": False,
                    "Error": "Category not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, pk):
        success = deleteProduct(pk)
        if success:
            return Response(
                {"Success": True, "Message": "Deleted successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"Success": False, "Error": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def get(self, request, pk):
        try:
            data = getProduct(request.user.id,pk)
            serializer = ProductSerializer(data, many=True)
            return Response(
                {"Success": True, "Data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer

class CategorytDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer

class orderExport(APIView):
    def post(self, request, *args, **kwargs):
        if "data_range" not in request.data or request.data['data_range']=='' or "date_type" not in request.data or request.data['date_type']=='' or "status" not in request.data or request.data['status']=='':
            return Response({"success":False,"massage":"data_range ,date_type and status all fields are mandatory and not pass empty"},status=status.HTTP_400_BAD_REQUEST)
        data = exportOrders(request.user.id,request.data)
        return Response({"success": True, "Data":data},status=status.HTTP_200_OK)
