from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from bookings.models import Booking

from .models import Room


class RoomSearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='guest')
        self.single = Room.objects.create(
            room_number='101',
            room_type='Single',
            price=2000,
            available=True,
        )
        self.deluxe = Room.objects.create(
            room_number='201',
            room_type='Deluxe',
            price=4500,
            available=True,
        )
        self.suite = Room.objects.create(
            room_number='301',
            room_type='Suite',
            price=9000,
            available=False,
        )

    def test_filters_by_room_type(self):
        response = self.client.get('/', {'room_type': 'Deluxe'})

        self.assertContains(response, 'Room 201')
        self.assertNotContains(response, 'Room 101')

    def test_filters_by_price_range(self):
        response = self.client.get('/', {
            'min_price': 3000,
            'max_price': 8000,
        })

        self.assertContains(response, 'Room 201')
        self.assertNotContains(response, 'Room 101')
        self.assertNotContains(response, 'Room 301')

    def test_filters_available_rooms_only(self):
        response = self.client.get('/', {'available_only': 'on'})

        self.assertContains(response, 'Room 101')
        self.assertContains(response, 'Room 201')
        self.assertNotContains(response, 'Room 301')

    def test_excludes_rooms_booked_for_selected_dates(self):
        today = timezone.localdate()
        Booking.objects.create(
            user=self.user,
            room=self.deluxe,
            check_in=today + timedelta(days=2),
            check_out=today + timedelta(days=5),
        )

        response = self.client.get('/', {
            'check_in': today + timedelta(days=3),
            'check_out': today + timedelta(days=6),
        })

        self.assertContains(response, 'Room 101')
        self.assertNotContains(response, 'Room 201')
