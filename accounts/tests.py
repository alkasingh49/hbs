from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking
from rooms.models import Room


class AccountsTests(TestCase):
    def test_signup_creates_user_and_redirects(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'newguest',
                'email': 'newguest@example.com',
                'password1': 'ComplexPass123!',
                'password2': 'ComplexPass123!',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newguest').exists())

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_profile_shows_user_bookings(self):
        user = User.objects.create_user(username='guest', password='test-password')
        room = Room.objects.create(
            room_number='101',
            room_type='Single',
            price=2000,
            available=True,
        )
        Booking.objects.create(
            user=user,
            room=room,
            check_in='2026-06-01',
            check_out='2026-06-03',
        )

        self.client.login(username='guest', password='test-password')
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room 101')
