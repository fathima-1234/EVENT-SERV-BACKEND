from django.urls import path
from . import views
from .views import create_checkout_session,confirm_booking,get_booking_details
from .views import update_booking_status
from . views import create_booking
urlpatterns = [
    
   
    path("bookings/", views.get_user_bookings, name="bookings"),
   
    path("servicerbookings/", views.get_servicer_bookings, name="servicer_bookings"),
   
    path(
        "cancelbooking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"
    ),
   
    path("allbookings/", views.get_all_bookings, name="bookings"),
    path(
        "get-bookings-for-event/<int:event_id>/",
        views.get_bookings_for_event,
        name="bookings",
    ),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path("create-booking/",create_booking, name="create_booking"),
    
    path('confirm-booking/', confirm_booking, name='confirm_booking'),
    path('booking-details/<int:booking_id>/', get_booking_details, name='get_booking_details'),
    path('updateBookingStatus/<int:booking_id>/', update_booking_status, name='update_booking_status'),
]   