from django.shortcuts import render
from rest_framework.views import APIView
from services.cloud_telephoney.cloud_telephoney_service import createCloudTelephoneyChannel,deleteCloudTelephoneyChannel
from rest_framework.permissions import IsAuthenticated
from .serializers import CloudTelephonyChannelSerializer
import pdb

from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CreateCloudTelephoneyChannel(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            CloudTelephonyChannel = createCloudTelephoneyChannel(request.data,request.user.id)
            return Response(
                {
                    "Success": True,
                    "data": CloudTelephonyChannelSerializer(CloudTelephonyChannel).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

class CloudTelephoneyChannelDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        success = deleteCloudTelephoneyChannel(id)
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

