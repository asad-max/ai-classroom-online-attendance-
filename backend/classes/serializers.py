# from rest_framework import serializers
# from .models import ClassRoom
# 
# class ClassRoomSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = ClassRoom
        # fields = '__all__'
        # read_only_fields = ['instructor', 'join_code', 'created_at']

from rest_framework import serializers
from .models import ClassRoom

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'
        read_only_fields = ['instructor', 'join_code', 'created_at', 'is_live']
