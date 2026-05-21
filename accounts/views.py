from django.shortcuts import render
from bookings.models import Booking

def profile(request):
    bookings = Booking.objects.all()

    return render(request, 'rooms/profile.html', {'bookings': bookings})