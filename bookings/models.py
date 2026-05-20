from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room


class Booking(models.Model):

    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    check_in = models.DateField()

    check_out = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} booked {self.room.room_number}"