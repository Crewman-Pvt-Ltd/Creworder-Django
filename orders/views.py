from rest_framework import status
from rest_framework.response import Response
from .models import Order_Table, OrderDetail, CategoryModel,ProductModel
from .serializers import OrderTableSerializer, OrderDetailSerializer, CategorySerializer,ProductSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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


class OrderAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                order = Order_Table.objects.get(pk=pk)
                serializer = OrderTableSerializer(order)
            except Order_Table.DoesNotExist:
                return Response(
                    {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            orders = Order_Table.objects.all()
            serializer = OrderTableSerializer(orders, many=True)
        return Response(serializer.data)

    # Order Create Function
    def post(self, request, *args, **kwargs):
        if (
            "product_details" not in request.data
            or request.data["product_details"] != None
        ):
            productData = request.data["product_details"]
            request.data["product_details"] = "Product Datails exist"
        serializer = OrderTableSerializer(data=request.data)
        if serializer.is_valid():
            OrderData = serializer.save()
            for product in productData:
                product["order_id"] = OrderData.id
                productSerializer = OrderDetailSerializer(data=product)
                if productSerializer.is_valid():
                    productSerializer.save()
                else:
                    order_instance = Order_Table.objects.get(pk=OrderData.id)
                    order_instance.delete()
                    return Response(
                        productSerializer.errors, status=status.HTTP_201_CREATED
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Order Function Delete Function
    def delete(self, request, pk, *args, **kwargs):
        try:
            order_instance = Order_Table.objects.get(pk=pk)
            order_instance.delete()
            return Response(
                {"message": "Order deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Order_Table.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk=None, *args, **kwargs):
        if not pk:
            return Response(
                {"error": "Order ID is required for update"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order_instance = Order_Table.objects.get(pk=pk)
        except Order_Table.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if (
            "product_details" in request.data
            and request.data["product_details"] is not None
        ):
            productData = request.data["product_details"]
            request.data["product_details"] = "Product Details exist"
        else:
            productData = []
        serializer = OrderTableSerializer(order_instance, data=request.data)
        if serializer.is_valid():
            OrderData = serializer.save()
            for product in productData:
                if "id" in product:
                    try:
                        product_instance = OrderDetail.objects.get(pk=product["id"])
                        productSerializer = OrderDetailSerializer(
                            product_instance, data=product
                        )
                    except OrderDetail.DoesNotExist:
                        productSerializer = OrderDetailSerializer(data=product)
                else:
                    product["order_id"] = OrderData.id
                    productSerializer = OrderDetailSerializer(data=product)

                if productSerializer.is_valid():
                    productSerializer.save()
                else:
                    return Response(
                        productSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request):
        try:
            data = getCategory(request.user.id)
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

    def get(self, request):
        try:
            data = getProduct(request.user.id)
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
