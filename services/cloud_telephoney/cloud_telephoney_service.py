import os
from cloud_telephony.models import CloudTelephonyChannel, CloudTelephonyChannelAssign
from cloud_telephony.serializers import (
    CloudTelephonyChannelSerializer,
    CloudTelephonyChannelAssignSerializer,
)
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
import pdb


def createCloudTelephoneyChannel(data, userid):
    userData = UserProfile.objects.filter(user_id=userid).first()
    serializer = UserProfileSerializer(userData)
    serialized_data = serializer.data
    mutable_data = data.copy()
    mutable_data['branch'] = serialized_data["branch"]
    mutable_data['company'] = serialized_data["company"]
    mutable_data['user'] = userid
    serializer = CloudTelephonyChannelSerializer(data=mutable_data)
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


def updateCloudTelephoneyChannel(id, data):
    try:
        updatedData = CloudTelephonyChannel.objects.get(id=id)
        serializer = CloudTelephonyChannelSerializer(
            updatedData, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise ValueError(serializer.errors)
    except ObjectDoesNotExist:
        return None


def getCloudTelephoneyChannel(id=None):
    CloudTelephonyChannelData = ""
    if id is not None:
        userData = UserProfile.objects.filter(user_id=id).first()
        serializer = UserProfileSerializer(userData)
        serialized_data = serializer.data
        CloudTelephonyChannelData = CloudTelephonyChannel.objects.filter(
            branch=serialized_data["branch"], company=serialized_data["company"]
        )

    return CloudTelephonyChannelData


def createCloudTelephoneyChannelAssign(data, userid):
    userData = UserProfile.objects.filter(user_id=userid).first()
    if not userData:
        raise ValueError("User not found")
    serializer = UserProfileSerializer(userData)
    serialized_data = serializer.data
    data["branch"] = serialized_data["branch"]
    data["company"] = serialized_data["company"]
    data["user"] = userid
    assignTableData = CloudTelephonyChannelAssign.objects.filter(
        cloud_telephony_channel_table=data["cloud_telephony_channel_table"],
        priority=data["priority"],
    ).first()
    if assignTableData:
        return "Please change the priority for adding this channel, as this priority already exists."
    serializer1 = CloudTelephonyChannelAssignSerializer(data=data)
    if serializer1.is_valid():
        cloud_telephony_channel = serializer1.save()
        return cloud_telephony_channel
    else:
        raise ValueError(serializer.errors)

def updateCloudTelephoneyChannelAssign(id, data):
    try:
        updatedData = CloudTelephonyChannelAssign.objects.get(id=id)
        serializer = CloudTelephonyChannelAssignSerializer(
            updatedData, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise ValueError(serializer.errors)
    except ObjectDoesNotExist:
        return None
    

def deleteCloudTelephoneyChannelAssign(id):
    try:
        createdData = CloudTelephonyChannelAssign.objects.get(id=id)
        createdData.delete()
        return True
    except ObjectDoesNotExist:
        return False