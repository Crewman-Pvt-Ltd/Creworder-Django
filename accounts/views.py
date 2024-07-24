from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
import pdb

from .models import User, Company, Package, UserRole, UserProfile
from .serializers import UserSerializer, CompanySerializer, PackageSerializer, UserRoleSerializer, UserProfileSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    parser_class = JSONParser
    permission_classes = [IsAuthenticated]


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = UserSerializer(user, many=False).data
        profile = UserProfileSerializer(user.profile, many=False).data
        role = UserRoleSerializer(user.role, many=False).data
        return Response({"user": user_data, "profile": profile, "role": role})
        pdb.set_trace()
        role = user.role.role
        permissions = {
            'can_create_company': user.role.role == 'superadmin',
            'can_create_package': user.role.role == 'superadmin',
            'can_manage_services': user.role.role in ['admin', 'agent']
        }
        # company = user.role.company
        # if company:
        #     package = company.package
        #     modules = package.modules.all()
        #     module_data = [{"id": module.id, "name": module.name} for module in modules]
        # else:
        module_data = []

        return Response({
            "role": role,
            # "company": company.id if company else None,
            "modules": module_data,
            "permissions": permissions
        })
