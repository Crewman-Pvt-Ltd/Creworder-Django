import pdb
from django.contrib.auth.models import Group,Permission 
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from accounts.models import UserProfile,UserTargetsDelails
import pdb

class UserTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTargetsDelails
        fields = ['month', 'target', 'achieved_target', 'created_at', 'updated_at']

class UserDetailForDashboard(serializers.ModelSerializer):
    user_target = UserTargetSerializer(many=True, read_only=True, source='targets')  
    class Meta:
        model = UserProfile
        fields = ['enrolment_id', 'user_target']  