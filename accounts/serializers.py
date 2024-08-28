import pdb

from rest_framework import serializers
from .models import User, Company, Package, UserRole, UserProfile, Notice, Branch, FormEnquiry, SupportTicket
import string
import random


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['name', 'address']


class CompanySerializer(serializers.ModelSerializer):
    total_user_count = serializers.SerializerMethodField()
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'company_email', 'company_phone', 'company_website', 'company_address', 'status',
                  'created_at', 'updated_at', 'company_id', 'company_image', 'package', 'payment_mode',
                  'total_user_count', 'branches']

    def get_total_user_count(self, obj):
        count = UserProfile.objects.filter(company_id=obj.id).count()
        return count


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


class FormEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = FormEnquiry
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserRoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        exclude = ['user']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileCreateSerializer()
    role = UserRoleCreateSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_staff',
                  'profile', 'role']

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        role_data = validated_data.pop("role")

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user = User.objects.create_user(password=password, **validated_data)

        UserRole.objects.create(user=user, **role_data)
        UserProfile.objects.create(user=user, **profile_data)

        return user


class UserSignupSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    contact_no = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email', 'company', 'contact_no']

    def create(self, validated_data):
        company_data = validated_data.pop("company")
        contact_no = validated_data.pop("contact_no")
        package = Package.objects.get(id=1)
        company = Company.objects.create(package=package, **company_data)

        user = User.objects.create_user(**validated_data)
        UserRole.objects.create(user=user, role='admin')

        UserProfile.objects.create(
            user=user,
            contact_no=contact_no,
            gender="m",
            status=True,
            marital_status="unmarried",
            company=company
        )

        return user


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'
