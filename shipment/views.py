from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ShipmentSerializer
from rest_framework import status
from rest_framework.response import Response
from services.shipment.shipment_service import *
from rest_framework.permissions import IsAuthenticated
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

