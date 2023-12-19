from rest_framework import serializers
from events.models import Event, EventCategory, EventSlot, Location, EventMenu
from servicer.serializers import ServicerSerializer
from .models import Feedback


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = "__all__"


class EventMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMenu
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class PostLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    servicer_name = serializers.SerializerMethodField()
    servicer_id = serializers.SerializerMethodField()
    category = EventCategorySerializer()
    status = serializers.CharField(source="get_event_status", read_only=True)

    class Meta:
        model = Event
        fields = "__all__"

    def get_servicer_name(self, event):
        return event.servicer.get_full_name()

    def get_servicer_id(self, event):
        return event.servicer.id


class PostEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class EventSlotSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = EventSlot
        fields = "__all__"


class PostEventSlotSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventSlot
        fields = "__all__"


# EventSingleView
class EventDetailSerializer(serializers.ModelSerializer):
    servicer_name = serializers.SerializerMethodField()

    category = EventCategorySerializer()
    # servicer = ServicerSerializer()

    class Meta:
        model = Event
        fields = "__all__"

    def get_servicer_name(self, event):
        return event.servicer.get_full_name()


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"
