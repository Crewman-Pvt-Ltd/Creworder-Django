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
        follow_up = CloudTelephonyChannel.objects.get(id=id)
        follow_up.delete()
        return True
    except ObjectDoesNotExist:
        return False
