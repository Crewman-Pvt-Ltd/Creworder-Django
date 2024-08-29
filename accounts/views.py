from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from guardian.shortcuts import get_objects_for_user
import pdb

from .models import User, Company, Package, UserRole, UserProfile, Notice, Branch, FormEnquiry, SupportTicket, Module
from .serializers import UserSerializer, CompanySerializer, PackageSerializer, UserRoleSerializer, \
    UserProfileSerializer, NoticeSerializer, BranchSerializer, UserSignupSerializer, FormEnquirySerializer, \
    SupportTicketSerializer, ModuleSerializer
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


class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        guardian_permissions = user.get_all_permissions()
        user_data = UserSerializer(user, many=False).data
        profile = UserProfileSerializer(user.profile, many=False).data
        user_data['profile'] = profile
        role = user.role.role
        # permissions = {
        #     'can_create_company': user.role.role == 'superadmin',
        #     'can_create_package': user.role.role == 'superadmin',
        #     'can_manage_services': user.role.role in ['admin', 'agent']
        # }
        response_data = {"user": user_data, "role": role, "permissions": guardian_permissions}
        # company = user.role.company
        # if company:
        #     package = company.package
        #     modules = package.modules.all()
        #     module_data = [{"id": module.id, "name": module.name} for module in modules]
        # else:
        module_data = []

        # return Response({
        #     "user": user_data,
        #     "role": role,
        #     # "company": company.id if company else None,
        #     # "modules": module_data,
        #     "permissions": permissions,
        #
        # })

        return Response(response_data)


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
