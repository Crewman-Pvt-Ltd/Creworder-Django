from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class GetUserDashboardtiles(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.has_perm('accounts.can_approve_disapprove_leave'):
            return Response(
                {
                    "status": True,
                    "message": "Data fetched successfully",
                    "data": {"name": "John Doe", "email": "john.doe@example.com"},
                    "errors": None,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": False,
                    "message": "Permission Denied",
                    "errors": "You do not have permission to view this resource.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )