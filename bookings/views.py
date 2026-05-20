from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookingForm
from rooms.models import Room

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.save()

            return redirect('/rooms/')

    else:
        form = BookingForm()

    return render(request, 'bookings/book_room.html', {
        'form': form,
        'room': room
    })