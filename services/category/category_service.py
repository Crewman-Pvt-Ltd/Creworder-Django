import os
import pdb

from orders.models import CategoryModel
from accounts.models import UserProfile
from orders.serializers import CategorySerializer
from django.core.exceptions import ObjectDoesNotExist
from accounts.serializers import UserProfileSerializer


def createCategory(data, userid):
    userData = UserProfile.objects.filter(user_id=userid).first()
    serializer = UserProfileSerializer(userData)
    serialized_data = serializer.data
    data["branch"] = serialized_data["branch"]
    data["company"] = serialized_data["company"]
    data["user"] = userid
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        cloud_telephony_channel = serializer.save()
        return cloud_telephony_channel
    else:
        raise ValueError(serializer.errors)


def updateCategory(id, data):
    try:
        updatedData = CategoryModel.objects.get(id=id)
        serializer = CategorySerializer(
            updatedData, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise ValueError(serializer.errors)
    except ObjectDoesNotExist:
        return None


def deleteCategory(id):
    try:
        data = CategoryModel.objects.get(id=id)
        data.delete()
        return True
    except ObjectDoesNotExist:
        return False


def getCategory(user_id, pk):
    try:
        tableData = ""
        if user_id is not None:
            userData = UserProfile.objects.filter(user_id=user_id).first()
            serializer = UserProfileSerializer(userData)
            serialized_data = serializer.data
            tableData = CategoryModel.objects.filter(
                branch=serialized_data["branch"], company=serialized_data["company"]
            )

            if pk is not None:
                tableData = CategoryModel.objects.filter(
                    branch=serialized_data["branch"], company=serialized_data["company"], id=pk
                )

        return tableData
    except ObjectDoesNotExist:
        return False
