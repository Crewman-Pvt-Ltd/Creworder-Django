from django.shortcuts import render

from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LeadModel
from .serializers import LeadSerializer
from services.lead_management.lead_management_service import createLead,updateLead,deleteLead,getLead

class LeadCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        createRes=createLead(request.data,request.user.id)
        if createRes.errors:
            return Response(createRes.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(createRes.data, status=status.HTTP_201_CREATED)


    def get(self, request, pk=None, *args, **kwargs):
        try:
            getRes=getLead(request.user.id,pk)
            serializerData = LeadSerializer(getRes, many=True)
            return Response(
                    {"Success": True, "Data": serializerData.data},
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                    {"Success": False, "Error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


    def delete(self, request, pk, *args, **kwargs):
        success = deleteLead(pk)
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
            updatedData = updateLead(pk, request.data)
            if updatedData:
                return Response(
                    {
                        "Success": True,
                        "data": LeadSerializer(updatedData).data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Success": False,
                        "Error": "Lead not found or invalid data provided.",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except LeadModel.DoesNotExist:
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