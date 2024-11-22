from django.shortcuts import render
from rest_framework.views import APIView
from django.db import transaction
from rest_framework import viewsets, status
from services.cloud_telephoney.cloud_telephoney_service import (
    createCloudTelephoneyChannel,
    deleteCloudTelephoneyChannel,
    updateCloudTelephoneyChannel,
    getCloudTelephoneyChannel,
    createCloudTelephoneyChannelAssign,
    updateCloudTelephoneyChannelAssign,
    deleteCloudTelephoneyChannelAssign
)
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CloudTelephonyChannelSerializer,
    CloudTelephonyChannelAssignSerializer,
    UserMailSetUpSerializers
)
import pdb
from .models import UserMailSetup

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
                {"Success": True, "Data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class CloudtelephoneyChannelAssignForUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            cloud_telephony_channel = createCloudTelephoneyChannelAssign(
                request.data, request.user.id
            )
            if isinstance(cloud_telephony_channel, str):
                return Response(
                    {"Success": False, "Errors": cloud_telephony_channel},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {
                    "Success": True,
                    "data": CloudTelephonyChannelAssignSerializer(cloud_telephony_channel).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Errors": "An unexpected error occurred: " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CloudTelephoneyChannelAssignUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, id):
        updatedData = updateCloudTelephoneyChannelAssign(id, request.data)
        if updatedData:
            return Response(
                {
                    "Success": True,
                    "data": CloudTelephonyChannelAssignSerializer(updatedData).data,
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
        
class CloudTelephoneyChannelAssignDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        success = deleteCloudTelephoneyChannelAssign(id)
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
class UserMailSetupView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset =UserMailSetup.objects.all()
    serializer_class= UserMailSetUpSerializers

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
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

