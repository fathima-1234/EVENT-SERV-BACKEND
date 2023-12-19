from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status
from events.models import Event, EventCategory, EventMenu
from base.models import User
from servicer.models import Servicer
from .serializers import (
    EventSerializer,
    EventCategorySerializer,
    PostEventSerializer,
    EventMenuSerializer,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import EventSlot
from .serializers import EventSlotSerializer, PostEventSlotSerializers
from rest_framework.generics import ListAPIView
from .models import EventSlot, Location
from .serializers import (
    EventSlotSerializer,
    LocationSerializer,
    PostLocationSerializer,
    EventDetailSerializer,
)

# from rest_framework.decorators import api_view, method_decorator
from django.utils.decorators import method_decorator

from celery.schedules import crontab
from django.http.response import HttpResponse
from django.shortcuts import render
import json

from django_celery_beat.models import PeriodicTask, CrontabSchedule
from datetime import timedelta
from django.utils import timezone
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from .tasks import test_func
from send_mail_app.tasks import send_mail_func

from .models import EventSlot
from .serializers import EventSlotSerializer, PostEventSlotSerializers

from .models import Feedback
from .serializers import FeedbackSerializer

from rest_framework import generics, permissions


# Create your views here.
def test(request):
    test_func.delay()
    return HttpResponse("Done")


def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Sent")


def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour=20, minute=45)
    task = PeriodicTask.objects.create(
        crontab=schedule,
        name="schedule_mail_task_" + "5",
        task="send_mail_app.tasks.send_mail_func",
    )  # , args = json.dumps([[2,3]]))
    return HttpResponse("Done")


class EventCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = EventCategorySerializer

    def get_queryset(self):
        servicer_id = self.request.user.id
        print("Logged-in Servicer ID:", servicer_id)
        queryset = EventCategory.objects.filter(servicer_id=servicer_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(servcier=self.request.user)


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        servicer_id = self.request.user.id
        print("Logged-in Servicer ID:", servicer_id)
        queryset = Event.objects.filter(servicer_id=servicer_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(servicer=self.request.user)


class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = EventCategory.objects.all()
        serializer = EventCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# eventListing
class EventListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            event = Event.objects.all()
            serializer = EventSerializer(event, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )


# SingleViewOfEvents
class EventDetailView(APIView):
    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
            serializer = EventDetailSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response(
                {"message": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )


class HomeListEvent(RetrieveAPIView):
    def get(self, request):
        queryset = Event.objects.all()
        serializer = EventSerializer(queryset, many=True)
        lookup_field = "id"
        return Response(serializer.data)


class HomeListLocation(RetrieveAPIView):
    def get(self, request):
        queryset = EventCategory.objects.all()
        serializer = EventCategorySerializer(queryset, many=True)
        return Response(serializer.data)


class EventDeleteView(APIView):
    def delete(self, request, event_id):
        queryset = Event.objects.filter(id=event_id)
        queryset.delete()
        return Response({"msg": "Event deleted successfully"})


class EventUpdateView(APIView):
    def put(self, request, event_id):
        try:
            Event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"msg": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostEventSerializer(Event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Event updated successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateEvent(APIView):
    def post(self, request, format=None):
        serializer = PostEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Event created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, event_id=None):
        if event_id is not None:
            queryset = Event.objects.get(id=event_id)
            serializer = EventSerializer(queryset)
            return Response(serializer.data)
        return Response({"msg": "Event not found"}, status=404)


class CreateEventCategory(APIView):
    def post(self, request, format=None):
        serializer = EventCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Event category created"}, status=status.HTTP_201_CREATED
            )
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    def delete(self, request, cat_id):
        queryset = EventCategory.objects.get(id=cat_id)
        queryset.delete()
        return Response({"msg": "Category deleted successfully"})


class CategoryUpdateView(APIView):
    def get(self, request, cat_id):
        category = EventCategory.objects.get(id=cat_id)
        serializer = EventCategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Category updated successfully"})
        else:
            return Response(serializer.errors)


class ApproveEvent(APIView):
    def get(self, request, car_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"msg": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        event.is_approved = True
        event.save()
        return Response({"msg": "Event approved"})


class RejectEvent(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"msg": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        event.is_approved = False
        event.save()
        return Response({"msg": "Event rejected"})


class BlockEvent(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"msg": "Event not found"}, status=status.HTTP_404_NOT_FOUND
            )

        event.is_approved = not event.is_approved
        event.save()
        return Response({"msg": "Event block status updated"})


class MyEvents(APIView):
    def get(self, request, user_id):
        try:
            user = Sevicer.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        events = Event.objects.filter(user=user)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def get_events_by_servicer(request):
    servicer_id = request.user.id
    events = Event.objects.filter(servicer_id=servicer_id)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class SingleEventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "id"


class GetEventSlotsInHome(APIView):
    def get(self, request, event_id):
        print(event_id)
        slot = EventSlot.objects.filter(eventr=event_id, is_booked=False)
        print(slot)
        serializer = EventSlotSerializer(slot, many=True)

        return Response(serializer.data)


# LocationListing
class LocationListView(APIView):
    def get(self, request, format=None):
        try:
            unique_citys = Event.objects.values_list("city", flat=True).distinct()
            return Response({"citys": list(unique_citys)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.permissions import IsAuthenticated


class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = EventCategory.objects.all()
        serializer = EventCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = EventCategorySerializer(data=request.data)

        if serializer.is_valid():
            category = serializer.save(is_active=True)
            return Response(
                {"message": "Category created successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateView(APIView):
    def get(self, request):
        categories = EventCategory.objects.all()
        serializer = EventCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = EventCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryUpdateDeleteView(APIView):
    def get_category(self, category_id):
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_id):
        category = self.get_category(category_id)
        if category:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        return Response(
            {"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, category_id):
        category = self.get_category(category_id)
        if category:
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, category_id):
        category = self.get_category(category_id)
        if category:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )


class MenuListCreateView(APIView):
    def get(self, request):
        menu = EventMenu.objects.all()
        serializer = EventMenuSerializer(menu, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = EventMenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateEventMenu(APIView):
    def post(self, request, format=None):
        serializer = EventMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Event menu created"}, status=status.HTTP_201_CREATED
            )
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDeleteView(APIView):
    def delete(self, request, cat_id):
        queryset = EventMenu.objects.get(id=cat_id)
        queryset.delete()
        return Response({"msg": "Menu deleted successfully"})


class MenuUpdateView(APIView):
    def get(self, request, cat_id):
        menu = EventMenu.objects.get(id=cat_id)
        serializer = EventMenuSerializer(menu, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Menu updated successfully"})
        else:
            return Response(serializer.errors)


class GetEventSlotsInHome(APIView):
    def get(self, request, event_id):
        print(event_id)
        slot = EventSlot.objects.filter(eventt=event_id, is_booked=False)
        print(slot)
        serializer = EventSlotSerializer(slot, many=True)

        return Response(serializer.data)


from rest_framework.permissions import IsAuthenticated


class SlotCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = PostEventSlotSerializers(data=request.data)
        if serializer.is_valid():
            event = serializer.validated_data["event"]
            date = serializer.validated_data["date"]
            if EventSlot.objects.filter(event=event, date=date).exists():
                return Response(
                    {"msg": "Slot already exists"}, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(is_booked=False)

            return Response({"msg": "Slot created"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, event_id=None):
        if event_id is not None:
            queryset = EventSlot.objects.filter(id=event_id)
            serializer = EventSlotSerializer(queryset)
            return Response(serializer.data)
        return Response({"msg": "Slot not found"}, status=status.HTTP_404_NOT_FOUND)


class GetEventSlots(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event_slots = EventSlot.objects.filter(event=event_id)
            serializer = EventSlotSerializer(event_slots, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SingleEventSlotDetailView(RetrieveAPIView):
    serializer_class = EventSlotSerializer

    def get_object(self):
        event_id = self.kwargs.get("event_id")
        date = self.request.query_params.get("date")
        queryset = EventSlot.objects.filter(event_id=event_id, date=date)
        return get_object_or_404(queryset)


class EventSlotsListView(ListAPIView):
    serializer_class = EventSlotSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("id")
        return EventSlot.objects.filter(event_id=event_id)


class CreateEventMenu(APIView):
    def post(self, request, format=None):
        serializer = EventMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Event menu created"}, status=status.HTTP_201_CREATED
            )
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
