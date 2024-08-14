import os
from cloud_telephony.models import CloudTelephonyChannel
from cloud_telephony.serializers import CloudTelephonyChannelSerializer
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
import pdb

def createCloudTelephoneyChannel(data,userid):
    userData=UserProfile.objects.filter(user_id=userid).first()
    serializer = UserProfileSerializer(userData)
    serialized_data = serializer.data
    data['branch']=serialized_data['branch']
    data['company']=serialized_data['company']
    data['user']=userid
    serializer = CloudTelephonyChannelSerializer(data=data)
    if serializer.is_valid():
        cloud_telephony_channel = serializer.save()
        return cloud_telephony_channel
    else:
        raise ValueError(serializer.errors)

def deleteCloudTelephoneyChannel(id):
    try:
        createdData = CloudTelephonyChannel.objects.get(id=id)
        createdData.delete()
        return True
    except ObjectDoesNotExist:
        return False

def updateCloudTelephoneyChannel(id,data):
    try:
        updatedData = CloudTelephonyChannel.objects.get(id=id)
        serializer = CloudTelephonyChannelSerializer(updatedData, data=data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise ValueError(serializer.errors)
    except ObjectDoesNotExist:
        return None
    
def getCloudTelephoneyChannel(id=None):
    CloudTelephonyChannelData=''
    if id is not None:
        userData=UserProfile.objects.filter(user_id=id).first()
        serializer = UserProfileSerializer(userData)
        serialized_data = serializer.data
        CloudTelephonyChannelData= CloudTelephonyChannel.objects.filter(branch=serialized_data['branch'],company=serialized_data['company'])

    return CloudTelephonyChannelData