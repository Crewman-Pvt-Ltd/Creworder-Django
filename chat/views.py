import sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer,ChatGroupDetailsSerializer,ChatGroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, ChatSession,Group,GroupDetails

class getChatDetail(APIView):
    serializer_class = ChatSerializer
    def get(self, request):
        from_user = request.query_params.get('from_user')
        to_user = request.query_params.get('to_user')
        group_id = request.query_params.get('group_id')
        if group_id is None:
            if from_user is None:
                return Response({"Success": False, "Message": "Please pass from_user"}, status=status.HTTP_400_BAD_REQUEST)
            if to_user is None:
                return Response({"Success": False, "Message": "Please pass to_user"}, status=status.HTTP_400_BAD_REQUEST)

        if group_id: 
            chatSessionId = ChatSession.objects.filter(name=f"{group_id}").first()
        else:
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
        chat_type=request.data.get('chat_type')
        session =None
        if chat_type is None:
            session = Chat.objects.filter(from_user=from_user, to_user=to_user).first() or Chat.objects.filter(from_user=to_user, to_user=from_user).first()
        if session:
            session_id = session.chat_session_id
        else:
            if chat_type=='group_chat':
                session = ChatSession.objects.filter(name=f"{to_user}").first()
            else:
                session = ChatSession.objects.filter(name=f"{from_user}_{to_user}").first() or ChatSession.objects.filter(name=f"{to_user}_{from_user}").first()

            if session:
                session_id = session.id
            else:
                if chat_type=='group_chat':
                   new_session = ChatSession.objects.create(name=f"{to_user}")
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
        
class GetGroups(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({"Success": False, "Errors": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        group_details = GroupDetails.objects.filter(Group_member_id=user_id).select_related('Group').prefetch_related('Group_member')
        if group_details.exists():
            data = []
            unique_groups = group_details.values('Group_id').distinct()
            for group in unique_groups:
                group_id = group['Group_id']
                group_info = Group.objects.get(id=group_id)
                member_count = GroupDetails.objects.filter(Group_id=group_id).count()
                members_details = GroupDetails.objects.filter(Group_id=group_id).select_related('Group_member')
                members = []
                for detail in members_details:
                    members.append({
                        'member_id': detail.Group_member.id,
                        'member_name': detail.Group_member.username,
                        'group_id': detail.Group_id,
                        'member_status': detail.Group_member_status
                    })
                data.append({
                    'group_id': group_info.id,
                    'group_name': group_info.group_name,
                    'member_count': member_count,
                    'members': members 
                })
            return Response({"Success": True, "Groups": data}, status=status.HTTP_200_OK)
        else:
            return Response({"Success": False, "Errors": f"No groups found for user_id {user_id}"}, status=status.HTTP_404_NOT_FOUND)



