from rest_framework import serializers
from .models import Servicer


class ServicerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicer
        fields = "__all__"
