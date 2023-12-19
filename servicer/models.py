from django.db import models
from base.models import User

# Create your models here.


class Servicer(models.Model):
    full_name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100, default="")
    is_active = models.BooleanField(default=False)
    is_servicer = models.BooleanField(default=False)

    def __str__(self):
        if self.full_name:
            return self.full_name

        else:
            return "Servicer"
