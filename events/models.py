from django.db import models
from django.contrib.auth import get_user_model
from base.models import User
from django.utils import timezone
from datetime import date



class EventCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to="photos/event_categories")
    is_active = models.BooleanField(default=True)
    servicer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="servicer_categories"
    )

    def __str__(self):
        return self.name



class Event(models.Model):
    name = models.CharField(max_length=500, null=False)
    year_manufactured = models.PositiveIntegerField()
    seating_capacity = models.PositiveIntegerField()
    description = models.CharField(max_length=600, null=False)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos/events",null=True, blank=True)
    image1 = models.ImageField(upload_to="photos/events",null=True, blank=True)
    image2 = models.ImageField(upload_to="photos/events",null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=True)
    is_rejected = models.BooleanField(default=False)
    is_veg = models.BooleanField(default=False)
    servicer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    city = models.CharField(max_length=100, default = None)
    start_time = models.DateTimeField(default=timezone.now)
    ending_time = models.DateTimeField(default=timezone.now)  # Set a default value
    renewal_email_sent = models.BooleanField(default=False)
   
    def get_event_status(self):
        if self.is_rejected:
            return "Rejected"
        elif self.is_approved:
            return "Approved"
        elif self.renewal_email_sent:
            return "Closed (Renewal Email Sent)"
        else:
            return "Pending Approval"

    def __str__(self):
        return self.name
class EventMenu(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to="photos/event_menu")
    is_active = models.BooleanField(default=True)
    servicer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="servicer_menu"
    )

    def __str__(self):
        return self.name

        
class Location(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class EventSlot(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event.name} - {self.date} "


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null = True)
    comment = models.TextField()