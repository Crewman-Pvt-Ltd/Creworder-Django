from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from guardian.shortcuts import get_objects_for_user
import pdb
from datetime import datetime
import random

from .models import User, Company, Package, UserRole, UserProfile, Notice, Branch, FormEnquiry, SupportTicket, Module, \
    Department, Designation, Leave, Holiday, Award, Appreciation, Shift, Attendance
from .serializers import UserSerializer, CompanySerializer, PackageSerializer, UserRoleSerializer, \
    UserProfileSerializer, NoticeSerializer, BranchSerializer, UserSignupSerializer, FormEnquirySerializer, \
    SupportTicketSerializer, ModuleSerializer, DepartmentSerializer, DesignationSerializer, LeaveSerializer, \
    HolidaySerializer, AwardSerializer, AppreciationSerializer, ShiftSerializer, AttendanceSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoObjectPermissions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data=serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.all()
        if user.role.role == "superadmin":
            queryset = User.objects.filter(role__role=user.role.role)
        elif user.role.role == "admin" or user.role.role == "agent":
            branch = user.profile.branch
            queryset = User.objects.filter(profile__branch=branch).exclude(id=user.id)
        return queryset


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]

    def get_queryset(self):
        user = self.request.user

        queryset = get_objects_for_user(user, 'accounts.view_company', klass=Company)

        if user.has_perm('accounts.can_view_own_company'):
            own_queryset = Company.objects.filter(created_by=user)
            queryset = queryset | own_queryset

        if not queryset.exists():
            raise PermissionDenied("You do not have permission to view any companies.")

        return queryset


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.role.role == "admin" or user.role.role == "agent":
            company = user.profile.company
            queryset = Branch.objects.filter(company=company)
        else:
            queryset = Branch.objects.all()
        return queryset


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Notice.objects.filter(created_by=user)
        return queryset


class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        guardian_permissions = user.get_all_permissions()
        user_data = UserSerializer(user, many=False).data
        profile = UserProfileSerializer(user.profile, many=False).data
        user_data['profile'] = profile
        role = user.role.role
        response_data = {"user": user_data, "role": role, "permissions": guardian_permissions}
        return Response(response_data)


class GetSpecificUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role.role == "superadmin":
            users = User.objects.filter(role__role="admin")
        elif user.role.role == "admin":
            company = user.profile.company
            users = User.objects.filter(profile__company=company).exclude(id=user.id)
        users_data = UserSerializer(users, many=True)
        # pdb.set_trace()
        return Response({"results": users_data.data})


class AdminSelfSignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data.get('user')

        user_serializer = UserSignupSerializer(data=user_data)

        if user_serializer.is_valid():
            user_serializer.save()

            return Response({
                'message': 'Signup Successful.'
            }, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormEnquiryViewSet(viewsets.ModelViewSet):
    queryset = FormEnquiry.objects.all()
    serializer_class = FormEnquirySerializer


class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class GetNoticesForUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = user.notices.all()
        serialized_data = NoticeSerializer(data, many=True).data
        return Response({"results": serialized_data})


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DesignationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class LeaveViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer


class HolidayViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


class AwardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


class AppreciationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Appreciation.objects.all()
    serializer_class = AppreciationSerializer


class ShiftViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class GetUsernameSuggestions(APIView):
    permission_classes = [IsAuthenticated]

    def generate_username_suggestions(self, firstname, lastname, date_of_birth):
        base_username = (firstname[::-1] + lastname[:random.randint(1, 5)] + date_of_birth.strftime('%Y')).lower()
        base_username = base_username[:20]

        existing_usernames = set(
            User.objects.filter(username__startswith=base_username)
            .values_list('username', flat=True)
        )

        suggestions = []
        for i in range(1, 30):
            suggestion = base_username[:15] + str(random.randint(100, 999))
            if suggestion not in existing_usernames and len(suggestions) < 5:
                suggestions.append(suggestion)
            if len(suggestions) == 5:
                break

        return suggestions

    def post(self, request):
        firstname = request.data.get('firstname', '')
        lastname = request.data.get('lastname', '')
        date_of_birth = request.data.get('date_of_birth', '')

        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
        except ValueError:
            return Response({"error": "Invalid date_of_birth format. Use 'YYYY-MM-DD'."}, status=400)

        suggestions = self.generate_username_suggestions(firstname, lastname, dob)

        return Response({"results": suggestions})


class Testing(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # attendances = user.attendances.all()
        # queryset = AttendanceSerializer(attendances, many=True).data
        appreciations = user.appreciations.all()
        queryset = AppreciationSerializer(appreciations, many=True).data
        pdb.set_trace()
        return Response({"results": queryset})
