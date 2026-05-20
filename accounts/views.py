from django.shortcuts import render
from bookings.models import Booking


def profile(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'profile.html', {
        'bookings': bookings
    })