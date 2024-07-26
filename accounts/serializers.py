import pdb

from rest_framework import serializers
from .models import User, Company, Package, UserRole, UserProfile


class CompanySerializer(serializers.ModelSerializer):
    total_user_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'company_email', 'company_phone', 'company_website', 'company_address', 'status',
                  'created_at', 'updated_at', 'company_id', 'company_image', 'payment_mode', 'total_user_count']

    def get_total_user_count(self, obj):
        count = UserRole.objects.filter(company_id=obj.id).count()
        return count


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    role = UserRoleSerializer()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_staff', 'profile',
                  'role']

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        role_data = validated_data.pop("role")
        user = User.objects.create_user(**validated_data)
        UserRole.objects.create(user=user, **role_data)
        UserProfile.objects.create(user=user, **profile_data)
