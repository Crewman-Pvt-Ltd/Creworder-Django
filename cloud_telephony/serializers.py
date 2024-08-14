from rest_framework import serializers
from .models import CloudTelephonyChannel

class CloudTelephonyChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudTelephonyChannel
        fields = '__all__'
