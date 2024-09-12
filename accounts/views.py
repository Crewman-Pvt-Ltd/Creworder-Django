from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from guardian.shortcuts import get_objects_for_user
import pdb
from datetime import datetime
import random
from rest_framework.decorators import action
from .models import User, Company, Package, UserRole, UserProfile, Notice, Branch, FormEnquiry, SupportTicket, Module, \
    Department, Designation, Leave, Holiday, Award, Appreciation, Shift, Attendance, AllowedIP,ShiftRoster
from .serializers import UserSerializer, CompanySerializer, PackageSerializer, UserRoleSerializer, \
    UserProfileSerializer, NoticeSerializer, BranchSerializer, UserSignupSerializer, FormEnquirySerializer, \
    SupportTicketSerializer, ModuleSerializer, DepartmentSerializer, DesignationSerializer, LeaveSerializer, \
    HolidaySerializer, AwardSerializer, AppreciationSerializer, ShiftSerializer, AttendanceSerializer,ShiftRosterSerializer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoObjectPermissions
from django.db.models import Q, Count
from datetime import datetime, time
from dj_rest_auth.views import LoginView
from .permissions import CanChangeCompanyStatusPermission,CanLeaveApproveAndDisapprove


class IPRestrictedLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                branch = user.profile.branch

                ip_address = self.get_client_ip(request)
                pdb.set_trace()

                # Check if the IP address is allowed for the user's branch
                if not AllowedIP.objects.filter(branch=branch, ip_address=ip_address).exists():
                    return Response({'error': 'Login from this IP address is not allowed'},
                                    status=status.HTTP_403_FORBIDDEN)

            except User.DoesNotExist:
                # Proceed with the standard response, the user may not exist
                pass

        return super().post(request, *args, **kwargs)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


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

    @action(detail=True, methods=['post'], permission_classes=[CanChangeCompanyStatusPermission])
    def change_status(self, request, pk=None):
        company = self.get_object()
        if 'status' not in request.data:
            raise ValidationError({"detail": "The status field is required."})
        else:
            company_status = request.data['status']
            if company_status not in [True, False]:
                raise ValidationError({"detail": "The value provided is not a valid choice."})
            company.status = company_status
            company.save()

        return Response({"detail": 'Status changed successfully.'})


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

    def get_queryset(self):
        user = self.request.user
        if user.role.role == "admin" or user.role.role == "agent":
            branch = user.profile.branch
            queryset = Designation.objects.filter(branch=branch)
        else:
            queryset = Branch.objects.all()
        return queryset


class LeaveViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

    @action(detail=True, methods=['put'],permission_classes=[CanLeaveApproveAndDisapprove])
    def leave_action(self, request, pk=None):
        leave = self.get_object()
        if 'status' not in request.data:
            raise ValidationError({"detail": "The status field is required."})
        leave_status = request.data['status']
        leave.status = leave_status
        leave.save()

        return Response({"detail": "Status changed successfully."}, status=status.HTTP_200_OK)

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

class ShiftRosterViewSet(viewsets.ModelViewSet):
    queryset = ShiftRoster.objects.all()
    serializer_class = ShiftRosterSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = ShiftRosterSerializer(data=request.data)
        if serializer.is_valid():
            shiftRosterExistOrNot = ShiftRoster.objects.filter(user=request.data['user'], branch=request.data['branch']).first()
            if shiftRosterExistOrNot:
                serializer = self.get_serializer(shiftRosterExistOrNot, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        userData = UserProfile.objects.filter(user_id=request.user.id).first()
        serializer = UserProfileSerializer(userData)
        serialized_data = serializer.data
        branch=serialized_data['branch']
        queryset = self.get_queryset()
        if branch:
            queryset = queryset.filter(branch=branch)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.data)
        date_range = request.query_params['date_range'].split(' - ')
        if len(date_range) != 2:
            return Response(
                {"Success": False, "Error": "Invalid date range format. Expected format: MM/DD/YYYY - MM/DD/YYYY"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            start_date = datetime.strptime(date_range[0], '%m/%d/%Y')
            end_date = datetime.strptime(date_range[1], '%m/%d/%Y')
            start_datetime = datetime.combine(start_date, time.min)
            end_datetime = datetime.combine(end_date, time.max)
            date_filter = Q(date__range=(start_datetime, end_datetime))
            tableData = Attendance.objects.filter(date_filter)
            attendance_counts = tableData.values('user__id','user__username').annotate(
                total_absent=Count('id', filter=Q(attendance='A')),
                total_present=Count('id', filter=Q(attendance='P'))
            )
            orderTableData = AttendanceSerializer(tableData, many=True).data
            user_by_data={}
            for row in orderTableData:
                present_title='Absent'
                if row['user'] not in user_by_data:
                    user_by_data[row['user']]=[]

                start_time = datetime.strptime(row['shift_start_time'], "%H:%M:%S")
                end_time = datetime.strptime(row['shift_end_time'], "%H:%M:%S")
                time_difference = end_time - start_time
                hours = time_difference.total_seconds() / 3600
                clock_in_time_str = row.get('clock_in', '')
                clock_out_time_str = row.get('clock_out', '')

                T1 = datetime.strptime(row['shift_start_time'], "%H:%M:%S")
                T2 = datetime.strptime(row['clock_in'], "%H:%M:%S")
                time_difference = T2 - T1
                difference_in_minutes = time_difference.total_seconds() / 60
                if not clock_out_time_str:
                    present_title = 'Not_Clock_Out'
                else:
                    user_start_time = datetime.strptime(clock_in_time_str, "%H:%M:%S")
                    user_end_time = datetime.strptime(clock_out_time_str, "%H:%M:%S")
                    user_time_difference = user_end_time - user_start_time
                    working_hours = user_time_difference.total_seconds() / 3600
                    if clock_out_time_str=='':
                        present_title = 'Not_Clock_Out'
                    if difference_in_minutes > 11:
                        present_title = 'Late'
                    elif working_hours >= hours and row['attendance'] !='A':
                        present_title = 'Full_Day'
                    elif working_hours >= hours / 2 and row['attendance'] !='A':
                        present_title = 'Half_Day'
                    elif working_hours >= hours / 4 and row['attendance'] !='A':
                        present_title = 'Short_Day'
                    else:
                        pass
                    if row['attendance'] =='A':
                        present_title = 'Absent'


                print("Shift hours: " + str(hours))
                print("Worked hours: " + str(working_hours))
                print(present_title)
                print("===================================================================")
                user_by_data[row['user']].append({
                    "id": row['id'],
                    "date": datetime.strptime(str(row['date']), '%Y-%m-%d').strftime('%Y-%m-%d'),
                    "clock_in": str(row['clock_in']),
                    "clock_out": str(row['clock_out']),
                    "working_from": row['working_from'],
                    "attendance": row['attendance'],
                    "shift": row['shift'],
                    "shift_name": row['shift_name'],
                    "shift_start_time": row['shift_start_time'],
                    "shift_end_time": row['shift_end_time'],
                    "shift_hours":str(hours),
                    "working_hours":str(working_hours),
                    "present_title":present_title
                })
            return Response(
                {
                    "Success": True,
                    "Data": user_by_data,
                    "Attendance_Counts": list(attendance_counts),
                },
                status=status.HTTP_200_OK
            )

        except ValueError:
            return Response(
                {"Success": False, "Error": "Invalid date format. Expected MM/DD/YYYY"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"Success": False, "Error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GetUsernameSuggestions(APIView):
    permission_classes = [IsAuthenticated]

    def generate_username_suggestions(self, firstname, lastname, date_of_birth):
        base_username = (firstname + lastname[:random.randint(1, 5)] + date_of_birth.strftime('%Y')).lower()
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
