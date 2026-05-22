from django.shortcuts import render

from bookings.models import Booking
from .forms import RoomSearchForm
from .models import Room


def room_list(request):
    form = RoomSearchForm(request.GET or None)
    rooms = Room.objects.all().order_by('room_number')
    selected_check_in = None
    selected_check_out = None

    if form.is_valid():
        room_type = form.cleaned_data.get('room_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        selected_check_in = form.cleaned_data.get('check_in')
        selected_check_out = form.cleaned_data.get('check_out')
        available_only = form.cleaned_data.get('available_only')

        if room_type:
            rooms = rooms.filter(room_type=room_type)

        if min_price is not None:
            rooms = rooms.filter(price__gte=min_price)

        if max_price is not None:
            rooms = rooms.filter(price__lte=max_price)

        if available_only:
            rooms = rooms.filter(available=True)

        if selected_check_in and selected_check_out:
            booked_room_ids = Booking.objects.filter(
                check_in__lt=selected_check_out,
                check_out__gt=selected_check_in,
            ).values_list('room_id', flat=True)
            rooms = rooms.exclude(id__in=booked_room_ids)

    return render(request, 'rooms/room_list.html', {
        'rooms': rooms,
        'form': form,
        'selected_check_in': selected_check_in,
        'selected_check_out': selected_check_out,
    })
