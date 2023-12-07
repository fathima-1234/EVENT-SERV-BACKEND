from django.contrib import admin
from .models import Servicer


class ServicerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Servicer,ServicerAdmin)