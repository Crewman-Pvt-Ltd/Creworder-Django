from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer

class getChatDetail(APIView):
    serializer_class = ChatSerializer
    def get(self, request):
        user_id = request.query_params.get('user_id')
        from_user = request.query_params.get('from_user')
        to_user = request.query_params.get('to_user')
        if from_user is None:
            return Response({"Success": False, "Message": "Please pass from_user"}, status=status.HTTP_400_BAD_REQUEST)
        if to_user is None:
            return Response({"Success": False, "Message": "Please pass to_user"}, status=status.HTTP_400_BAD_REQUEST)

        filters = {}
        if user_id is not None:
            filters['user_id'] = user_id
        if from_user is not None:
            filters['from_user_id'] = from_user
        if to_user is not None:
            filters['to_user_id'] = to_user

        chatData = Chat.objects.filter(**filters)
        serializer = ChatSerializer(chatData, many=True)
        return Response({"Success": True, "data": serializer.data})

    
class createChat(APIView):
    serializer_class = ChatSerializer
    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": True, "ChatData": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Success": False, "Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

