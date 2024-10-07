from accounts.models import UserProfile
from shipment.models import ShipmentModel
from shipment.serializers import ShipmentSerializer
from django.core.exceptions import ObjectDoesNotExist
from accounts.serializers import UserProfileSerializer
def createShipment(data, userid):
    userData = UserProfile.objects.filter(user_id=userid).first()
    serializer = UserProfileSerializer(userData)
    serialized_data = serializer.data
    mutable_data = data.copy()
    mutable_data["branch"] = serialized_data["branch"]
    mutable_data["company"] = serialized_data["company"]
    # data["branch"] = serialized_data["branch"]
    # data["company"] = serialized_data["company"]
    serializer = ShipmentSerializer(data=mutable_data)
    if serializer.is_valid():
        savedata = serializer.save()
        return savedata
    else:
        raise ValueError(serializer.errors)
    
def getShipment(user_id, id=None):
    try:
        tableData = ""
        if user_id is not None:
            userData = UserProfile.objects.filter(user_id=user_id).first()
            serializer = UserProfileSerializer(userData)
            serialized_data = serializer.data
            if id:
                tableData = ShipmentModel.objects.filter(
                    branch=serialized_data["branch"],
                    company=serialized_data["company"],
                    id=id,
                )
            else:
                tableData = ShipmentModel.objects.filter(
                    branch=serialized_data["branch"], company=serialized_data["company"]
                )
        return tableData
    except ObjectDoesNotExist:
        return False
    

def deleteShipment(id):
    try:
        data = ShipmentModel.objects.get(id=id)
        data.delete()
        return True
    except ObjectDoesNotExist:
        return False

def updateShipment(id, data):
    try:
        updatedData = ShipmentModel.objects.get(id=id)
        serializer = ShipmentSerializer(updatedData, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise ValueError(serializer.errors)
    except ObjectDoesNotExist:
        return None