from rest_framework import serializers
from base.models import User, Servicer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_servicer', 'is_profile']
        read_only_fields = ['is_active', 'is_staff', 'is_admin', 'is_superadmin', 'is_servicer', 'is_profile']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class ServicerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicer
        fields = ['user']
