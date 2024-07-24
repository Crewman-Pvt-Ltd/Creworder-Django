import pdb

from rest_framework import serializers
from .models import User, Company, Package, UserRole, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')


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
