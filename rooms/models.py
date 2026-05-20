from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number