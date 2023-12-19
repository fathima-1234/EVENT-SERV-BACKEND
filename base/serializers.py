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
        fields = "__all__"

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ServicerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicer
        fields = "__all__"
