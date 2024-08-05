import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, ChatSession
from .serializers import ChatSerializer

class getChatDetail(APIView):
    serializer_class = ChatSerializer
    def get(self, request):
        from_user = request.query_params.get('from_user')
        to_user = request.query_params.get('to_user')
        if from_user is None:
            return Response({"Success": False, "Message": "Please pass from_user"}, status=status.HTTP_400_BAD_REQUEST)
        if to_user is None:
            return Response({"Success": False, "Message": "Please pass to_user"}, status=status.HTTP_400_BAD_REQUEST)

        chatSessionId = ChatSession.objects.filter(name=f"{from_user}_{to_user}").first() or ChatSession.objects.filter(name=f"{to_user}_{from_user}").first()
        if chatSessionId is None:
            return Response({"Success": False, "Message": f"Data not exist.!" }, status=status.HTTP_400_BAD_REQUEST)
        
        filters = {}
        if chatSessionId is not None:
            filters['chat_session_id'] = chatSessionId
        Chat.objects.filter(from_user=to_user, chat_session_id=chatSessionId).update(chat_status=0)
        chatData = Chat.objects.filter(**filters).order_by('-created_at')
        serializer = ChatSerializer(chatData, many=True)
        return Response({"Success": True, "data": serializer.data})


class createChat(APIView):
    serializer_class = ChatSerializer
    def post(self, request):
        from_user = request.data.get('from_user')
        to_user = request.data.get('to_user')
        session = Chat.objects.filter(from_user=from_user, to_user=to_user).first() or Chat.objects.filter(from_user=to_user, to_user=from_user).first()
        if session:
            session_id = session.chat_session_id
        else:
            session = ChatSession.objects.filter(name=f"{from_user}_{to_user}").first() or ChatSession.objects.filter(name=f"{to_user}_{from_user}").first()
            if session:
                session_id = session.id
            else:
                new_session = ChatSession.objects.create(name=f"{from_user}_{to_user}")
                session_id = new_session.id

        serializer = ChatSerializer(data={**request.data, 'chat_session': session_id})
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": True, "ChatData": serializer.data, "SessionID": session_id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Success": False, "Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class chat_count(APIView):
    def get(self, request):
        from_user = request.query_params.get('from_user')
        to_user = request.query_params.get('to_user')
        session = Chat.objects.filter(from_user=from_user, to_user=to_user).first() or Chat.objects.filter(from_user=to_user, to_user=from_user).first()
        if session:
            session_id = session.chat_session_id
            chat_count = Chat.objects.filter(to_user=to_user, chat_session_id=session_id,chat_status=1).count()
            return Response({"Success": True, "chat_count": chat_count, "SessionID": session_id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Success": False, "Errors": "Session not able"}, status=status.HTTP_400_BAD_REQUEST)

