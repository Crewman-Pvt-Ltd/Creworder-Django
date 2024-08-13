from rest_framework import serializers
from .models import FollowUp,Notepad
class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = '__all__'


class NotepadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notepad
        fields = '__all__'