from rest_framework import serializers
from base.serializers import UserSerializer
from events.serializers import EventSerializer, EventSlotSerializer, EventMenuSerializer
from .models import EventBooking, Order


class EventBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    event = EventSerializer()
    slot = EventSlotSerializer()
    # menu = EventMenuSerializer()

    class Meta:
        model = EventBooking
        fields = "__all__"


class EventBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ["status"]

    def validate(self, data):
        # Validate 'status' field
        status = data.get("status")
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"