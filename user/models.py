from django.db import models
from django.contrib.auth import get_user_model  # Import get_user_model
from events.models import Event

# Use get_user_model to reference the user model

from base.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=100, default="")
    profile_photo = models.ImageField(
        upload_to="profile_pictures", default="profile/profile.jpg"
    )
    email = models.EmailField(default="")

    def __str__(self):
        return str(self.user)
