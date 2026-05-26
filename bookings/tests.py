from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from rooms.models import Room

from .forms import BookingForm
from .models import Booking, Coupon


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

    def test_booking_form_requires_dates(self):
        form = BookingForm({}, room=self.room, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('Please select a check-in date.', str(form.errors))
        self.assertIn('Please select a check-out date.', str(form.errors))

    def test_booking_view_shows_message_for_missing_dates(self):
        self.client.login(username='guest', password='test-password')

        response = self.client.post(f'/booking/{self.room.id}/', {})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please select a check-in date.')

    def test_booking_view_shows_message_for_past_check_in(self):
        self.client.login(username='guest', password='test-password')
        today = timezone.localdate()

        response = self.client.post(
            f'/booking/{self.room.id}/',
            {
                'check_in': today - timedelta(days=1),
                'check_out': today + timedelta(days=1),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-in date cannot be in the past.')

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

    def test_booking_view_shows_message_for_checkout_before_checkin(self):
        self.client.login(username='guest', password='test-password')
        today = timezone.localdate()

        response = self.client.post(
            f'/booking/{self.room.id}/',
            {
                'check_in': today + timedelta(days=2),
                'check_out': today + timedelta(days=1),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Check-out date must be after check-in date.')

    def test_rejects_overlapping_booking(self):
        today = timezone.localdate()
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=today + timedelta(days=2),
            check_out=today + timedelta(days=5),
        )
        self.client.login(username='guest', password='test-password')

        response = self.client.post(
            f'/booking/{self.room.id}/',
            {
                'check_in': today + timedelta(days=4),
                'check_out': today + timedelta(days=6),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertContains(response, 'This room is already booked for the selected dates.')

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

    def test_accepts_active_coupon_code(self):
        Coupon.objects.create(code='SAVE25', discount_percent=25, active=True)
        today = timezone.localdate()

        form = BookingForm(
            {
                'check_in': today + timedelta(days=2),
                'check_out': today + timedelta(days=4),
                'coupon_code': 'save25',
            },
            room=self.room,
            user=self.user,
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.coupon.code, 'SAVE25')

    def test_rejects_inactive_coupon_code(self):
        Coupon.objects.create(code='OLD10', discount_percent=10, active=False)
        today = timezone.localdate()

        form = BookingForm(
            {
                'check_in': today + timedelta(days=2),
                'check_out': today + timedelta(days=4),
                'coupon_code': 'OLD10',
            },
            room=self.room,
            user=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn('valid active coupon', str(form.errors))

    def test_discounted_total_uses_booking_snapshot(self):
        today = timezone.localdate()
        coupon = Coupon.objects.create(code='SAVE25', discount_percent=25)
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            coupon=coupon,
            discount_percent=coupon.discount_percent,
            check_in=today + timedelta(days=2),
            check_out=today + timedelta(days=4),
        )

        coupon.discount_percent = 5
        coupon.save()
        booking.refresh_from_db()

        self.assertEqual(booking.subtotal, 9000)
        self.assertEqual(booking.discount_amount, 2250)
        self.assertEqual(booking.total_price, 6750)
