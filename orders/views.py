from rest_framework import status
from rest_framework.response import Response
from .models import Order_Table, OrderDetail
from .serializers import OrderTableSerializer,OrderDetailSerializer
from rest_framework.views import APIView

class OrderAPIView(APIView):
    queryset = Order_Table.objects.all()
    serializer_class = OrderTableSerializer
    def get(self, request):
        return Response({"Success" : True})
    
    def post(self, request, *args, **kwargs):
        if 'product_details' not in request.data or request.data['product_details']!=None: 
            productData=request.data['product_details']
            request.data['product_details']='Product Datails exist'
        
        serializer = OrderTableSerializer(data=request.data)
        if serializer.is_valid():
            OrderData=serializer.save()
            for product in productData:
                product['order_id']=OrderData.id
                productSerializer = OrderDetailSerializer(data=product)
                if productSerializer.is_valid():
                    productSerializer.save()
                else:
                    return Response(productSerializer.errors, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args, **kwargs):
        try:
            order_instance = Order_Table.objects.get(pk=pk)
            order_instance.delete()
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Order_Table.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

