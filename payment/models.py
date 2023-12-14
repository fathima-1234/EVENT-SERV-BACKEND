from django.db import models
from base.models import User
from events.models import Event, EventSlot, EventMenu

# Create your models here.


class Order(models.Model):
    order_product = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_product


class EventBooking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_active": True}
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    slot = models.ForeignKey(EventSlot, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
        ("returned", "Returned"),
        
        
        
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    
    is_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now=True)
   
    requirements = models.TextField()
    numberOfMembers = models.IntegerField()
    stripe_session_id = models.CharField(max_length=100, blank=True, null=True)
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
       
    )

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    def calculate_total_charges(self):
   
        total_charges = self.event.price_per_person * self.numberOfMembers
        return total_charges

  

    def __str__(self):
        return f"{self.user.username} - {self.event.name} - {self.slot.date}"
