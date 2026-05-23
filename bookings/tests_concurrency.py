import threading
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import connection
from django.test import Client, TestCase
from django.utils import timezone

from rooms.models import Room

from .models import Booking


class BookingConcurrencyTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.room = Room.objects.create(
            room_number='900',
            room_type='Executive',
            price=7000,
            available=True,
        )
        self.check_in = timezone.localdate() + timedelta(days=7)
        self.check_out = timezone.localdate() + timedelta(days=9)

    def _book_room(self, username, password, results, index):
        client = Client()
        client.login(username=username, password=password)
        response = client.post(f'/booking/{self.room.id}/', {
            'check_in': self.check_in,
            'check_out': self.check_out,
        })
        results[index] = response.status_code

    def test_concurrent_bookings_do_not_create_double_booking(self):
        if connection.vendor != 'postgresql':
            self.skipTest('PostgreSQL required for concurrency lock test.')

        results = [None, None]
        t1 = threading.Thread(target=self._book_room, args=('user1', 'testpass', results, 0))
        t2 = threading.Thread(target=self._book_room, args=('user2', 'testpass', results, 1))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(Booking.objects.filter(room=self.room, check_in=self.check_in, check_out=self.check_out).count(), 1)
        self.assertIn(302, results)
