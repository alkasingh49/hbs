from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from rooms.models import Room
from .forms import BookingForm
from .models import Booking, Coupon


def room_has_overlapping_booking(room, check_in, check_out):
    return Booking.objects.filter(
        room=room,
        check_in__lt=check_out,
        check_out__gt=check_in,
    ).exists()


def booking_context(form, room, active_coupons):
    return {
        'form': form,
        'room': room,
        'active_coupons': active_coupons,
        'coupon_discounts': {
            coupon.code: coupon.discount_percent
            for coupon in active_coupons
        },
    }


def first_form_error(form):
    for field_name, errors in form.errors.items():
        if errors:
            return errors[0]

    return 'Please correct the highlighted booking details.'


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    active_coupons = Coupon.objects.filter(active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST, room=room, user=request.user)

        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            if room_has_overlapping_booking(room, check_in, check_out):
                messages.error(
                    request,
                    'This room is already booked for the selected dates. Please choose different dates.',
                )
                return render(
                    request,
                    'bookings/book_room.html',
                    booking_context(form, room, active_coupons),
                )

            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.coupon = form.coupon
            booking.discount_percent = form.coupon.discount_percent if form.coupon else 0

            try:
                booking.full_clean()
                booking.save()
            except ValidationError:
                messages.error(
                    request,
                    'This booking could not be completed. Please review the selected dates.',
                )
                return render(
                    request,
                    'bookings/book_room.html',
                    booking_context(form, room, active_coupons),
                )

            coupon_message = ''
            if booking.coupon:
                coupon_message = f' Coupon {booking.coupon.code} applied.'

            messages.success(
                request,
                f'Room {room.room_number} booked for {booking.nights} night(s).{coupon_message}',
            )
            return redirect('profile')
        else:
            messages.error(request, first_form_error(form))
    else:
        form = BookingForm(room=room, user=request.user)

    return render(
        request,
        'bookings/book_room.html',
        booking_context(form, room, active_coupons),
    )
