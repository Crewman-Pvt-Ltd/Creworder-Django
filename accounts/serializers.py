import pdb

from rest_framework import serializers
from .models import User, Company, Package, UserRole, UserProfile, Notice, Branch
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
    role = UserRoleCreateSerializer()
    company = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email', 'role', 'company']

    def create(self, validated_data):
        role_data = validated_data.pop("role")
        company_name = validated_data.pop("company")

        # password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        # print(password)

        package = Package.objects.get(id=3)
        company, created = Company.objects.get_or_create(name=company_name, package=package)

        user = User.objects.create_user(**validated_data)
        UserRole.objects.create(user=user, **role_data)

        UserProfile.objects.create(
            user=user,
            contact_no="0000000000",
            gender="m",
            status=True,
            marital_status="unmarried",
            company=company
        )

        return user
