from django.dispatch import Signal

# Custom signal for sending email notifications
order_paid_signal = Signal()


# Custom signal for sending email notifications for booking updates
booking_updated_signal = Signal()
