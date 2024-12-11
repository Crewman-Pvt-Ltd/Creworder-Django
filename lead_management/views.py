from django.shortcuts import render

from rest_framework import generics, permissions , viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LeadModel, LeadSourceModel
from .serializers import LeadSerializer, LeadSourceModelSerializer
from services.lead_management.lead_management_service import createLead,updateLead,deleteLead,getLead
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoObjectPermissions

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
        
class LeadSourceModelViewSet(viewsets.ModelViewSet):
    queryset = LeadSourceModel.objects.all()
    serializer_class = LeadSourceModelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new LeadSource entry with the user's branch and company.
        """
        # Get the authenticated user
        user = request.user
        branch = user.profile.branch
        company = user.profile.company
        print(branch,company,"-----------------------------")
        # Add the branch and company to the data before creating
        request_data = request.data.copy()  # Make a mutable copy of the request data
        request_data['branch'] = branch.get('id') if branch else None
        request_data['company'] = company.get('id') if company else None

        # Use the modified data to create a new LeadSource entry
        serializer = self.get_serializer(data=request_data)
        if serializer.is_valid():
            # Save the new LeadSource entry
            lead_source = serializer.save()

            # Return a custom response
            return Response({
                "Success": True,
                "Message": "Lead Source created successfully",
                "Data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        # If validation fails, return an error response
        return Response({
            "Success": False,
            "Message": "Failed to create Lead Source",
            "Errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single LeadSource entry.
        """
        # Get the lead source object based on the primary key
        lead_source = self.get_object()
        # Serialize the lead source data
        serializer = self.get_serializer(lead_source)
        
        return Response({
            "Success": True,
            "Data": serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """
        Update a LeadSource entry with the provided data.
        """
        # Get the authenticated user
        user = request.user
        branch = user.profile.branch
        company = user.profile.company
        print(branch,company,"-----------------------------")
        # Add the branch and company to the request data
        request_data = request.data.copy()  # Make a mutable copy of the request data
        request_data['branch'] = branch.get('id') if branch else None
        request_data['company'] = company.get('id') if company else None

        # Get the lead source instance to update
        lead_source = self.get_object()

        # Serialize the data and update the lead source instance
        serializer = self.get_serializer(lead_source, data=request_data, partial=False)  # partial=False means full update
        if serializer.is_valid():
            updated_lead_source = serializer.save()

            return Response({
                "Success": True,
                "Message": "Lead Source updated successfully",
                "Data": serializer.data
            }, status=status.HTTP_200_OK)

        # If validation fails, return an error response
        return Response({
            "Success": False,
            "Message": "Failed to update Lead Source",
            "Errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a LeadSource entry.
        """
        # Get the authenticated user
        user = request.user
        branch = user.profile.branch
        company = user.profile.company

        # Add the branch and company to the request data
        request_data = request.data.copy()  # Make a mutable copy of the request data
        request_data['branch'] = branch.get('id') if branch else None
        request_data['company'] = company.get('id') if company else None

        # Get the lead source instance to update
        lead_source = self.get_object()

        # Serialize the data and update the lead source instance
        serializer = self.get_serializer(lead_source, data=request_data, partial=True)  # partial=True allows partial update
        if serializer.is_valid():
            updated_lead_source = serializer.save()

            return Response({
                "Success": True,
                "Message": "Lead Source partially updated successfully",
                "Data": serializer.data
            }, status=status.HTTP_200_OK)

        # If validation fails, return an error response
        return Response({
            "Success": False,
            "Message": "Failed to partially update Lead Source",
            "Errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # Get the lead source instance to delete
        lead_source = self.get_object()

        # Delete the lead source instance
        lead_source.delete()

        return Response({
            "Success": True,
            "Message": "Lead Source deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Optionally filter the queryset based on the authenticated user's branch and company.
        """
        user = self.request.user
        return LeadSourceModel.objects.filter(company=user.profile.company, branch=user.profile.branch)