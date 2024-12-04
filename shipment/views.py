from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ShipmentSerializer,CourierServiceSerializer
from .models import CourierServiceModel
from rest_framework import viewsets, status
from rest_framework import status
from rest_framework.response import Response
from services.shipment.shipment_service import *
from services.shipment.schedule_orders import ShiprocketScheduleOrder
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
class ShipmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            createCategoryResponse = createShipment(request.data, request.user.id)
            return Response(
                {
                    "Success": True,
                    "data": ShipmentSerializer(createCategoryResponse).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, pk=None):
        try:
            data = getShipment(request.user.id,pk)
            serializer = ShipmentSerializer(data, many=True)
            return Response(
                {"Success": True, "Data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
    def delete(self, request, pk):
        success = deleteShipment(pk)
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
    
    def put(self, request, pk):
        try:
            updatedData = updateShipment(pk, request.data)
            if updatedData:
                return Response(
                    {
                        "Success": True,
                        "data": ShipmentSerializer(updatedData).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Success": False,
                        "Error": "Shipment not found or invalid data provided.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except ShipmentModel.DoesNotExist:
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

# class CheckServiceability(APIView):
#     def get(self, request, pk=None):
#         data = checkServiceability(request.user.profile.branch_id,request.user.profile.company_id, request.data['pincode'])
#         if data:
#             return Response(
#                 {
#                     "success": True,
#                     "data": data,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {
#                     "success": False,
#                     "data": {"massage":f"Non serviceable {request.data['pincode']}"},
#                 },
#                 status=status.HTTP_404_NOT_FOUND,
#             )

class CourierServiceView(viewsets.ModelViewSet):
    queryset = CourierServiceModel.objects.all()
    serializer_class = CourierServiceSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        if 'branch' not in request.data:
            request.data['branch'] = user.profile.branch.id 
        request.data['company'] = user.profile.company.id
        return super().create(request, *args, **kwargs)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if 'company' not in request.data:
            request.data['company'] = instance.company.id 
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class ScheduleOrders(viewsets.ModelViewSet):
    queryset = ShipmentModel.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        trackdata = ShipmentModel.objects.filter(branch=request.user.profile.branch.id,company=request.user.profile.company.id,status=1)
        serializer = ShipmentSerializer(trackdata, many=True)
        serialized_data = serializer
        for shipmentData in serialized_data.data:
            if shipmentData['provider_name'].lower()=='shiprocket':
                if shipmentData['credential_username']!='' or shipmentData['credential_username']!=None:
                    shiprocket_service = ShiprocketScheduleOrder(shipmentData['credential_username'],shipmentData['credential_password'])
                    _response=shiprocket_service.schedule_order([35,34,33,37], request.user.profile.branch.id, request.user.profile.company.id)
        if _response:
            return Response(
                {
                    "data":_response
                },
                status=status.HTTP_200_OK,
            )