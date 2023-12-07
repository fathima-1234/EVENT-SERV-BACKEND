from django.urls import path
from . import views
from .views import create_checkout_session,confirm_booking,get_booking_details

from . views import(
    
    create_booking,
    PaymentSuccessView,
    UpdateBookingView,
    
)
urlpatterns = [
    
    path("pay/", views.Start_payment.as_view(), name="payment"),
    path("success/", views.Handle_payment_success.as_view(), name="payment_success"),
    path("bookings/", views.get_user_bookings, name="bookings"),
    # servicer side
    path("servicerbookings/", views.get_servicer_bookings, name="servicer_bookings"),
    path(
        "updatebooking/<int:booking_id>/", views.Update_booking, name="update_booking"
    ),
    path(
        "cancelbooking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"
    ),
    # admin
    path("allbookings/", views.get_all_bookings, name="bookings"),
    path(
        "get-bookings-for-event/<int:event_id>/",
        views.get_bookings_for_event,
        name="bookings",
    ),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path("create-booking/",create_booking, name="create_booking"),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('update-booking/<int:booking_id>/', UpdateBookingView.as_view(), name='update-booking'),
    path('confirm-booking/', confirm_booking, name='confirm_booking'),
    path('booking-details/<int:booking_id>/', get_booking_details, name='get_booking_details'),
]   