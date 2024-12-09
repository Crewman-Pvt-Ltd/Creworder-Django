from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.contrib.contenttypes.models import ContentType
from guardian.shortcuts import get_objects_for_user
from rest_framework import generics, status
from django.contrib.auth.models import Group,Permission
from django.db import transaction
import pdb
import sys
from datetime import datetime
import random
from rest_framework.decorators import action
from .models import User, Company, Package, UserProfile, Notice, Branch, FormEnquiry, SupportTicket, Module, \
    Department, Designation, Leave, Holiday, Award, Appreciation, Shift, Attendance, AllowedIP,ShiftRoster,CustomAuthGroup,PickUpPoint,\
    UserTargetsDelails,AdminBankDetails,QcTable
from .serializers import UserSerializer, CompanySerializer, PackageSerializer, \
    UserProfileSerializer, NoticeSerializer, BranchSerializer, UserSignupSerializer, FormEnquirySerializer, \
    SupportTicketSerializer, ModuleSerializer, DepartmentSerializer, DesignationSerializer, LeaveSerializer, \
    HolidaySerializer, AwardSerializer, AppreciationSerializer, ShiftSerializer, AttendanceSerializer,ShiftRosterSerializer, \
    PackageDetailsSerializer,CustomAuthGroupSerializer,PermissionSerializer,PickUpPointSerializer,UserTargetSerializer,AdminBankDetailsSerializers,\
    AllowedIPSerializers,QcSerialiazer
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
        if user.profile.user_type == "superadmin":
            queryset = User.objects.filter(profile__user_type=user.profile.user_type)
        elif user.profile.user_type == "admin":
            company = user.profile.company
            queryset = User.objects.filter(profile__company=company).exclude(id=user.id)
        elif user.profile.user_type== "agent":
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
        if user.profile.user_type == "admin" or user.profile.user_type == "agent":
            company = user.profile.company
            queryset = Branch.objects.filter(company=company)
        else:
            queryset = Branch.objects.all()
        return queryset

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        package_data = data.get('package')
        package_details_data = data.get('package_details')
        package_serializer = PackageSerializer(data=package_data)
        
        if package_serializer.is_valid():
            package = package_serializer.save()
            for detail_data in package_details_data:
                detail_data['package'] = package.id
                package_detail_serializer = PackageDetailsSerializer(data=detail_data)
                if package_detail_serializer.is_valid():
                    package_detail_serializer.save()
                else:
                    return Response(package_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            package_serializer = PackageSerializer(package)
            return Response(package_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(package_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        package_data = data.get('package')
        package_details_data = data.get('package_details')
        package_serializer = PackageSerializer(instance, data=package_data, partial=True)
        if package_serializer.is_valid():
            package = package_serializer.save()
            existing_details = {detail.id: detail for detail in instance.packagedetails.all()}
            for detail_data in package_details_data:
                detail_id = detail_data.get('id')
                if detail_id and detail_id in existing_details:
                    package_detail_instance = existing_details.pop(detail_id)
                    package_detail_serializer = PackageDetailsSerializer(package_detail_instance, data=detail_data, partial=True)
                else:
                    detail_data['package'] = package.id 
                    package_detail_serializer = PackageDetailsSerializer(data=detail_data)
                if package_detail_serializer.is_valid():
                    package_detail_serializer.save()
                else:
                    return Response(package_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            for remaining_detail in existing_details.values():
                remaining_detail.delete()
            package_serializer = PackageSerializer(package)
            return Response(package_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(package_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class UserRoleViewSet(viewsets.ModelViewSet):
#     queryset = UserRole.objects.all()
#     serializer_class = UserRoleSerializer
#     permission_classes = [IsAuthenticated]


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

# for all permisson given user
class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        guardian_permissions = user.get_all_permissions()
        user_data = UserSerializer(user, many=False).data
        profile = UserProfileSerializer(user.profile, many=False).data
        user_data['profile'] = profile
        role = user.profile.user_type
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
        if user.profile.user_type == "admin" or user.profile.user_type == "agent":
            branch = user.profile.branch
            queryset = Designation.objects.filter(branch=branch)
        else:
            queryset = Designation.objects.all()
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
    permission_classes = [IsAuthenticated,DjangoObjectPermissions]
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

# class GetPackageModule(viewsets.ModelViewSet):
#     queryset = Package.objects.all()
#     serializer_class = PackageSerializer
#     permission_classes = [IsAuthenticated, DjangoObjectPermissions]
#     def retrieve(self, request, *args, **kwargs):
#         userData = UserProfile.objects.filter(user_id=request.user.id).values("branch", "company").first()
#         CompanyData=Company.objects.filter(id=userData['company']).values("package").first()
#         print(CompanyData['package'])
#         showDataDict={}
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         for data in serializer.data['packagedetails']:
#             if f"{data['menu_name']}" in showDataDict:
#                 print("yes")
#                 if isinstance(showDataDict[f"{data['menu_name']}"], list):
#                     print(data['menu_name'])
#                     showDataDict[f"{data['menu_name']}"].append({f"{data['sub_menu_name']}":f"{data['sub_menu_url']}"})
#             else:
#                 if data['sub_menu_name']==None:
#                     showDataDict[f"{data['menu_name']}"]={f"{data['menu_name']}":f"{data['menu_url']}"}
#                 else:
#                     showDataDict[f"{data['menu_name']}"]=[{f"{data['sub_menu_name']}":f"{data['sub_menu_url']}"}]
#         data = dict(serializer.data)
#         data['sidebardata'] = showDataDict
#         return Response(data)
class GetPackageModule(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated, DjangoObjectPermissions]
    def retrieve(self, request, *args, **kwargs):
        userData = UserProfile.objects.filter(user_id=request.user.id).values("branch", "company").first()
        CompanyData = Company.objects.filter(id=userData['company']).values("package").first()
        package_id = CompanyData['package']
        package_instance = Package.objects.get(id=package_id)
        serializer = self.get_serializer(package_instance)
        showDataDict = {}
        for data in serializer.data['packagedetails']:
            menu_name = data['menu_name']
            sub_menu_name = data['sub_menu_name']
            sub_menu_url = data['sub_menu_url']
            menu_url = data['menu_url']
            icon=data['menu_icon']
            if menu_name in showDataDict:
                if isinstance(showDataDict[menu_name], list):
                    showDataDict[menu_name].append({sub_menu_name: sub_menu_url})
            else:
                if sub_menu_name is None or sub_menu_name==None:
                    print("1221221")
                    showDataDict[menu_name] = {menu_name: menu_url,"icon":icon}
                else:
                    showDataDict[menu_name+'_icon']=icon
                    showDataDict[menu_name] = [{sub_menu_name: sub_menu_url}]


        data = dict(serializer.data)
        data['sidebardata'] = showDataDict
        return Response(data)


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
    
class CustomAuthGroupViewSetold(viewsets.ModelViewSet):
    queryset = CustomAuthGroup.objects.all()
    serializer_class = CustomAuthGroupSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['company_id'] = request.user.profile.company.id
        request.data['branch_id'] = request.user.profile.branch.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class CustomAuthGroupViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, updating, and deleting objects and managing permissions within a group.
    """
    queryset = CustomAuthGroup.objects.all()
    serializer_class = CustomAuthGroupSerializer
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['company_id'] = request.user.profile.company.id
        request.data['branch_id'] = request.user.profile.branch.id
        permission_ids = request.data.get('permission_ids', [])
        if not isinstance(permission_ids, list) or not permission_ids:
            return Response(
                {"error": "permission_ids must be a non-empty list."},
                status=status.HTTP_400_BAD_REQUEST
            )
        permissions = Permission.objects.filter(id__in=permission_ids)
        if not permissions.exists():
            return Response(
                {"error": "No valid permissions found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                group_id = serializer.data['group']['id']
                group = Group.objects.get(id=group_id)
                group.permissions.add(*permissions)
                group.save()
                return Response(
                    {
                        "message": f"Group '{group.name}' created and permissions added.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, pk=None ,*args, **kwargs,):
        """
        Update group permissions.
        """
        instance = self.get_object()
        request.data['company_id'] = request.user.profile.company.id
        request.data['branch_id'] = request.user.profile.branch.id
        order = CustomAuthGroup.objects.get(id=pk)
        serializer = CustomAuthGroupSerializer(order)
        serialized_data = serializer.data
        if 'group' in request.data:
            print(serialized_data['group']['name'])
            if serialized_data['group']['name']==request.data['group']['name']:
                request.data.pop('group', None)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        permission_ids = request.data.get('permission_ids', [])
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            if not permissions.exists():
                return Response(
                    {"error": "No valid permissions found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        try:
            with transaction.atomic():
                serializer.save()
                group = Group.objects.get(id=serializer.data['group']['id'])
                group.permissions.clear()
                group.permissions.add(*permissions)
                group.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """
        Delete a group and its associated permissions.
        """
        instance = self.get_object()
        try:
            with transaction.atomic():
                group = Group.objects.get(id=instance.group.id)
                group.permissions.clear()
                group.delete()
                instance.delete()
                return Response({"massage": "Deleted."},status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request, *args, **kwargs):
        """
        Get a list of CustomAuthGroup instances with their associated group, branch, and company details.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserGroupViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing user group memberships using user_id and group_id.
    """
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='add-user-to-group')
    def add_user_to_group(self, request):
        """
        Custom action to add a user to a group using user_id and group_id.
        """
        user_id = request.data.get('user_id')
        group_id = request.data.get('group_id')
        try:
            user = User.objects.get(id=user_id)
            group = Group.objects.get(id=group_id)
            user.groups.add(group)
            user.save()
            return Response({"message": f"User '{user.username}' added to group '{group.name}'."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='list-group-members/(?P<group_id>\d+)')
    def list_group_members(self, request, group_id=None):
        """
        Custom action to list all members of a specific group using group_id.
        """
        try:
            group = Group.objects.get(id=group_id)
            users = group.user_set.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        

class GroupPermissionViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing permissions within a group.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='add-permissions-to-group')
    def add_permissions_to_group(self, request):
        """
        Add multiple permissions to a group.
        """
        group_id = request.data.get('group_id')
        permission_ids = request.data.get('permission_ids', [])

        if not isinstance(permission_ids, list):
            return Response({"error": "permission_ids must be a list."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = Group.objects.get(id=group_id)
            permissions = Permission.objects.filter(id__in=permission_ids)
            if permissions.exists():
                group.permissions.add(*permissions)
                group.save()
                return Response(
                    {"message": f"Permissions added to group '{group.name}'."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": "No valid permissions found."}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['put'], url_path='update-permissions-of-group')
    def update_permissions_of_group(self, request):
        """
        Update (replace) the permissions of a group with new permissions.
        """
        group_id = request.data.get('group_id')
        permission_ids = request.data.get('permission_ids', [])

        if not isinstance(permission_ids, list):
            return Response({"error": "permission_ids must be a list."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
            new_permissions = Permission.objects.filter(id__in=permission_ids)

            if new_permissions.exists():
                group.permissions.set(new_permissions)
                group.save()
                return Response(
                    {"message": f"Permissions updated for group '{group.name}'."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": "No valid permissions found."}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'], url_path='delete-permissions-from-group')
    def delete_permissions_from_group(self, request):
        """
        Delete specific permissions from a group.
        """
        group_id = request.data.get('group_id')
        permission_ids = request.data.get('permission_ids', [])

        if not isinstance(permission_ids, list):
            return Response({"error": "permission_ids must be a list."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group = Group.objects.get(id=group_id)
            permissions_to_remove = Permission.objects.filter(id__in=permission_ids)

            if permissions_to_remove.exists():
                group.permissions.remove(*permissions_to_remove)
                group.save()
                return Response(
                    {"message": f"Permissions removed from group '{group.name}'."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": "No valid permissions found."}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='list-group-permissions/(?P<group_id>\d+)')
    def list_group_permissions(self, request, group_id=None):
        """
        List all permissions of a specific group using group_id.
        """
        try:
            group = Group.objects.get(id=group_id)
            permissions = group.permissions.all()
            serializer = PermissionSerializer(permissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

class PermmisionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = None 

class FetchPermissionView(APIView):
    def post(self, request, model_name=None):
        request.data['name_list'].extend(["Order Details", "Dashboard"])
        if not request.data or 'name_list' not in request.data or not request.data['name_list']:
            return Response({"detail": "Request body must contain a non-empty 'name_list'."}, status=400)
        name_list = [name.replace(" ", "_").lower() for name in request.data.get('name_list', [])]
        content_type_ids = ContentType.objects.filter(Q(model__in=name_list) | Q(model__startswith='settings_')).values_list('id', flat=True)
        permissions = Permission.objects.filter(content_type__in=content_type_ids)
        permissions_dict = {}
        for permission in permissions:
            permissions_dict[permission.codename] = permission.id
        return Response(permissions_dict)
        
class PickUpPointView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PickUpPoint.objects.all()
    serializer_class = PickUpPointSerializer



class TargetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserTargetsDelails.objects.all()
    serializer_class = UserTargetSerializer

class AdminBankDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AdminBankDetails.objects.all()
    serializer_class = AdminBankDetailsSerializers
    def create(self, request, *args, **kwargs):
        data = request.data
        user_profile = UserProfile.objects.get(user__id=request.data['user'])
        data['branch']=user_profile.branch.id
        data['company']=user_profile.company.id
        if data.get('account_number') != data.get('re_account_number'):
            return Response(
                {"error": "Account number and re-entered account number must match."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = request.user
        priority = data.get('priority')
        if AdminBankDetails.objects.filter(user=user, priority=priority).exists():
            return Response(
                {"error": f"Priority {priority} already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AddAllowIpViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AllowedIP.objects.all()
    serializer_class = AllowedIPSerializers

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['branch'] = user.profile.branch.id
        request.data['company'] = user.profile.company.id
        return super().create(request, *args, **kwargs)
    
class QcViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset =QcTable.objects.all()
    serializer_class= QcSerialiazer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        request.data['company'] = user.profile.company.id
        return super().create(request, *args, **kwargs)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if 'company' not in request.data:
            request.data['company'] = instance.company.id 
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
class AssignRole(APIView):
    def post(self, request, *args, **kwargs):
        # Get the teamlead, manager, and agent_list from the request data
        teamlead_id = request.data.get('teamlead')
        manager_id = request.data.get('manager')
        agent_list = request.data.get('agent_list')

        # Validate if teamlead and manager are provided
        if not teamlead_id:
            return Response({"Success": False, "Message": "Teamlead required."},
                            status=status.HTTP_400_BAD_REQUEST)
        if not manager_id:
            return Response({"Success": False, "Message": "Manager required."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if not agent_list or not isinstance(agent_list, list):
            return Response({"Success": False, "Message": "Agent list is required and should be a list."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Try to get the teamlead and manager instances
        try:
            teamlead = UserProfile.objects.get(user_id=teamlead_id)
        except UserProfile.DoesNotExist:
            return Response({"Success": False, "Message": "Teamlead not found."},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            manager = UserProfile.objects.get(user_id=manager_id)
        except UserProfile.DoesNotExist:
            return Response({"Success": False, "Message": "Manager not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # List to hold updated agents
        updated_profiles = []

        for agent_id in agent_list:
            try:
                agent_profile = UserProfile.objects.get(user_id=agent_id)

                # Assign the teamlead and manager to the agent
                agent_profile.teamlead = teamlead.user
                agent_profile.manager = manager.user
                agent_profile.save()

                # Add the updated agent username to the list
                updated_profiles.append(agent_profile.user.username)
            except UserProfile.DoesNotExist:
                return Response({"Success": False, "Message": f"Agent with ID {agent_id} not found."},
                                status=status.HTTP_404_NOT_FOUND)

        return Response(
            {"Success": True, "Data": {"Updated Agents": updated_profiles}},
            status=status.HTTP_200_OK,
        )
# team lead list and manager list view     
class TeamleadViewSet(APIView):
   
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    
    def get(self, request, *args, **kwargs):
        # Get company_id and branch_id from the request query parameters
        company_id = request.query_params.get('company_id', None)
        branch_id = request.query_params.get('branch_id', None)
        
        # Ensure that either company_id or branch_id is provided
        if not company_id and not branch_id:
            return Response(
                {"Success": False, "Message": "Either company_id or branch_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Query to get distinct teamlead values, filtered by company_id and branch_id
        teamleads = UserProfile.objects.exclude(teamlead=None)
        
        if company_id:
            teamleads = teamleads.filter(company=company_id)
        if branch_id:
            teamleads = teamleads.filter(branch=branch_id)

        teamleads = teamleads.values('teamlead').distinct()

        # Fetching the teamlead users based on the distinct IDs
        teamlead_users = UserProfile.objects.filter(user__in=[teamlead['teamlead'] for teamlead in teamleads])
        
        # Serialize the teamlead users
        serializer = UserProfileSerializer(teamlead_users, many=True)
        
        # Return the response with the serialized data
        return Response(
            {"Success": True, "Data":  serializer.data},
            status=status.HTTP_200_OK
        )
    
class ManagerViewSet(APIView):
   
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view
    
    def get(self, request, *args, **kwargs):
        # Get company_id and branch_id from the request query parameters
        company_id = request.query_params.get('company_id', None)
        branch_id = request.query_params.get('branch_id', None)
        
        # Ensure that either company_id or branch_id is provided
        if not company_id and not branch_id:
            return Response(
                {"Success": False, "Message": "Either company_id or branch_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Query to get distinct manager values, filtered by company_id and branch_id
        managers = UserProfile.objects.exclude(manager=None)
        
        if company_id:
            managers = managers.filter(company_id=company_id)
        if branch_id:
            managers = managers.filter(branch_id=branch_id)

        managers = managers.values('manager').distinct()

        # Fetching the manager users based on the distinct IDs
        manager_users = UserProfile.objects.filter(user__in=[manager['manager'] for manager in managers])
        
        # Serialize the manager users
        serializer = UserProfileSerializer(manager_users, many=True)
        
        # Return the response with the serialized data
        return Response(
            {"Success": True, "Data":  serializer.data},
            status=status.HTTP_200_OK
        )



class AgentListByTeamleadAPIView(APIView):

    permission_classes = [IsAuthenticated] 
    """
    Returns the list of agents for a specific teamlead.
    Accepts 'teamlead_id' as a query parameter.
    """
    def get(self, request, *args, **kwargs):
        teamlead_id = request.query_params.get('teamlead_id', None)
        
        # Ensure that teamlead_id is provided
        if not teamlead_id:
            return Response(
                {"Success": False, "Error": "teamlead_id must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter agents based on teamlead_id
        agents = UserProfile.objects.filter(teamlead_id=teamlead_id)
        
        # Serialize the result and return the response
        serializer = UserProfileSerializer(agents, many=True)
        return Response(
            {"Success": True, "Data": {"Agents": serializer.data}},
            status=status.HTTP_200_OK
        )
    

class AgentListByManagerAPIView(APIView):
   
    def get(self, request, *args, **kwargs):
        manager_id = request.query_params.get('manager_id', None)
        
        # Ensure that manager_id is provided
        if not manager_id:
            return Response(
                {"Success": False, "Error": "manager_id must be provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter agents based on manager_id
        agents = UserProfile.objects.filter(manager_id=manager_id)
        
        # Serialize the result and return the response
        serializer = UserProfileSerializer(agents, many=True)
        return Response(
            {"Success": True, "Data": {"Agents": serializer.data}},
            status=status.HTTP_200_OK
        )
