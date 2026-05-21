from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone

from rooms.models import Room


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-check_in', '-created_at']
        constraints = [
            models.CheckConstraint(
                condition=Q(check_out__gt=models.F('check_in')),
                name='booking_check_out_after_check_in',
            ),
        ]

    @property
    def nights(self):
        return max((self.check_out - self.check_in).days, 0)

    @property
    def total_price(self):
        return self.nights * self.room.price

    def clean(self):
        errors = {}

        if self.check_in and self.check_in < timezone.localdate():
            errors['check_in'] = 'Check-in date cannot be in the past.'

        if self.check_in and self.check_out and self.check_out <= self.check_in:
            errors['check_out'] = 'Check-out date must be after check-in date.'

        if self.room_id and self.check_in and self.check_out:
            overlapping_bookings = Booking.objects.filter(
                room=self.room,
                check_in__lt=self.check_out,
                check_out__gt=self.check_in,
            )

            if self.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

            if overlapping_bookings.exists():
                errors['check_in'] = 'This room is already booked for the selected dates.'

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.user.username} booked room {self.room.room_number}"
