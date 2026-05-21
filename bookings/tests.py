from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from rooms.models import Room
from .forms import BookingForm
from .models import Booking


class BookingValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='guest',
            password='test-password',
        )
        self.room = Room.objects.create(
            room_number='101',
            room_type='Deluxe',
            price=4500,
            available=True,
        )

    def test_rejects_past_check_in(self):
        booking = Booking(
            user=self.user,
            room=self.room,
            check_in=timezone.localdate() - timedelta(days=1),
            check_out=timezone.localdate() + timedelta(days=1),
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_rejects_check_out_before_check_in(self):
        today = timezone.localdate()
        booking = Booking(
            user=self.user,
            room=self.room,
            check_in=today + timedelta(days=2),
            check_out=today + timedelta(days=2),
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_rejects_overlapping_booking(self):
        today = timezone.localdate()
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=today + timedelta(days=2),
            check_out=today + timedelta(days=5),
        )

        form = BookingForm(
            {
                'check_in': today + timedelta(days=4),
                'check_out': today + timedelta(days=6),
            },
            room=self.room,
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn('This room is already booked', str(form.errors))

    def test_allows_back_to_back_bookings(self):
        today = timezone.localdate()
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=today + timedelta(days=2),
            check_out=today + timedelta(days=5),
        )

        form = BookingForm(
            {
                'check_in': today + timedelta(days=5),
                'check_out': today + timedelta(days=7),
            },
            room=self.room,
            user=self.user,
        )

        self.assertTrue(form.is_valid(), form.errors)
