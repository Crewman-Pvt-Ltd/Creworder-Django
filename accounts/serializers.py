import pdb

from rest_framework import serializers
from .models import User, Company, Package, UserRole, UserProfile, Notice, Branch, FormEnquiry, SupportTicket, Module, \
    Department, Designation, Leave, Holiday, Award, Appreciation, Shift, Attendance
import string
import random


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'company']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    total_user_count = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'company_email', 'company_phone', 'company_website', 'company_address', 'status',
                  'created_at', 'updated_at', 'company_id', 'company_image', 'package_name', 'package', 'payment_mode',
                  'total_user_count', 'branches', 'gst', 'pan', 'cin', 'fssai', 'bank_account_no', 'bank_account_type',
                  'bank_name', 'bank_branch_name', 'bank_ifsc_code', 'support_email']

    def get_total_user_count(self, obj):
        count = UserProfile.objects.filter(company_id=obj.id).count()
        return count

    def get_package_name(self, obj):
        name = obj.package.name
        return name


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
        pdb.set_trace()

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        print(password)
        user = User.objects.create_user(password=password, **validated_data)

        UserRole.objects.create(user=user, **role_data)
        UserProfile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        pdb.set_trace()

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()

        if profile_data:
            profile = instance.profile
            pdb.set_trace()
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'


class AppreciationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appreciation
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
