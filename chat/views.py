import sys
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, Group
from .serializers import (
    ChatSerializer,
    ChatGroupSerializer,
    GroupSerializer,
    GroupDetailsSerializer,
)
from accounts.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chat, ChatSession, Group, GroupDetails, User
from rest_framework.permissions import IsAuthenticated


class getChatDetail(APIView):
    serializer_class = ChatSerializer
    # =======================================================================
    #                Retrieve Chat Details
    # =======================================================================

    """
    Fetches chat details between two users or within a specified group.

    This function checks if a `group_id` is provided and attempts to retrieve 
    the corresponding chat session. If `group_id` is not provided, it retrieves 
    the session based on `from_user` and `to_user` parameters. The function also
    updates the chat status for messages where the target user is involved and
    returns the serialized chat data.

    @method get
    @param {Request} request - The HTTP request containing query parameters.
    @return {Response} - The HTTP response with the chat details or an error message.
    """

    def get(self, request):
        from_user = request.query_params.get("from_user")
        to_user = request.query_params.get("to_user")
        group_id = request.query_params.get("group_id")
        if group_id is None:
            if from_user is None:
                return Response(
                    {"Success": False, "Message": "Please pass from_user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if to_user is None:
                return Response(
                    {"Success": False, "Message": "Please pass to_user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if group_id:
            chatSessionId = ChatSession.objects.filter(name=f"{group_id}").first()
        else:
            chatSessionId = (
                ChatSession.objects.filter(name=f"{from_user}_{to_user}").first()
                or ChatSession.objects.filter(name=f"{to_user}_{from_user}").first()
            )

        if chatSessionId is None:
            return Response(
                {"Success": False, "Message": f"Data not exist.!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        filters = {}
        if chatSessionId is not None:
            filters["chat_session_id"] = chatSessionId
        Chat.objects.filter(from_user=to_user, chat_session_id=chatSessionId).update(
            chat_status=0
        )
        chatData = Chat.objects.filter(**filters).order_by("-created_at")
        serializer = ChatSerializer(chatData, many=True)
        return Response({"Success": True, "data": serializer.data})


class createChat(APIView):
    serializer_class = ChatSerializer
    # =======================================================================
    #                Create New Chat Message
    # =======================================================================

    """
    Handles the creation of a new chat message and manages the chat session.

    This function extracts `from_user`, `to_user`, and `chat_type` from the 
    request. It then checks for an existing chat session and creates a new one
    if necessary. The new chat message is serialized and saved. The function 
    returns the serialized chat data and session ID on success or validation 
    errors if the data is invalid.

    @method post
    @param {Request} request - The HTTP request containing chat details.
    @return {Response} - The HTTP response with the chat data, session ID, or errors.
    """

    def post(self, request):
        from_user = request.data.get("from_user")
        to_user = request.data.get("to_user")
        chat_type = request.data.get("chat_type")
        session = None
        if chat_type is None:
            session = (
                Chat.objects.filter(from_user=from_user, to_user=to_user).first()
                or Chat.objects.filter(from_user=to_user, to_user=from_user).first()
            )
        if session:
            session_id = session.chat_session_id
        else:
            if chat_type == "group_chat":
                session = ChatSession.objects.filter(name=f"{to_user}").first()
            else:
                session = (
                    ChatSession.objects.filter(name=f"{from_user}_{to_user}").first()
                    or ChatSession.objects.filter(name=f"{to_user}_{from_user}").first()
                )

            if session:
                session_id = session.id
            else:
                if chat_type == "group_chat":
                    new_session = ChatSession.objects.create(name=f"{to_user}")
                else:
                    new_session = ChatSession.objects.create(
                        name=f"{from_user}_{to_user}"
                    )
                session_id = new_session.id

        serializer = ChatSerializer(data={**request.data, "chat_session": session_id})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"Success": True, "ChatData": serializer.data, "SessionID": session_id},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"Success": False, "Errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class chat_count(APIView):
    # =======================================================================
    #                Count Unread Messages
    # =======================================================================

    """
    Provides the count of unread messages for a specific chat session.

    This function retrieves the `from_user` and `to_user` parameters and finds
    the corresponding chat session. It counts the number of unread messages
    (`chat_status=1`) for the session and returns this count along with the
    session ID. If no session is found, an error response is returned.

    @method get
    @param {Request} request - The HTTP request containing query parameters.
    @return {Response} - The HTTP response with the count of unread messages or an error.
    """

    def get(self, request):
        from_user = request.query_params.get("from_user")
        to_user = request.query_params.get("to_user")
        session = (
            Chat.objects.filter(from_user=from_user, to_user=to_user).first()
            or Chat.objects.filter(from_user=to_user, to_user=from_user).first()
        )
        if session:
            session_id = session.chat_session_id
            chat_count = Chat.objects.filter(
                to_user=to_user, chat_session_id=session_id, chat_status=1
            ).count()
            return Response(
                {"Success": True, "chat_count": chat_count, "SessionID": session_id},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"Success": False, "Errors": "Session not able"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class getUserListChat(APIView):
    # =======================================================================
    #                Retrieve User List for Chat
    # =======================================================================

    """
    Returns a list of users who have had a chat with a specified user.

    This function takes a `user_id` and finds all unique users who have
    chatted with that user. It serializes the user data and returns it in the
    response. If `user_id` is not provided, an error response is returned.

    @method get
    @param {Request} request - The HTTP request containing the user ID.
    @return {Response} - The HTTP response with the list of users or an error message.
    """

    def get(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"Success": False, "Errors": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        unique_to_users = (
            Chat.objects.filter(from_user=user_id)
            .values_list("to_user", flat=True)
            .distinct()
        )
        users = User.objects.filter(id__in=unique_to_users)
        user_serializer = UserSerializer(users, many=True)
        return Response(
            {"Success": True, "results": user_serializer.data},
            status=status.HTTP_200_OK,
        )


class GetGroups(APIView):
    # =======================================================================
    #                Retrieve Groups for User
    # =======================================================================

    """
    Fetches groups associated with a specific user and includes details
    about the group and its members.

    This function retrieves groups where the specified user is a member,
    along with details about each group and its members. It serializes this
    information and returns it in the response. If no groups are found for
    the user, an error response is returned.

    @method get
    @param {Request} request - The HTTP request containing the user ID.
    @return {Response} - The HTTP response with the groups and their details or an error message.
    """

    def get(self, request):
        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"Success": False, "Errors": "user_id is required "},
                status=status.HTTP_400_BAD_REQUEST,
            )
        group_details = (
            GroupDetails.objects.filter(Group_member_id=user_id)
            .select_related("Group")
            .prefetch_related("Group_member")
        )
        if group_details.exists():
            data = []
            unique_groups = group_details.values("Group_id").distinct()
            for group in unique_groups:
                group_id = group["Group_id"]
                group_info = Group.objects.get(id=group_id)
                member_count = GroupDetails.objects.filter(Group_id=group_id).count()
                members_details = GroupDetails.objects.filter(
                    Group_id=group_id
                ).select_related("Group_member")
                members = []
                for detail in members_details:
                    members.append(
                        {
                            "member_id": detail.Group_member.id,
                            "member_name": detail.Group_member.username,
                            "group_id": detail.Group_id,
                            "member_status": detail.Group_member_status,
                        }
                    )
                data.append(
                    {
                        "group_id": group_info.id,
                        "group_name": group_info.group_name,
                        "member_count": member_count,
                        "members": members,
                    }
                )
            return Response(
                {"Success": True, "Groups": data}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Success": False, "Errors": f"No groups found for user_id {user_id}"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CreateGroup(APIView):
    permission_classes = [IsAuthenticated]
    # =======================================================================
    #                Create a New Group
    # =======================================================================

    """
    Creates a new group and adds members to it.

    This function takes `group_name` and `members` data from the request and 
    creates a new group. It then creates `GroupDetails` entries for each 
    member in the new group. The function returns the serialized group data 
    on success or validation errors if any issues occur during creation.

    @method post
    @param {Request} request - The HTTP request containing group and member details.
    @return {Response} - The HTTP response with the group data or errors.
    """

    def post(self, request):
        group_data = request.data.get("group_name")
        members_data = request.data.get("members", [])

        # Create Group
        group_serializer = GroupSerializer(data={"group_name": group_data})
        if group_serializer.is_valid():
            group = group_serializer.save()
        else:
            return Response(
                {"Success": False, "Errors": group_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create GroupDetails for each member
        for member_data in members_data:
            member_serializer = GroupDetailsSerializer(
                data={
                    "Group": group.id,
                    "Group_member": member_data.get("group_member_id"),
                    "Group_member_status": member_data.get(
                        "group_member_status", GroupDetails.GroupMemberType.USER
                    ),
                }
            )
            if member_serializer.is_valid():
                member_serializer.save()
            else:
                return Response(
                    {"Success": False, "Errors": member_serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"Success": True, "Group": group_serializer.data},
            status=status.HTTP_201_CREATED,
        )
