import pdb
from django.contrib.auth.models import Group,Permission 
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import User, Company, Package,UserProfile, Notice, Branch, FormEnquiry, SupportTicket, Module, \
    Department, Designation, Leave, Holiday, Award, Appreciation, Shift, Attendance,ShiftRoster,PackageDetailsModel,CustomAuthGroup,\
    PickUpPoint,UserTargetsDelails
import string
import random
from superadmin_assets.serializers import SubMenuSerializer,MenuSerializer
from superadmin_assets.models import SubMenuModel,MenuModel

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'company', 'id']

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

class PackageDetailsSerializer(serializers.ModelSerializer):
    menu_name=serializers.SerializerMethodField()
    menu_url=serializers.SerializerMethodField()
    menu_icon=serializers.SerializerMethodField()
    sub_menu_name=serializers.SerializerMethodField()
    sub_menu_url=serializers.SerializerMethodField()
    class Meta:
        model = PackageDetailsModel
        fields = '__all__'
    def get_menu_url(self,data):
        return data.menu.url if data.menu else None
    def get_sub_menu_url(self,data):
        return data.submenu.url if data.submenu else None
    def get_menu_name(self,data):
        return data.menu.name if data.menu else None
    def get_sub_menu_name(self,data):
        return data.submenu.name if data.submenu else None
    def get_menu_icon(self,data):
        return data.menu.icon if data.menu else None


class PackageSerializer(serializers.ModelSerializer):
    packagedetails = PackageDetailsSerializer(many=True, read_only=True)
    class Meta:
        model = Package
        fields = '__all__'

class FormEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = FormEnquiry
        fields = '__all__'


# class UserRoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserRole
#         fields = '__all__'


# class UserRoleCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserRole
#         exclude = ['user']


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
    # role = UserRoleCreateSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password',  'first_name', 'last_name', 'email', 'last_login', 'date_joined',
                  'is_staff', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
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

class ShiftRosterSerializer(serializers.ModelSerializer):
    monday_shift_name=serializers.SerializerMethodField()
    tuesday_shift_name=serializers.SerializerMethodField()
    wednesday_shift_name=serializers.SerializerMethodField()
    thursday_shift_name=serializers.SerializerMethodField()
    friday_shift_name=serializers.SerializerMethodField()
    saturday_shift_name=serializers.SerializerMethodField()
    sunday_shift_name=serializers.SerializerMethodField()
    class Meta:
        model = ShiftRoster
        fields = '__all__'
    def get_monday_shift_name(self,data):
        if data.monday_shift:
            return ShiftSerializer(data.monday_shift).data
        return None
    def get_tuesday_shift_name(self,data):
        if data.tuesday_shift:
            return ShiftSerializer(data.tuesday_shift).data
        return None
    def get_wednesday_shift_name(self,data):
        if data.wednesday_shift:
            return ShiftSerializer(data.wednesday_shift).data
        return None
    def get_thursday_shift_name(self,data):
        if data.thursday_shift:
            return ShiftSerializer(data.thursday_shift).data
        return None
    def get_friday_shift_name(self,data):
        if data.friday_shift:
            return ShiftSerializer(data.friday_shift).data
        return None
    def get_saturday_shift_name(self,data):
        if data.saturday_shift:
            return ShiftSerializer(data.saturday_shift).data
        return None
    def get_sunday_shift_name(self,data):
        if data.sunday_shift:
            return ShiftSerializer(data.sunday_shift).data
        return None


class AttendanceSerializer(serializers.ModelSerializer):
    shift_name = serializers.CharField(source='shift.name')
    shift_start_time = serializers.CharField(source='shift.start_time')
    shift_end_time = serializers.CharField(source='shift.end_time')
    class Meta:
        model = Attendance
        fields = '__all__'

    def get_shift_name(self, data):
        return data.shift.name if data.shift else None
    def get_shift_start_time(self, data):
        return data.shift.start_time if data.shift else None
    def get_end_time(self, data):
        return data.shift.end_time if data.shift else None
    
class AuthGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']  # Include relevant fields from Branch


class CompanySerializer1(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']  # Include relevant fields from Company


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class CustomAuthGroupSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    branch = BranchSerializer(read_only=True)
    company = CompanySerializer1(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), source='branch', write_only=True)
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), source='company', write_only=True)

    class Meta:
        model = CustomAuthGroup
        fields = ['id', 'group', 'branch', 'company', 'branch_id', 'company_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        group_data = validated_data.pop('group')
        group = Group.objects.create(**group_data)

        custom_auth_group = CustomAuthGroup.objects.create(group=group, **validated_data)
        return custom_auth_group

    def update(self, instance, validated_data):
        group_data = validated_data.pop('group', None)
        if group_data:
            group_serializer = GroupSerializer(instance.group, data=group_data, partial=True)
            group_serializer.is_valid(raise_exception=True)
            group_serializer.save()

        return super().update(instance, validated_data)
    
class PickUpPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickUpPoint
        fields = '__all__'