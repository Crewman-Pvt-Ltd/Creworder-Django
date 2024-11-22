from rest_framework import serializers
from .models import CloudTelephonyChannel,CloudTelephonyChannelAssign,UserMailSetup

class CloudTelephonyChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudTelephonyChannel
        fields = '__all__'

class CloudTelephonyChannelAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudTelephonyChannelAssign
        fields = '__all__'

class UserMailSetUpSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserMailSetup
        fields = '__all__'
