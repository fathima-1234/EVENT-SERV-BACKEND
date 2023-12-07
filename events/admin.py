from django.contrib import admin
from .models import Event, EventCategory, EventSlot, Location,EventMenu

admin.site.register(Event)
admin.site.register(EventCategory)
admin.site.register(EventSlot)
admin.site.register(Location)
admin.site.register(EventMenu)