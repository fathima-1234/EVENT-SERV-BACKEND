from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from backend import settings
from django.utils import timezone
from datetime import timedelta
from events.models import Event
@shared_task(bind=True)
def send_mail_func(self):
    events = Event.objects.filter(servicer__is_servicer=True)
    # users = get_user_model().objects.filter(is_servicer = True)
    servicers = get_user_model().objects.filter(events__in=events).distinct()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    current_time = timezone.now()
    for event in events:
        if current_time > event.ending_time and not event.renewal_email_sent:
            servicer = event.servicer 
            to_email = servicer.email
            mail_subject = "Event Renewal Reminder"
            message = f"Dear {servicer.username},\n\nPlease renew your event '{event.name}' as it has reached its ending time."
        
            send_mail(
                subject = mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True,
            )
            event.renewal_email_sent = True
            event.is_approved = False
            event.save()

    return "Done"