from django.shortcuts import render
from rest_framework.views import APIView
from services.cloud_telephoney.cloud_telephoney_service import (
    createCloudTelephoneyChannel,
    deleteCloudTelephoneyChannel,
    updateCloudTelephoneyChannel,
    getCloudTelephoneyChannel,
)
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
            CloudTelephonyChannel = createCloudTelephoneyChannel(
                request.data, request.user.id
            )
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


class CloudTelephoneyChannelUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        updatedData = updateCloudTelephoneyChannel(id, request.data)
        if updatedData:
            return Response(
                {
                    "Success": True,
                    "data": CloudTelephonyChannelSerializer(updatedData).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "Success": False,
                    "Error": "Not found or invalid data provided.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )


class CloudTelephoneyChannelList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data = getCloudTelephoneyChannel(request.user.id)
            serializer = CloudTelephonyChannelSerializer(data, many=True)
            return Response(
                {"Success": True, "FollowUps": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
