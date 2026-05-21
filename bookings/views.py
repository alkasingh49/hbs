from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rooms.models import Room
from .forms import BookingForm


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, room=room, user=request.user)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.full_clean()
            booking.save()

            messages.success(
                request,
                f'Room {room.room_number} booked for {booking.nights} night(s).',
            )
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the highlighted booking details.')
    else:
        form = BookingForm(room=room, user=request.user)

    return render(request, 'bookings/book_room.html', {
        'form': form,
        'room': room,
    })
