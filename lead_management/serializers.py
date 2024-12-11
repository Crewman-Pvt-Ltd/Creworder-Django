from rest_framework import serializers
from .models import LeadModel, LeadSourceModel

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadModel
        fields = '__all__'


class LeadSourceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSourceModel
        fields = ['id', 'name', 'branch', 'company', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']