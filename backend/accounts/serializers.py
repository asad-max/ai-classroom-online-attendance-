from rest_framework import serializers
from .models import CustomUser
from .utils import save_face_encoding

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password', 'role', 'face_image']

    def create(self, validated_data):
        face_img = validated_data.pop('face_image', None)
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if face_img:
            save_face_encoding(user, face_img)
        return user