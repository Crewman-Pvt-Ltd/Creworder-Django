from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Company, Package, UserRole
from .serializers import UserSerializer, CompanySerializer, PackageSerializer, UserRoleSerializer
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


class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = user.role.role
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
            "modules": module_data
        })