from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FollowUp
from .serializers import FollowUpSerializer
from services.follow_up.follow_up_service import (
    createFollowUp,
    getFollowUpsbyuser,
    deleteFollowUp,
    updateFollowUp,
)
from rest_framework.permissions import IsAuthenticated


class CreateFollowUp(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            follow_up = createFollowUp(request.data)
            return Response(
                {
                    "Success": True,
                    "data": FollowUpSerializer(follow_up).data,
                    "id": follow_up.id,
                },
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            return Response(
                {"Success": False, "Errors": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class FollowUpList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            user_id = None
        try:
            follow_ups = getFollowUpsbyuser(user_id)
            serializer = FollowUpSerializer(follow_ups, many=True)
            return Response(
                {"Success": True, "FollowUps": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FollowUpDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, follow_up_id):
        success = deleteFollowUp(follow_up_id)
        if success:
            return Response(
                {"Success": True, "Message": "Follow-up deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"Success": False, "Error": "Follow-up not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class FollowUpUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, follow_up_id):
        follow_up = updateFollowUp(follow_up_id, request.data)

        if follow_up:
            return Response(
                {"Success": True, "FollowUp": FollowUpSerializer(follow_up).data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "Success": False,
                    "Error": "Follow-up not found or invalid data provided.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
