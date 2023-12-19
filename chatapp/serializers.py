from rest_framework import serializers
from .models import Room, Message
from base.serializers import UserSerializer
from base.models import User


class RoomSerializer(serializers.ModelSerializer):
    servicer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Room
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
