from django.shortcuts import render, redirect
from rest_framework.views import APIView
from base.models import User, Servicer
from events.models import Event, EventSlot, EventMenu
import razorpay
from datetime import datetime
from .serializers import (
    EventBookingUpdateSerializer,
    EventBookingSerializer,
    OrderSerializer,
)
from rest_framework.response import Response
import json
from .models import EventBooking, Order
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from decimal import Decimal
from .signals import order_paid_signal, booking_updated_signal
from django.core.mail import send_mail

from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

stripe.api_key = settings.STRIPE_SECRET_KEY

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from stripe import PaymentIntent
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from .models import EventBooking  # Import your EventBooking model
from django.http import HttpResponseRedirect


@csrf_exempt
@require_POST
def create_checkout_session(request):
    try:
        payload = json.loads(request.body)
        print("Payload:", payload)
        booking_id = payload.get("booking_id")
        if not booking_id:
            return JsonResponse({"error": "Booking ID is required"}, status=400)

        booking = get_object_or_404(EventBooking, pk=booking_id)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",  # Change to your currency
                        "product_data": {
                            "name": booking.event.name,
                            # 'images': [booking.event.image.url] if booking.event.image else [],
                        },
                        "unit_amount": int(
                            booking.calculate_total_charges() * 100
                        ),  # Amount in cents
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            # success_url=settings.SITE_URL + '/order-status/?success=true',
            success_url=settings.SITE_URL
            + f"/order-status/?success=true&amount={booking.calculate_total_charges()}&currency=inr",
            cancel_url=settings.SITE_URL + "/order-status/?canceled=true",
        )
        booking.is_paid = True
        booking.status = "completed"
        booking.save()

        return JsonResponse(
            {"session_id": session.id, "stripe_public_key": settings.STRIPE_PUBLIC_KEY}
        )
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)


def create_booking(request):
    try:
        # Extract data from the request
        event_id = request.POST.get("event")
        booked_slot_id = request.POST.get("booked_slot")
        number_of_members = request.POST.get("number_of_members")
        menu_ids = request.POST.getlist(
            "menus"
        )  # Assuming 'menus' is an array of menu ids

        # Retrieve event, booked slot, and menus
        event = get_object_or_404(Event, pk=event_id)
        booked_slot = get_object_or_404(BookedSlot, pk=booked_slot_id)
        menus = Menu.objects.filter(pk__in=menu_ids)

        # Create the booking
        booking = EventBooking.objects.create(
            user=request.user,
            event=event,
            slot=booked_slot,
            number_of_members=number_of_members,
            menus=menus,
            # ... other fields ...
        )

        # Serialize the booking data (you might need to create a serializer)
        booking_serializer = EventBookingSerializer(booking)

        # Return the response to the frontend
        response_data = {
            "success": True,
            "booking": booking_serializer.data,
        }
        return JsonResponse(response_data)

    except Exception as e:
        # Handle errors and return an appropriate response
        error_data = {"success": False, "error": str(e)}
        return JsonResponse(error_data, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_booking(request):
    try:
        event_id = request.data.get("eventId")
        slot_ids = request.data.get("selectedSlots")
        number_of_members = request.data.get("numberOfMembers")
        requirements = request.data.get("requirements")

        # Fetch the event and slots from the database
        event = Event.objects.get(id=event_id)
        slots = EventSlot.objects.filter(id__in=slot_ids)

        # Perform the booking confirmation logic (create EventBooking objects, update slots, etc.)
        # Create an EventBooking instance
        event_booking = EventBooking.objects.create(
            user=request.user,
            event=event,
            slot=slots[0],  # Assuming only one slot is selected for simplicity
            status="pending",  # You might want to set an appropriate initial status
            numberOfMembers=number_of_members,
            requirements=requirements,
            # menus={},
            # ... other fields ...
        )

        # Update the selected slots as booked
        for slot in slots:
            slot.is_booked = True
            slot.save()

        return Response({"message": "Booking confirmed successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


class BookingListView(RetrieveAPIView):
    queryset = EventBooking.objects.all()
    serializer_class = EventBookingSerializer
    lookup_field = "user_id"


class ServicerBookingsAPIView(APIView):
    def get(self, request, id):
        try:
            current_user = User.objects.get(id=id)
            event = Event.objects.get(user=current_user)
            bookings = EventBooking.objects.filter(car=car)
            serializer = EventBookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EventBooking.DoesNotExist:
            return Response("Bookings not found", status=status.HTTP_404_NOT_FOUND)


from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist


@api_view(["PUT"])
def cancel_booking(request, booking_id):
    try:
        booking = EventBooking.objects.get(id=booking_id)
    except EventBooking.DoesNotExist:
        return JsonResponse({"error": "Booking not found"}, status=404)

    if booking.status == "cancelled":
        return JsonResponse({"error": "Booking is already cancelled"}, status=400)

    try:
        # Assuming you want to set status directly in the model
        booking.status = "cancelled"
        booking.is_paid = False
        booking.save()

        # Optionally, perform any additional actions needed when a booking is cancelled

        return JsonResponse({"message": "Booking cancelled successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EventBooking
from .serializers import EventBookingSerializer


@api_view(["GET"])
def get_user_bookings(request):
    user_id = request.query_params.get("user")

    bookings = EventBooking.objects.filter(user__id=user_id)

    serializer = EventBookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_servicer_bookings(request):
    user_id = request.query_params.get("user")
    events_added_by_servicer = Event.objects.filter(servicer_id=user_id)

    bookings = EventBooking.objects.filter(event__in=events_added_by_servicer)
    serializer = EventBookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_bookings(request):
    bookings = EventBooking.objects.all()
    serializer = EventBookingSerializer(bookings, many=True)
    return Response(serializer.data)


from rest_framework import status


@api_view(["GET"])
def get_bookings_for_event(request, event_id):
    try:
        bookings = EventBooking.objects.filter(event_id=event_id)
        if not bookings:
            return Response(
                {"message": "No bookings found for this event."},
                status=status.HTTP_204_NO_CONTENT,
            )

        serializer = EventBookingSerializer(bookings, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.dispatch import receiver
from .signals import order_paid_signal, booking_updated_signal
from django.core.mail import send_mail
from django.conf import settings

from django.urls import reverse


@receiver(order_paid_signal)
def send_order_paid_notification(sender, order, **kwargs):
    user_redirect = "http://localhost:3000/mybookings"
    user_subject = "Order Processing"
    user_message = f'Dear valued customer,\n\nWe greatly appreciate your recent order. Your order has been successfully received and is currently being processed. Kindly await confirmation of your order shortly.\n\nFor your convenience, you can track and manage all your bookings by visiting the following link: <a href="{user_redirect}">Booking Management Portal</a>.\n\nShould you require any assistance or have inquiries, please do not hesitate to contact our dedicated customer service team. We are here to provide the utmost support.\n\nThank you for choosing DriveNow.\n\nBest regards,\nTeam DriveNow'
    user_recipient_list = [order.user.email]

    renter_redirect = "http://localhost:3000/servicerbookings"
    renter_subject = "New Order Received"
    renter_message = f'Dear esteemed partner,\n\nWe are pleased to inform you that a new order has been recieved. Your attention is kindly requested to review and confirm the details of this order at your earliest convenience.\n\nTo facilitate the management of your bookings, please access the following link: <a href="{renter_redirect}">Booking Management Portal</a>.\n\nShould you require any further assistance or have inquiries, please do not hesitate to contact our dedicated support team. We are committed to ensuring a seamless partnership experience.\n\nThank you for choosing DriveNow as your trusted partner.\n\nSincerely,\nTeam DriveNow'
    renter_recipient_list = [order.evvent.servicer.email]

    # Send messages to user and servicer
    send_mail(
        user_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        user_recipient_list,
        html_message=user_message,
    )
    send_mail(
        servicer_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        servicer_recipient_list,
        html_message=servicer_message,
    )


@receiver(booking_updated_signal)
def send_booking_updated_notification(sender, booking, **kwargs):
    user_redirect = "http://localhost:3000/mybookings"
    user_subject = "Booking Update"
    user_message = f'Dear valued customer,We are pleased to notify you that your car booking has been successfully updated. Your reservation for the vehicle named {booking.car.name} has been adjusted and confirmed as per your request. To conveniently access and review the latest details of your bookings, kindly click on the following link:<a href="{user_redirect}">here</a>. Should you require any further assistance or have inquiries, please do not hesitate to get in touch with our dedicated support team. We are committed to ensuring your experience with DriveNow is consistently exceptional. We appreciate your trust in DriveNow for your car rental needs and sincerely look forward to the opportunity to serve you again.Best regards,Team DriveNow'
    user_recipient_list = [booking.user.email]

    renter_redirect = "https://drive-now-client.vercel.app/renterbookings"
    renter_subject = "Booking Update"
    renter_message = f'Dear {booking.event.servicer},\n\nWe wish to inform you that the booking with ID {booking.id} for the car "{booking.car.name}" associated with your account has been successfully updated. This update was requested by the user {booking.user.first_name}.\n\nTo conveniently manage and review your bookings, please access the following link: [Manage Your Bookings](<a href="{renter_redirect}">here</a>).\n\nIf you have any questions or require further assistance, please do not hesitate to contact our dedicated support team. We are committed to ensuring a seamless experience for you and our valued users.\n\nThank you for choosing DriveNow for your car rental services.\n\nBest regards,\nTeam DriveNow'
    renter_recipient_list = [booking.event.servicer.email]

    # Send messages to user and servicer
    send_mail(
        user_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        user_recipient_list,
        html_message=user_message,
    )
    send_mail(
        servicer_subject,
        "",
        settings.DEFAULT_FROM_EMAIL,
        renter_recipient_list,
        html_message=servicer_message,
    )


def get_booking_details(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id)
    serializer = EventBookingSerializer(booking)  # Use your serializer here

    return JsonResponse(serializer.data)


@api_view(["PATCH"])
def update_booking_status(request, booking_id):
    try:
        booking = EventBooking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        return Response(
            {"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PATCH":
        new_status = request.data.get("status", None)
        if new_status is not None and new_status in [
            "pending",
            "completed",
            "rejected",
            "given",
        ]:
            booking.status = new_status
            booking.save()
            return Response({"message": "Booking status updated successfully"})
        else:
            return Response(
                {"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST
            )
