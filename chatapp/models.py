from django.db import models
from base.models import User


class Room(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="images/",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    servicer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self):
        return self.name

    def get_last_message(self):
        last_message = self.messages.last()
        return last_message

    def get_unread_count(self, user):
        unread_count = self.messages.filter(author=user, is_read=False).count()
        return unread_count


class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} - {self.content}"
